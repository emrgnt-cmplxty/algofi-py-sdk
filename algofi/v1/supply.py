import base64
from os import name
import algosdk
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn, AssetTransferTxn
from .prepend import get_init_txns
from algofi.utils import package_all_tx
from algofi.config import manager_id, escrow_hash, storage_ids

def prepare_supply_transactions(sender_addr, sender_key, params, amt, asset_name):
    (txn0, txn1, txn2, txn3) = get_init_txns(sender_addr, params)
    txn4 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, [b'mint'])
    
    txn5 = transaction.ApplicationNoOpTxn(sender_addr, params, storage_ids[asset_name], [], foreign_apps=[manager])
    txn6 = AssetTransferTxn(sender=sender_addr, sp=params, receiver=escrow_hash, 
                                                        amt=amt, index=assets[asset_name])
    stxn_group = package_all_tx([txn0, txn1, txn2, txn3, txn4, txn5, txn6], [sender_key]*7, sign_last_wlogic=False)
    return stxn_group