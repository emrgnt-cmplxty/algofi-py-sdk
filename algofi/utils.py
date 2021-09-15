from base64 import decodebytes, b64decode, b64encode
from algosdk.future.transaction import AssetTransferTxn, ApplicationOptInTxn, LogicSig, LogicSigTransaction, assign_group_id, calculate_group_id
from algosdk.error import AlgodHTTPError


#   Utility function used to create opt-in asset transaction
def opt_in_user_to_asset(sender_addr, sender_key, params, asset_id):
    # declare sender
    txn = AssetTransferTxn(sender=sender_addr, sp=params, receiver=sender_addr, amt=0, index=asset_id)
    return txn.sign(sender_key)


#   Utility function used to create opt-in appl transaction
def opt_in_user_to_app(sender_addr, sender_key, params, app_id):
    # declare sender
    # create unsigned transaction
    txn = ApplicationOptInTxn(sender_addr, params, app_id)
    # sign transaction
    return txn.sign(sender_key) 


def get_program(definition, variables=None):
    """
    Return a byte array to be used in LogicSig.
    """
    template = definition['bytecode']
    template_bytes = list(b64decode(template))

    offset = 0
    for v in sorted(definition['variables'], key=lambda v: v['index']):
        name = v['name'].split('TMPL_')[-1].lower()
        value = variables[name]
        start = v['index'] - offset
        end = start + v['length']
        value_encoded = encode_value(value, v['type'])
        value_encoded_len = len(value_encoded)
        diff = v['length'] - value_encoded_len
        offset += diff
        template_bytes[start:end] = list(value_encoded)

    return bytes(template_bytes)


def encode_value(value, type):
    if type == 'int':
        return encode_varint(value)
    raise Exception('Unsupported value type %s!' % type)


def encode_varint(number):
    buf = b''
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buf += bytes([towrite | 0x80])
        else:
            buf += bytes([towrite])
            break
    return buf


def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        try:
            formatted_key = b64decode(key).decode('utf-8')
        except:
            formatted_key = key
        formatted[formatted_key] = value['uint']
    return formatted


def logic_sign(txn, program):
    t = program.encode()
    program_encoded = decodebytes(t)
    lsig = LogicSig(program_encoded)
    return LogicSigTransaction(txn, lsig)

# read user local state
def read_local_state(algod, user_address, app_id):
    results = algod.account_info(user_address)
    for local_state in results['apps-local-state']:
        if local_state['id'] == app_id:
            if 'key-value' not in local_state:
                return {}
            return format_state(local_state['key-value'])
    return {}

# read app global state
def read_global_state(algod, creator_address, app_id):
    results = algod.account_info(creator_address)
    apps_created = results['created-apps']
    for app in apps_created:
        if app['id'] == app_id:
            return format_state(app['params']['global-state'])
    return {}


def sign_and_submit_transactions(client, transactions, signed_transactions, sender, sender_sk):
    for i, txn in enumerate(transactions):
        if txn.sender == sender:
            signed_transactions[i] = txn.sign(sender_sk)
    
    txid = client.send_transactions(signed_transactions)
    return wait_for_confirmation(client, txid)


def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    txinfo['txid'] = txid
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


def int_to_bytes(num):
    return num.to_bytes(8, 'big')


def get_state_int(state, key):
    if type(key) == str:
        key = b64encode(key.encode())
    return state.get(key.decode(), {'uint': 0})['uint']


def get_state_bytes(state, key):
    if type(key) == str:
        key = b64encode(key.encode())
    return state.get(key.decode(), {'bytes': ''})['bytes']


class TransactionGroup:
    def __init__(self, transactions):
        self.transactions = transactions
        self.signed_transactions = [None for _ in self.transactions]

    def set_transaction_keys(self, keys):
        self.keys = keys

    def sign(self, sign_last_wlogic=False):
        stxn_group = []
        gid = calculate_group_id(self.transactions)
        for txn, key in zip(self.transactions, self.keys):
            txn.group = gid
            if txn != self.transactions[-1]:
                stxn_group.append(txn.sign(key))
            else:
                if (sign_last_wlogic):
                    stxn_group.append(logic_sign(txn, key))
                else:
                    stxn_group.append(txn.sign(key))
        self.signed_transactions = stxn_group
