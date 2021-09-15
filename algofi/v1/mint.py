import base64
from os import name
import algosdk
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn, AssetTransferTxn
from .prepend import get_init_txns
from algofi.config import assets, manager_id, escrow_hashes, storage_ids

def prepare_mint_transactions(sender_addr, sender_key, params, amt, asset_name):
    (txn0, txn1, txn2, txn3) = get_init_txns(sender_addr, params)
    txn4 = ApplicationNoOpTxn(sender_addr, params, manager_id, [b'mint'])
    txn5 = ApplicationNoOpTxn(sender_addr, params, storage_ids[asset_name], [], foreign_apps=[manager_id])
    txn6 = AssetTransferTxn(sender=sender_addr, sp=params, receiver=escrow_hashes[asset_name], amt=amt, index=assets[asset_name])
    return [txn0, txn1, txn2, txn3, txn4, txn5, txn6]