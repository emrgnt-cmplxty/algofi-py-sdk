from config import manager_id, storage_ids, oracle_ids, ordered_symbols

def get_init_txns(sender_addr, params, account=None):
    txn0 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                            [b'update_prices'], foreign_apps=[oracle_ids[symbol] for symbol in ordered_symbols])

    txn1 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                            [b'update_exchange_rate'], foreign_apps=[storage_ids[symbol] for symbol in ordered_symbols])
    if (account):
        txn2 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                                [b'update_collateral_value'], 
                                                foreign_apps=[storage_ids[symbol] for symbol in ordered_symbols],
                                                accounts=[account])
        txn3 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                                [b'update_borrow_value'], 
                                                foreign_apps=[storage_ids[symbol] for symbol in ordered_symbols],
                                                accounts=[account])
    else:
        txn2 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                                [b'update_collateral_value'], 
                                                foreign_apps=[storage_ids[symbol] for symbol in ordered_symbols])
        txn3 = transaction.ApplicationNoOpTxn(sender_addr, params, manager_id, 
                                                [b'update_borrow_value'], 
                                                foreign_apps=[storage_ids[symbol] for symbol in ordered_symbols])
    return [txn0, txn1, txn2, txn3]