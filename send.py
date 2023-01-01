# Import required libraries
import binascii
import web3
from hexbytes import HexBytes

# Set the Binance Smart Chain endpoint URL
w3 = web3.Web3(web3.Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

# Set the contract address and function data
contract_address = HexBytes(0x22f77fb41fd0d2a4ea99f2719d1180afc2a74484)
# Change data for you new unstake transaction
data = HexBytes(0x2e17de7800000000000000000000000000000000000000000000005150ae84a8cdf00000)

# Load the private keys from a file
with open("private_keys.txt", "r") as f:
    private_keys = f.readlines()

# Initialize the counter variables
completed_count = 0
failed_count = 0

# Iterate over the private keys and send a transaction for each one
for private_key in private_keys:
    # Convert the private key to bytes
    private_key_bytes = binascii.unhexlify(private_key.strip())

    # Get the account address associated with the private key
    address = w3.eth.account.privateKeyToAccount(private_key_bytes).address

    # Get the nonce for the account
    nonce = w3.eth.getTransactionCount(address)

    # Set the transaction parameters
    tx_params = {
        "nonce": nonce,
        "gasPrice": w3.eth.gasPrice,
        #Approve - 50000
        #Unstake - 500000
        #Stake - 500000
        "gas": 500000,
        "to": contract_address,
        "value": 0,
        "data": data
    }

    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx_params, private_key_bytes)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Check the transaction status
    if tx_receipt["status"] == 1:
        # Transaction was successful
        completed_count += 1
        print(f"Completed: {tx_hash.hex()}")
    else:
        # Transaction failed
        failed_count += 1
        print(f"Failed: {tx_hash.hex()}")

# Print the results
print(f"Total transactions: {len(private_keys)}")
print(f"Completed: {completed_count}")
print(f"Failed: {failed_count}")
