# Telegram Chat Q&A

This project provides two Python scripts to interact with Telegram chats and perform question-answering on the chat history.

## Features

*   `list_chats.py`: Lists all your Telegram chats and allows you to export the message history of a selected chat to a Markdown file.
*   `qna.py`: A question-answering engine that uses a local vector store of a chat history file to answer your questions about it.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add the following credentials:
    ```
    TELEGRAM_API_ID=<your-telegram-api-id>
    TELEGRAM_API_HASH=<your-telegram-api-hash>
    GEMINI_API_KEY=<your-gemini-api-key>
    ```
    You can obtain the Telegram API credentials from [here](https://core.telegram.org/api/obtaining_api_id) and the Gemini API key from [Google AI Studio](https://aistudio.google.com/).

## Usage

### 1. Exporting Chat History

First, you need to export the chat history of the Telegram group you want to analyze.

1.  **Run the `list_chats.py` script:**
    ```bash
    python list_chats.py
    ```

2.  **Log in to Telegram:**
    The script will prompt you for your phone number, password, and a login code sent to you on Telegram.

3.  **Select a chat:**
    The script will list all your chats. Enter the number corresponding to the chat you want to export.

4.  **Export the chat:**
    The script will export the entire message history of the selected chat to a Markdown file (e.g., `My_Chat.md`).

### 2. Question Answering

Once you have the chat history file, you can use the `qna.py` script to ask questions about it.

1.  **Run the `qna.py` script with a question:**
    ```bash
    python qna.py "Your question about the chat history"
    ```
    For example:
    ```bash
    python qna.py "What was the main topic of discussion last week?"
    ```

2.  **Get the answer:**
    The script will create a local vector store of the chat history file (if it doesn't exist already) and then use it to find the most relevant passages to answer your question. The answer will be printed to the console.

    The first time you run this script, it will take some time to create the vector store. Subsequent runs will be much faster as they will reuse the existing vector store.
