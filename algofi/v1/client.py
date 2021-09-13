import json
from base64 import b64decode
from algosdk.v2client.algod import AlgodClient
from algosdk.error import AlgodHTTPError
from algosdk.encoding import encode_address
from algofi.utils import opt_in_user_to_app, opt_in_user_to_asset, wait_for_confirmation
from algofi.assets import Asset, AssetAmount
from algofi.config import ordered_symbols, assets, manager_id, storage_ids
from .optin import prepare_app_optin_transactions
from .constants import TESTNET_VALIDATOR_APP_ID, MAINNET_VALIDATOR_APP_ID

class Client:
    def __init__(self, algod_client: AlgodClient, validator_app_id: int, user_address=None):
        self.algod = algod_client
        self.validator_app_id = validator_app_id
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

    def submit(self, transaction_group, wait=False):
        try:
            txid = self.algod.send_transactions(transaction_group)
        except AlgodHTTPError as e:
            raise Exception(json.loads(e.args[0])['message']) from None
        if wait:
            return wait_for_confirmation(self.algod, txid)
        return {'txid': txid}

    def prepare_app_optin_transactions(self, user_address=None):
        user_address = user_address or self.user_address
        suggested_params = self.algod.suggested_params()
        txn_group = prepare_app_optin_transactions(
            validator_app_id=self.validator_app_id,
            sender=user_address,
            suggested_params=suggested_params,
        )
        return txn_group
    
    def is_opted_in(self, user_address=None):
        user_address = user_address or self.user_address
        account_info = self.algod.account_info(user_address)
        for a in account_info['apps-local-state']:
            if a['id'] == self.validator_app_id:
                return True
        return False

class TestnetClient(Client):
    def __init__(self, algod_client=None, user_address=None):
        if algod_client is None:
            algod_client = AlgodClient('', 'https://api.testnet.algoexplorer.io', headers={'User-Agent': 'algosdk'})
        super().__init__(algod_client, validator_app_id=TESTNET_VALIDATOR_APP_ID, user_address=user_address)

class MainnetClient(Client):
    def __init__(self, algod_client=None, user_address=None):
        raise Exception('Not on mainnet yet!')
        if algod_client is None:
            algod_client = AlgodClient('', 'https://api.algoexplorer.io', headers={'User-Agent': 'algosdk'})
        super().__init__(algod_client, validator_app_id=MAINNET_VALIDATOR_APP_ID, user_address=user_address)

