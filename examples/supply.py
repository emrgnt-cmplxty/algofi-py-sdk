# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.
from algofi.config import ordered_symbols
from algofi.v1.client import TestnetClient
from algofi.v1.supply import prepare_supply_transactions
from algofi.utils import TransactionGroup
from algosdk import mnemonic

# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
sender = {
    'address': 'P4YQ75KCRZT6FF72AF4VZXZ5JDSQA6MVPN5EMCN3H6Z66DK3BRWUO3UQCI',
    'mnemonic': 'noodle learn crack outdoor salon acoustic blind creek panther elegant alone curve surface pair little salute steak above nature cook account chat column above universe', 
}

client = TestnetClient(user_address=sender['address'])
client.init_params()
client.opt_in_all(mnemonic.to_private_key(sender['mnemonic']))

for asset_name in ordered_symbols:
    print("Processing transaction for asset=%s" % (asset_name))
    txn_group = TransactionGroup(prepare_supply_transactions(sender['address'], mnemonic.to_private_key(sender['mnemonic']), client.params, 100, asset_name))
    txn_group.set_keys([sender['address']]*len(txn_group.transactions))
    result = client.submit(txn_group.sign(sign_last_wlogic=False).signed_transactions, wait=True)

#for asset_name in ordered_symbols:
