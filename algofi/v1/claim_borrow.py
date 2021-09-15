import base64
from os import name
import algosdk
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn, AssetTransferTxn
from .prepend import get_init_txns
from algofi.config import assets, manager_id, escrow_hashes, storage_ids

def prepare_claim_borrow_transactions(sender_addr, sender_key, params, amt, asset_name):
    (txn0, txn1, txn2, txn3) = get_init_txns(sender_addr, params)
    txn4 = ApplicationNoOpTxn(sender_addr, params, manager_id, [b'claim_borrow'])
    txn5 = ApplicationNoOpTxn(sender_addr, params, storage_ids[asset_name], [], foreign_apps=[manager_id])
    txn6 = AssetTransferTxn(sender=escrow_hashes[asset_name], sp=params, receiver=sender_addr, amt=amt, index=assets[asset_name])
    return [txn0, txn1, txn2, txn3, txn4, txn5, txn6]