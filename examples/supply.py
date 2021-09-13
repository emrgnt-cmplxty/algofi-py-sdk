# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.

from algofi.v1.client import TestnetClient
from algofi.v1.supply import prepare_supply_transactions

# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
sender = {
    'address': 'GI2W32BVKTSKOWSXFQXKQZBKMTLDLFI2KST7BJ7YZWDZL2PM6TGCGBTLGI',
    'private_key': 'hamster size staff top reject clap ivory matrix vintage trip south current transfer upper lemon all toe fade again sweet south rely horse about giraffe', # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}

client = TestnetClient(user_address=account['address'])
client.init_params()

asset_name = "USDC"
transaction_group = prepare_supply_transactions(sender['address'], sender['private_key'], client.params, 100, asset_name)



# By default all subsequent operations are on behalf of user_address

'''
# Fetch our two assets of interest
TINYUSDC = client.fetch_asset(21582668)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(TINYUSDC, ALGO)

# Get a quote for supplying 1000.0 TinyUSDC
quote = pool.fetch_mint_quote(TINYUSDC(1000_000_000), slippage=0.01)

print(quote)

# Check if we are happy with the quote..
if quote.amounts_in[ALGO] < 5_000_000:
    # Prepare the mint transactions from the quote and sign them
    transaction_group = pool.prepare_mint_transactions_from_quote(quote)
    transaction_group.sign_with_private_key(account['address'], account['private_key'])
    result = client.submit(transaction_group, wait=True)

    # Check if any excess liquidity asset remaining after the mint
    excess = pool.fetch_excess_amounts()
    if pool.liquidity_asset in excess:
        amount = excess[pool.liquidity_asset]
        print(f'Excess: {amount}')
        if amount > 1_000_000:
            transaction_group = pool.prepare_redeem_transactions(amount)
            transaction_group.sign_with_private_key(account['address'], account['private_key'])
            result = client.submit(transaction_group, wait=True)

info = pool.fetch_pool_position()
share = info['share'] * 100
print(f'Pool Tokens: {info[pool.liquidity_asset]}')
print(f'Assets: {info[TINYUSDC]}, {info[ALGO]}')
print(f'Share of pool: {share:.3f}%')
'''