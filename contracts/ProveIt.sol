// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title ProveIt
 * @dev A simple contract for registering and verifying file hashes on the blockchain
 */
contract ProveIt {
    /**
     * @dev Registration struct to store information about a registered hash
     * @param owner The address that registered the hash
     * @param timestamp The time when the hash was registered
     * @param metadata Optional metadata associated with the hash
     */
    struct Registration {
        address owner;
        uint256 timestamp;
        string metadata;
    }
    
    // Mapping from file hash to registration details
    mapping(bytes32 => Registration) public registrations;
    
    // Event emitted when a new hash is registered
    event HashRegistered(bytes32 indexed hash, address indexed owner, uint256 timestamp, string metadata);
    
    /**
     * @dev Register a new file hash
     * @param fileHash The SHA-256 hash of the file
     * @param metadata Optional metadata about the file (e.g., title, description)
     */
    function register(bytes32 fileHash, string calldata metadata) external {
        // Ensure the hash hasn't been registered before
        require(registrations[fileHash].owner == address(0), "Hash already registered");
        
        // Store the registration details
        registrations[fileHash] = Registration({
            owner: msg.sender,
            timestamp: block.timestamp,
            metadata: metadata
        });
        
        // Emit an event for off-chain tracking
        emit HashRegistered(fileHash, msg.sender, block.timestamp, metadata);
    }
    
    /**
     * @dev Verify a file hash and retrieve its registration details
     * @param fileHash The SHA-256 hash of the file to verify
     * @return Registration details if the hash is registered, or a struct with address(0) if not
     */
    function verify(bytes32 fileHash) external view returns (Registration memory) {
        return registrations[fileHash];
    }
    
    /**
     * @dev Check if a hash is registered
     * @param fileHash The SHA-256 hash to check
     * @return bool True if the hash is registered, false otherwise
     */
    function isRegistered(bytes32 fileHash) external view returns (bool) {
        return registrations[fileHash].owner != address(0);
    }
    
    /**
     * @dev Get the owner of a registered hash
     * @param fileHash The SHA-256 hash to check
     * @return address The owner's address, or address(0) if not registered
     */
    function getOwner(bytes32 fileHash) external view returns (address) {
        return registrations[fileHash].owner;
    }
    
    /**
     * @dev Get the registration timestamp of a hash
     * @param fileHash The SHA-256 hash to check
     * @return uint256 The timestamp, or 0 if not registered
     */
    function getTimestamp(bytes32 fileHash) external view returns (uint256) {
        return registrations[fileHash].timestamp;
    }
    
    /**
     * @dev Get the metadata of a registered hash
     * @param fileHash The SHA-256 hash to check
     * @return string The metadata, or empty string if not registered
     */
    function getMetadata(bytes32 fileHash) external view returns (string memory) {
        return registrations[fileHash].metadata;
    }
}
