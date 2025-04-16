// Script to deploy the ProveIt contract
const fs = require('fs');
const path = require('path');
const hre = require("hardhat");

async function main() {
  console.log("Deploying ProveIt contract...");

  // Get the contract factory
  const ProveIt = await hre.ethers.getContractFactory("ProveIt");
  
  // Deploy the contract
  const proveit = await ProveIt.deploy();
  
  // Wait for deployment to complete
  await proveit.deployed();
  
  // Get the network name
  const networkName = hre.network.name;
  
  console.log(`ProveIt contract deployed to: ${proveit.address} on network: ${networkName}`);
  
  // Save deployment information
  saveDeploymentInfo(networkName, {
    address: proveit.address,
    deployer: (await hre.ethers.getSigners())[0].address,
    deploymentTime: new Date().toISOString(),
    networkName: networkName
  });
  
  // Wait for a few blocks for Etherscan to index the contract
  if (networkName !== "localhost" && networkName !== "hardhat") {
    console.log("Waiting for Etherscan to index the contract...");
    await new Promise(resolve => setTimeout(resolve, 60000)); // 60 seconds
    
    // Verify the contract on Etherscan
    try {
      console.log("Verifying contract on Etherscan...");
      await hre.run("verify:verify", {
        address: proveit.address,
        constructorArguments: []
      });
      console.log("Contract verified on Etherscan");
    } catch (error) {
      console.error("Error verifying contract on Etherscan:", error);
    }
  }
}

function saveDeploymentInfo(networkName, deploymentInfo) {
  // Create deployments directory if it doesn't exist
  const deploymentsDir = path.join(__dirname, '../deployments');
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir);
  }
  
  // Create network directory if it doesn't exist
  const networkDir = path.join(deploymentsDir, networkName);
  if (!fs.existsSync(networkDir)) {
    fs.mkdirSync(networkDir);
  }
  
  // Save deployment info to JSON file
  const deploymentPath = path.join(networkDir, 'ProveIt.json');
  fs.writeFileSync(
    deploymentPath,
    JSON.stringify(deploymentInfo, null, 2)
  );
  
  console.log(`Deployment information saved to: ${deploymentPath}`);
}

// Execute the deployment
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
