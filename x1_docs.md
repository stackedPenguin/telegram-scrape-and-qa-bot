The provided content describes the X1 blockchain, its technical specifications, validator information, and developer resources.

Here's a summary of the key information:

**1. Introduction to X1**
*   **Mission:** A high-performance, high-throughput, monolithic L1 blockchain focused on providing decentralized, censorship-resistant infrastructure for free transactions with minimal technical and economic limitations.
*   **Solana Compatibility:** Fully compatible with the Solana Virtual Machine (SVM), allowing seamless deployment of dApps.
*   **Key Differentiators:**
    *   **Zero-Cost Votes:** Significantly lowers validator entry barriers by eliminating voting fees (unlike Solana), reducing daily validator costs to approximately $5.
    *   **Congestion-Reflective Dynamic Base Fees:** Adjusts transaction fees based on global compute-unit (CU) congestion, preventing underpricing, spam, and ensuring fair transaction pricing, similar to Ethereum's EIP-1559 but with Solana's parallelism.

**2. The Constitution of X1**
Guiding principles for X1's vision for a decentralized, self-sovereign digital future:
*   Freedom of Individual Agency
*   Self-Custody and Ownership
*   Privacy as a Choice
*   Transparency and Accountability via Code
*   Evolution Through Innovation

**3. Key Technical Features**
*   **SVM Capacity Scaling (Dynamic Thread Scaling):** Addresses Solana's limitation of fixed banking threads by dynamically adjusting the number of banking threads based on the node's CPU core count, optimizing hardware utilization and increasing throughput.
*   **Stake, Performance, and Randomness-Based Leader Selection:** Combines stake weight, historical validator performance, and Verifiable Random Function (VRF) integration (via Anti-Collusion Protocol - ACP) to select leaders, aiming for more efficient and decentralized block production.
*   **Homomorphic Encryption:** Allows computations on encrypted data without decryption, enhancing privacy, security, and regulatory compliance for use cases like encrypted on-chain intents, bad-MEV prevention, and private governance.
*   **Scaling Through Reductionism (Subcommittee Voting):** Improves consensus scalability by using smaller subsets of nodes (subcommittees) for voting, reducing communication overhead and achieving O(1) time complexity for consensus operations, unlike Solana's O(n^2).

**4. Validator Information**
*   **Rewards:** Validators can earn rewards through voting rewards (from inflation), commissions from delegators, block rewards (transaction fees), and a bootstrap bonus program.
*   **Costs & Hardware:** The primary direct cost is hardware. X1 validators do not pay for votes. Recommended hardware: 12+ cores/24+ threads CPU (3GHz+), 192GB+ RAM, 4TB NVME disk (bare metal dedicated server).
*   **Setup Guides:** Detailed instructions are provided for:
    *   Creating a read-only node (installing Rust, Tachyon, Solana tools, system tuning).
    *   Creating a validator node (funding identity, creating vote and stake accounts, staking).
    *   Installing and running a Pinger to share leader data transmission times.
    *   Securing a validator with a hardware wallet (e.g., Ledger) for withdraw authority.
    *   Connecting a validator to X1 Mainnet.
*   **Incentivized Testnet Rewards:** Validators earn "Validator Credits" during testnet, convertible to XNT at mainnet launch (50,000 credits = 1 XNT). 10% is immediately claimable, 90% is locked and vested over 365 days, with unlock proportional to uptime and performance.
*   **Bootstrap Bonus:** Rewards early, performant, and decentralized validators. Includes a base reward and a +16% performance bonus for meeting criteria like self-stake range (1,000-10,000 XNT), max 10% commission, high vote credits, low skip rate, and running the latest Tachyon version.
*   **Health Checks:** Scripts are provided for a full system health report (`x1_health.sh`) and Disk IOPS testing (using `fio`) to ensure hardware meets performance requirements.

**5. Developer Information**
*   **Metaplex:** The preferred platform for digital asset creation on X1, compatible with SVM. Supports:
    *   **Token Metadata:** For fungible and semi-fungible tokens, and basic non-fungible tokens (NFTs).
    *   **Metaplex Core:** A more programmatic standard for NFTs, offering advanced functionality and efficiency with a plugin system.
    *   **Candy Machine:** Simplifies deployment of NFT collections with various "Guards" for minting conditions.
*   **Creating Programs:** Basic setup for Anchor development on X1, including quick installation scripts for dependencies (Rust, Solana CLI, Anchor, Node.js, Yarn), project initialization, building, and deployment.
*   **RPC Endpoints:**
    *   X1 Testnet: `https://rpc.testnet.x1.xyz`
    *   X1 Mainnet: `https://rpc.mainnet.x1.xyz`

**6. Network Upgrades & Maintenance**
*   **Node Maintenance:** Instructions for updating packages (`sudo apt update`, `sudo apt upgrade`), checking disk space (`df -h`).
*   **Tachyon 2.0 Migration:** Steps for validators to migrate to Tachyon v2.0, including installing the new version, stopping the old validator, backing up data, updating startup configuration, and re-delegating stake.
*   **Mainnet Buenos Aires Reboot:** Guide for validators to reset and reconnect to the X1 network after a mainnet reboot, involving stopping the validator, removing the old ledger, updating RPC, and restarting the validator.