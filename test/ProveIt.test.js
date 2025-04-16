const { expect } = require("chai");
const { ethers } = require("hardhat");
const crypto = require("crypto");

describe("ProveIt Contract", function () {
  let ProveIt;
  let proveit;
  let owner;
  let addr1;
  let addr2;

  // Helper function to create a random file hash
  function createRandomHash() {
    return "0x" + crypto.randomBytes(32).toString("hex");
  }

  // Deploy a fresh contract before each test
  beforeEach(async function () {
    // Get contract factory and signers
    ProveIt = await ethers.getContractFactory("ProveIt");
    [owner, addr1, addr2] = await ethers.getSigners();

    // Deploy contract
    proveit = await ProveIt.deploy();
    await proveit.deployed();
  });

  describe("Deployment", function () {
    it("Should deploy successfully", async function () {
      expect(proveit.address).to.be.properAddress;
    });
  });

  describe("Registration", function () {
    it("Should register a new hash", async function () {
      const fileHash = createRandomHash();
      const metadata = "Test file metadata";

      // Register the hash
      await expect(proveit.register(fileHash, metadata))
        .to.emit(proveit, "HashRegistered")
        .withArgs(fileHash, owner.address, await getBlockTimestamp(), metadata);

      // Verify the hash is registered
      const registration = await proveit.verify(fileHash);
      expect(registration.owner).to.equal(owner.address);
      expect(registration.metadata).to.equal(metadata);
    });

    it("Should prevent registering the same hash twice", async function () {
      const fileHash = createRandomHash();
      
      // Register the hash
      await proveit.register(fileHash, "First registration");
      
      // Try to register the same hash again
      await expect(
        proveit.register(fileHash, "Second registration")
      ).to.be.revertedWith("Hash already registered");
    });

    it("Should allow different users to register different hashes", async function () {
      const fileHash1 = createRandomHash();
      const fileHash2 = createRandomHash();
      
      // First user registers a hash
      await proveit.connect(addr1).register(fileHash1, "User 1 file");
      
      // Second user registers a different hash
      await proveit.connect(addr2).register(fileHash2, "User 2 file");
      
      // Verify both registrations
      const registration1 = await proveit.verify(fileHash1);
      const registration2 = await proveit.verify(fileHash2);
      
      expect(registration1.owner).to.equal(addr1.address);
      expect(registration2.owner).to.equal(addr2.address);
    });
  });

  describe("Verification", function () {
    it("Should return empty registration for unregistered hash", async function () {
      const fileHash = createRandomHash();
      
      // Verify an unregistered hash
      const registration = await proveit.verify(fileHash);
      
      expect(registration.owner).to.equal(ethers.constants.AddressZero);
      expect(registration.timestamp).to.equal(0);
      expect(registration.metadata).to.equal("");
    });

    it("Should correctly report if a hash is registered", async function () {
      const fileHash = createRandomHash();
      
      // Initially the hash should not be registered
      expect(await proveit.isRegistered(fileHash)).to.be.false;
      
      // Register the hash
      await proveit.register(fileHash, "Test metadata");
      
      // Now the hash should be registered
      expect(await proveit.isRegistered(fileHash)).to.be.true;
    });
  });

  describe("Helper Functions", function () {
    it("Should return correct owner for a hash", async function () {
      const fileHash = createRandomHash();
      
      // Register the hash
      await proveit.connect(addr1).register(fileHash, "Test metadata");
      
      // Check the owner
      expect(await proveit.getOwner(fileHash)).to.equal(addr1.address);
    });

    it("Should return correct timestamp for a hash", async function () {
      const fileHash = createRandomHash();
      
      // Register the hash
      await proveit.register(fileHash, "Test metadata");
      
      // Get the registration timestamp
      const timestamp = await proveit.getTimestamp(fileHash);
      
      // The timestamp should be recent (within the last minute)
      const now = Math.floor(Date.now() / 1000);
      expect(timestamp).to.be.closeTo(now, 60);
    });

    it("Should return correct metadata for a hash", async function () {
      const fileHash = createRandomHash();
      const metadata = "Detailed test metadata";
      
      // Register the hash
      await proveit.register(fileHash, metadata);
      
      // Check the metadata
      expect(await proveit.getMetadata(fileHash)).to.equal(metadata);
    });
  });

  // Helper function to get the timestamp of the latest block
  async function getBlockTimestamp() {
    const blockNumber = await ethers.provider.getBlockNumber();
    const block = await ethers.provider.getBlock(blockNumber);
    return block.timestamp;
  }
});
