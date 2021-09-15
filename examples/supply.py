# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.
from algofi.config import ordered_symbols, decimals, scale
from algofi.v1.client import TestnetClient
from algofi.v1.supply import prepare_supply_transactions
from algofi.utils import TransactionGroup
from algosdk import mnemonic

# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
sender = {
    'address': 'YOUR_ADDRESS',
    'mnemonic': 'YOUR_MNEOMNIC'
}

client = TestnetClient(user_address=sender['address'])
client.init_params()
client.opt_in_all(mnemonic.to_private_key(sender['mnemonic']))

print("~"*100)
print("Global contract states before calling supply")
print("~"*100)
init_global_state = client.get_global_states()
for asset_name in ordered_symbols:
    print("Printing global state for asset = ", asset_name)
    print('underlying_cash=', init_global_state[asset_name]['underlying_cash']/decimals[asset_name])
    print('underlying_borrowed=', init_global_state[asset_name]['underlying_borrowed']/decimals[asset_name])
    print('total_borrow_interest_rate=', init_global_state[asset_name]['total_borrow_interest_rate']/scale)
    print("~"*100)

print("~"*100)
print("Processing supply transactions for all assets")
print("~"*100)
for asset_name in ordered_symbols:
    print("Processing transaction for asset = %s" % (asset_name))
    txn_group = TransactionGroup(prepare_supply_transactions(sender['address'], mnemonic.to_private_key(sender['mnemonic']), client.params, 100*decimals[asset_name], asset_name))
    txn_group.set_transaction_keys([mnemonic.to_private_key(sender['mnemonic'])]*len(txn_group.transactions))
    txn_group.sign(sign_last_wlogic=False)
    result = client.submit(txn_group.signed_transactions, wait=True)

print("~"*100)
print("Global contract states after calling supply")
print("~"*100)
final_global_state = client.get_global_states()
for asset_name in ordered_symbols:
    print("Printing global state for asset = ", asset_name)
    print('underlying_cash=', final_global_state[asset_name]['underlying_cash']/decimals[asset_name])
    print('underlying_borrowed=', final_global_state[asset_name]['underlying_borrowed']/decimals[asset_name])
    print('total_borrow_interest_rate=', final_global_state[asset_name]['total_borrow_interest_rate']/scale)
    print("~"*100)

print("~"*100)
print("User local states after calling supply")
print("~"*100)
final_user_state = client.get_user_state()
for asset_name in ordered_symbols:
    print("Printing global state for asset = ", asset_name)
    print('user_bank_minted=', final_user_state[asset_name]['user_bank_minted']/decimals[asset_name])
    print('user_bank_pending_claim=', final_user_state[asset_name]['user_bank_pending_mint']/decimals[asset_name])
    print("~"*100)
