import json
from base64 import b64decode
from algosdk.v2client.algod import AlgodClient
from algosdk.error import AlgodHTTPError
from algosdk.encoding import encode_address
from algofi.utils import opt_in_user_to_app, opt_in_user_to_asset, read_local_state, read_global_state, wait_for_confirmation
from algofi.assets import Asset, AssetAmount
from algofi.config import assets, creator_address, ordered_symbols, manager_id, storage_ids

class Client:
    def __init__(self, algod_client: AlgodClient, user_address=None):
        self.algod = algod_client
        self.assets_cache = {}
        self.user_address = user_address
    
    def init_params(self):
        params = self.algod.suggested_params()
        params.flat_fee = True
        params.fee = 1000
        self.params = params

    def opt_in_all(self, sender_key):
        n_apps = 0
        n_assets = 0
        for symbol in ordered_symbols:
            try:
                stxn_assets = opt_in_user_to_asset(self.user_address, sender_key, self.params, assets[symbol])
                txn = self.algod.send_transactions([stxn_assets])
                n_assets = n_assets + 1
            except:
                pass
            try:               
                stxn_bank_assets = opt_in_user_to_asset(self.user_address, sender_key, self.params, assets['b'+symbol])
                txn = self.algod.send_transactions([stxn_bank_assets])
                n_assets = n_assets + 1
            except:
                pass
            try:               
                stxn = opt_in_user_to_app(self.user_address, sender_key, self.params, storage_ids[symbol])
                txn = self.algod.send_transactions([stxn])
                n_apps = n_apps + 1
            except:
                pass
        try:               
            stxn = opt_in_user_to_app(self.user_address, sender_key, self.params, manager_id)
            txn = send_and_wait(self.algod, [stxn])
            n_apps = n_apps + 1
        except:
            pass

    def get_user_state(self):
        init = {"manager" : read_local_state(self.algod, self.user_address, manager_id)}
        for asset_name in ordered_symbols:
            init = {asset_name : read_local_state(self.algod, self.user_address, storage_ids[asset_name])}
        return init

    def get_global_states(self):
        init = {"manager" : read_global_state(self.algod, creator_address, manager_id)}
        for asset_name in ordered_symbols:
            init = {asset_name : read_global_state(self.algod, creator_address, storage_ids[asset_name])}
        return init

    def submit(self, transaction_group, wait=False):
        try:
            txid = self.algod.send_transactions(transaction_group)
        except AlgodHTTPError as e:
            raise Exception(json.loads(e.args[0])['message']) from None
        if wait:
            return wait_for_confirmation(self.algod, txid)
        return {'txid': txid}

    
class TestnetClient(Client):
    def __init__(self, algod_client=None, user_address=None):
        if algod_client is None:
            algod_client = AlgodClient('', 'https://api.testnet.algoexplorer.io', headers={'User-Agent': 'algosdk'})
        super().__init__(algod_client, user_address=user_address)

class MainnetClient(Client):
    def __init__(self, algod_client=None, user_address=None):
        raise Exception('Not on mainnet yet!')
        if algod_client is None:
            algod_client = AlgodClient('', 'https://api.algoexplorer.io', headers={'User-Agent': 'algosdk'})
        super().__init__(algod_client, user_address=user_address)

