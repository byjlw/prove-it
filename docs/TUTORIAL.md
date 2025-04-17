# ProveIt: Complete Beginner's Tutorial

This step-by-step tutorial will guide you through using ProveIt to register and verify your intellectual property on the blockchain, even if you've never used cryptocurrency or GitHub before.

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up Your Computer](#setting-up-your-computer)
3. [Creating a Crypto Wallet with Rabby](#creating-a-crypto-wallet-with-rabby)
4. [Getting Some Cryptocurrency](#getting-some-cryptocurrency)
5. [Installing ProveIt](#installing-proveit)
6. [Using the Web Interface](#using-the-web-interface)
7. [Registering Your First File](#registering-your-first-file)
8. [Verifying a File](#verifying-a-file)
9. [Understanding Your Certificate](#understanding-your-certificate)
10. [Troubleshooting](#troubleshooting)

## Introduction

ProveIt is a tool that helps you prove you created something (like a document, image, or other file) at a specific time. It does this by:

1. Creating a unique "fingerprint" (hash) of your file
2. Storing this fingerprint on a blockchain (a type of secure, public database)
3. Giving you a certificate that proves when you registered the file

This can be useful for:
- Proving you wrote a book or article before someone else
- Establishing ownership of artwork or designs
- Documenting when you created research or technical documents

The best part is that your actual file never leaves your computer - only the fingerprint is stored on the blockchain.

## Setting Up Your Computer

Before we begin, you'll need to install a few basic programs on your computer.

### For Windows Users

1. **Install Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Click the "Download Python" button (get the latest version)
   - Run the installer
   - **Important**: Check the box that says "Add Python to PATH" before clicking Install

2. **Install Git**:
   - Go to [git-scm.com](https://git-scm.com/download/win)
   - Download the installer and run it
   - Use the default options during installation

3. **Install Node.js**:
   - Go to [nodejs.org](https://nodejs.org/)
   - Download the "LTS" (Long Term Support) version
   - Run the installer with default options

### For Mac Users

1. **Install Homebrew** (a package manager that makes installing software easier):
   - Open Terminal (find it in Applications > Utilities)
   - Paste this command and press Enter:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Follow the prompts on the screen

2. **Install Python, Git, and Node.js**:
   - In Terminal, paste this command and press Enter:
     ```
     brew install python git node
     ```

### For Linux Users

Use your distribution's package manager to install Python, Git, and Node.js:

```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git nodejs npm

# For Fedora
sudo dnf install python3 python3-pip git nodejs

# For Arch Linux
sudo pacman -S python python-pip git nodejs npm
```

## Creating a Crypto Wallet with Rabby

To use ProveIt, you'll need a cryptocurrency wallet. We'll use Rabby, which is a modern, feature-rich Ethereum wallet designed for DeFi and NFT users.

### Installing Rabby

1. Open your web browser (Chrome, Firefox, Edge, or Brave work best)
2. Go to [rabby.io](https://rabby.io/)
3. Click "Download" and select your browser
4. Click "Add to Chrome" (or your browser's equivalent)
5. After installation, click the Rabby icon in your browser extensions area (usually top-right)

### Setting Up Your Wallet

1. Click "Create Wallet" when Rabby opens
2. Create a password (make it strong and write it down somewhere safe)
3. You'll be shown a "Seed Phrase" (12 words) - this is EXTREMELY IMPORTANT
   - Write these words down on paper in the correct order
   - Store this paper somewhere very safe
   - Never share these words with anyone
   - If you lose these words, you'll lose access to your wallet forever
4. Confirm your seed phrase by selecting the words in the correct order
5. Your wallet is now set up!

### Understanding Your Wallet

- Your wallet has an "address" - a long string starting with "0x" (e.g., 0x71C7656EC7ab88b098defB751B7401B5f6d8976F)
- This address is like your account number - you can share it with others
- Your wallet stores your private keys (the secret information that proves you own the address)
- Rabby lets you interact with blockchain applications directly from your browser
- Rabby supports multiple networks, including Ethereum, Polygon, and other EVM-compatible chains

### Rabby's Special Features

Rabby has several advantages over other wallets:

- **Multi-chain support**: Easily switch between different blockchain networks
- **Security features**: Phishing detection and transaction simulation
- **Portfolio view**: See all your assets across different chains
- **Gas optimization**: Helps you save on transaction fees

## Getting Some Cryptocurrency

To register files on the blockchain, you'll need a small amount of cryptocurrency to pay for the transaction fees (called "gas fees").

For beginners, we recommend using the Polygon network instead of Ethereum, as the fees are much lower (often less than $0.01 per transaction).

### Getting Polygon (MATIC)

1. **Option 1: Buy through an exchange**:
   - Create an account on an exchange like [Coinbase](https://www.coinbase.com/), [Binance](https://www.binance.com/), or [Kraken](https://www.kraken.com/)
   - Complete their identity verification process
   - Buy some MATIC (about $5-10 worth is plenty for many transactions)
   - Withdraw the MATIC to your Rabby wallet address

2. **Option 2: Use a faucet for testnet tokens** (for practice only):
   - If you just want to try things out without real money, you can use the Polygon Mumbai testnet
   - Go to [faucet.polygon.technology](https://faucet.polygon.technology/)
   - Enter your Rabby address
   - Receive free test MATIC (these have no real value but work for testing)

### Configuring Rabby for Polygon

1. Open Rabby
2. Click on the network dropdown at the top (it probably says "Ethereum")
3. Select "Polygon" from the list of networks
4. If you don't see Polygon, click "Add Network" and add these details:
   - Network Name: Polygon
   - RPC URL: https://polygon-rpc.com
   - Chain ID: 137
   - Symbol: MATIC
   - Block Explorer: https://polygonscan.com

## Installing ProveIt

Now that you have the prerequisites installed, let's get ProveIt set up on your computer.

### Getting the Code from GitHub

1. Open a command prompt or terminal on your computer:
   - **Windows**: Press Win+R, type "cmd" and press Enter
   - **Mac**: Open Applications > Utilities > Terminal
   - **Linux**: Open your terminal application

2. Navigate to where you want to store the project:
   ```bash
   # For example, to put it in a "Projects" folder in your Documents
   # Windows:
   cd Documents
   mkdir Projects
   cd Projects
   
   # Mac/Linux:
   cd ~/Documents
   mkdir Projects
   cd Projects
   ```

3. Download the code from GitHub:
   ```bash
   git clone https://github.com/example/proveit.git
   cd proveit
   ```

### Setting Up ProveIt

Run the setup script to install all the necessary dependencies:

```bash
# Windows:
setup.sh

# Mac/Linux:
chmod +x setup.sh
./setup.sh
```

This might take a few minutes as it installs all the required software.

## Using the Web Interface

The easiest way to use ProveIt is through its web interface.

### Starting the Web Server

1. In your command prompt or terminal (make sure you're in the proveit directory):
   ```bash
   # Activate the virtual environment
   # Windows:
   venv\Scripts\activate
   
   # Mac/Linux:
   source venv/bin/activate
   
   # Start the web server
   proveit serve
   ```

2. Open your web browser and go to: http://localhost:8000

You should now see the ProveIt web interface!

## Registering Your First File

Let's register a file to establish when you created it.

### Step 1: Prepare Your File

Choose a file you want to register. This could be:
- A document you wrote (DOC, PDF)
- An image you created (JPG, PNG)
- A design or diagram (SVG, AI)
- Any other digital file that represents your intellectual property

Make sure the file is in its final form, as any changes to the file will change its fingerprint.

### Step 2: Register the File

1. In the ProveIt web interface, click on "Register" in the navigation menu
2. You'll see a file upload area - drag your file onto this area or click "Browse Files" to select it
3. Wait while the file is hashed (this creates the unique fingerprint)
4. You'll see the hash displayed - this is the unique identifier for your file
5. (Optional) Add metadata about your file, such as:
   - Title: My Novel Manuscript
   - Author: Your Name
   - Date Created: April 15, 2025
6. Select the network (Polygon is recommended for beginners)
7. Click "Connect Wallet" if your wallet isn't already connected
   - Rabby will pop up asking for permission to connect
   - Click "Connect" to approve
8. Click "Register on Blockchain"
9. Rabby will pop up again showing the transaction details:
   - You'll see the estimated gas fee (usually a small amount)
   - Rabby will show a security check of the transaction
   - Click "Confirm" to proceed with the transaction
10. Wait for the transaction to be processed (usually takes 10-30 seconds on Polygon)
11. Success! You'll see a confirmation screen with your registration details

### Step 3: Save Your Certificate

1. Click "Download Certificate" to save a PDF certificate of your registration
2. This certificate contains:
   - The file hash
   - Your wallet address (proving you registered it)
   - The timestamp (proving when you registered it)
   - The blockchain transaction details
3. Store this certificate safely - it's your proof of registration

## Verifying a File

If you need to prove that a file was registered, or check if someone else's file was registered, you can use the verification feature.

### Verifying Your Own File

1. In the ProveIt web interface, click on "Verify" in the navigation menu
2. Upload the file you want to verify
3. The system will calculate the hash and check if it exists on the blockchain
4. If found, you'll see the registration details:
   - Who registered it (wallet address)
   - When it was registered (timestamp)
   - Any metadata that was included

### Verifying Someone Else's File

If someone sends you a file and claims they registered it:

1. Ask them for the blockchain network they used (e.g., Polygon, Ethereum)
2. Go to the "Verify" page and select that network
3. Upload their file
4. Check if the owner address matches their claimed address
5. Check the timestamp to see when it was registered

## Understanding Your Certificate

The registration certificate contains several important pieces of information:

### File Information
- **Hash**: The unique fingerprint of your file (SHA-256 hash)
- **File Name**: The name of your registered file

### Registration Details
- **Owner Address**: Your wallet address (proves YOU registered it)
- **Registration Date**: The exact date and time of registration
- **Network**: Which blockchain network it's registered on
- **Transaction Hash**: The unique identifier of the blockchain transaction

### Verification
The certificate includes instructions on how others can verify your registration.

## Troubleshooting

### "Transaction Failed" Error

- **Cause**: You might not have enough cryptocurrency for the gas fee
- **Solution**: Add more funds to your wallet

### "File Too Large" Warning

- **Cause**: Very large files (over 100MB) can cause browser performance issues
- **Solution**: Use the command-line interface instead, or compress your file

### Wallet Connection Issues

- **Make sure Rabby is installed**: Check that the extension is visible in your browser
- **Check you're on the right network**: Make sure Rabby is set to the same network you selected in ProveIt
- **Try refreshing the page**: Sometimes a simple refresh fixes connection issues
- **Check Rabby's connection settings**: In Rabby, go to Settings > Connections and make sure the site is allowed

### "Hash Already Registered" Message

- **Cause**: This exact file has already been registered on the blockchain
- **Solution**: Use the "Verify" function to see who registered it and when

### Command Line Not Working

- **Check your installation**: Make sure you ran the setup script successfully
- **Activate the virtual environment**: Make sure you ran the activation command
- **Check your PATH**: Make sure Python and npm are in your system PATH

## Next Steps

Now that you've registered your first file, here are some things you might want to do next:

1. **Register more files**: Build a portfolio of registered intellectual property
2. **Share your certificates**: When sharing your work, include the certificate as proof of creation date
3. **Learn more about blockchain**: Understanding the technology better will help you explain how your proof works
4. **Explore the command-line interface**: For more advanced usage, try the CLI commands

## Getting Help

If you encounter any issues not covered in this tutorial:

- Check the [Troubleshooting](#troubleshooting) section above
- Read the more detailed [Usage Guide](USAGE.md)
- Search for your issue on the project's GitHub page
- Ask for help in the project's discussion forum

Remember, your files never leave your computer - only the hash is stored on the blockchain. This means your intellectual property remains private while still being verifiable.
