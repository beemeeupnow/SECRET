"""
SAFE Execution Cost Reimbursement Estimation Tool

Calculate amount spent per signer for transaction execution to simplify reimbursements for shared multi-sigs.

# NOTE: Safe Transaction Service was shut down after recent events, and it took too long to sync a local instance.
# This greatly hindered progress, but it was good to learn how to run the service locally.
"""
import argparse
import decimal
import safe_eth.eth
import safe_eth.safe
import safe_eth.safe.api


if __name__ == "__main__":
    """
    future GUI could allow:
    * specify RPC URL
    * specify SAFE address
    * specify network (drop-down of supported ones)
    * transaction service API base URL (override automatic one that is based on network)
    * mark transaction with ETH send as *not* reimbursement
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--address", type=str, required=True, help="SAFE ethereum address")
    arg_parser.add_argument("--decimals", type=int, default=18, help="native asset decimals")
    arg_parser.add_argument("--network", type=int, default=1, help="network/chain ID")
    arg_parser.add_argument("--rpc", type=str, default="https://eth.llamarpc.com", help="JSON RPC URL")
    arg_parser.add_argument("--txapi", type=str, default="", help="SAFE Transaction Service API URL")

    args = arg_parser.parse_args()

    # set precision for native asset (e.g. ETH)
    decimal.getcontext().prec = args.decimals

    # set up API connections
    ethereum_client = safe_eth.eth.EthereumClient(args.rpc)
    safe = safe_eth.safe.Safe(args.address, ethereum_client)
    network = args.network
    transaction_service_api = safe_eth.safe.api.TransactionServiceApi(network, base_url=args.txapi or None)

    # collect transaction information for the provided SAFE address
    transactions = transaction_service_api.get_transactions(args.address)

    # add up amounts for spent gas and reimbursements
    gas_spent_per_address = {}
    gas_reimbursed_per_address = {}

    for tx in transactions:
        if tx["isExecuted"] is False:
            continue

        gas_spent_per_address.setdefault(tx["executor"], decimal.Decimal(0))

        # TODO: get gas fee for transaction, add to counter
        # TODO: check if ETH was sent to any address that previously executed transactions and store the amount

    # TODO: subtract reimbursements from spent amounts to determine remaining amount to reimburse
