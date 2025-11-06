import os
import sys
import textwrap
import numpy as np
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm

# Configure the generative AI model
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

def get_or_create_vector_store(file_paths, store_path="vector_store.pkl"):
    """Loads the vector store from a file or creates it if it doesn't exist."""
    if os.path.exists(store_path):
        print(f"Loading existing vector store from {store_path}")
        return pd.read_pickle(store_path)

    print("Creating new vector store...")
    content = ""
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            content += f.read()

    # Split the text into smaller chunks
    text_chunks = textwrap.wrap(content, width=2000, replace_whitespace=False, break_long_words=False)

    print(f"Embedding {len(text_chunks)} text chunks... This may take a while.")
    embeddings = []
    for chunk in tqdm(text_chunks):
        try:
            res = genai.embed_content(model="models/embedding-001", content=chunk, task_type="retrieval_document")
            embeddings.append(res["embedding"])
        except Exception as e:
            print(f"Error embedding chunk: {e}. Skipping.")
            embeddings.append(None)  # Add a placeholder for failed embeddings

    df = pd.DataFrame({
        "chunk": text_chunks,
        "embedding": embeddings,
    })

    # Remove rows with failed embeddings
    df.dropna(subset=["embedding"], inplace=True)

    print(f"Saving vector store to {store_path}")
    df.to_pickle(store_path)
    return df

def find_best_passages(query, dataframe, top_k=3):
    """Finds the most relevant passages in the DataFrame for a given query."""
    query_embedding = genai.embed_content(model="models/embedding-001", content=query, task_type="retrieval_query")["embedding"]

    # Calculate dot product similarity
    dataframe["similarity"] = dataframe["embedding"].apply(lambda x: np.dot(x, query_embedding))

    # Sort by similarity and get top_k results
    top_passages = dataframe.sort_values("similarity", ascending=False).head(top_k)
    return top_passages["chunk"].tolist()

def generate_answer(query, passages):
    """Generates an answer to the query based on the provided passages."""
    model = genai.GenerativeModel("gemini-pro-latest")

    context = "\n\n".join(passages)

    prompt = f"""
    Here is the context from the X1 Validator Army chat group and X1 documentation:
    --- CONTEXT START ---
    {context}
    --- CONTEXT END ---

    Based ONLY on the context provided, please answer the following question.
    Do not use any other information. If the answer is not found in the context, say "I could not find an answer in the provided text."

    Question: {query}
    Answer:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the answer: {e}"

def main():
    """Main function to run the Q&A engine."""
    file_paths = ["/Users/wei/projects/x1-validator/telegram/X1_Validator_Army.md", "/Users/wei/projects/x1-validator/telegram/x1_docs.md"]
    vector_store = get_or_create_vector_store(file_paths)

    if len(sys.argv) > 1 and sys.argv[1].lower() == '--chat':
        print("Starting chat session. Type 'exit' or 'quit' to end.")
        while True:
            try:
                query = input("\nAsk a question: ")
                if query.lower() in ['exit', 'quit']:
                    break
                if not query.strip():
                    continue

                print("Finding relevant passages...")
                best_passages = find_best_passages(query, vector_store)

                print("Generating answer...")
                answer = generate_answer(query, best_passages)
                print(f"\nAnswer:\n{answer}")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting chat session.")
                break
        return

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Default question if none is provided
        query = "What is the main topic of discussion?"

    print(f"\nQuestion: {query}")
    print("Finding relevant passages...")
    best_passages = find_best_passages(query, vector_store)

    print("Generating answer...")
    answer = generate_answer(query, best_passages)

    print(f"\nAnswer:\n{answer}")

if __name__ == "__main__":
    main()
