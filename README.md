# algofi-py-sdk
Algofi Python SDK


## Design Goal
This SDK is useful for developers who wish to create automated trading programs/bots for the Algofi platform. 

## Status
This SDK is currently under active early development and should not be considered stable.

## Installation
algofi-py-sdk is not yet released on PYPI. It can be installed directly from this repository with pip:

`pip install git+https://github.com/owen-colegrove/algofi-py-sdk.git`


## Sneak Preview

```python
from algofi.v1.client import TinymanTestnetClient
from algofi.config import ordered_symbols, decimals, scale

client = TestnetClient()

# loop over all assets on platform
for asset_name in ordered_symbols:
    print("Processing transaction for asset = %s" % (asset_name))
    # prepare_mint_transactions returns a transaction block which adds liquidity to the platform
    txn_group = TransactionGroup(prepare_mint_transactions(sender['address'], mnemonic.to_private_key(sender['mnemonic']), client.params, 100*decimals[asset_name], asset_name))
    txn_group.set_transaction_keys([mnemonic.to_private_key(sender['mnemonic'])]*len(txn_group.transactions))
    txn_group.sign(sign_last_wlogic=False)
    result = client.submit(txn_group.signed_transactions, wait=True)


```

## Examples

### Add Liquidity (mint)
[mint.py](examples/mint.py)
This example shows how to add liquidity to the platform


### Claim bank asset (claim_mint)
[claim_mint.py](examples/claim_mint.py)
This example shows how to claim bank assets that are created in minting process

### Burn asset (burn)
[burn.py](examples/burn.py)
This example shows how to burn bank assets to redeem for underlying liquidity

### Claim underlying asset (claim_burn)
[claim_burn.py](examples/claim_burn.py)
This example shows how to claim underlying assets the user has earned from burning

### Add collateral (add_collateral)
[add_collateral.py](examples/add_collateral.py)
This example shows how to add bank assets as collateral to the platform

### Remove collateral (remove_collateral)
[remove_collateral.py](examples/remove_collateral.py)
This example shows how to remove bank assets that were added as collateral

### Borrow (claim_borrow)
[claim_borrow.py](examples/claim_borrow.py)
This example shows how to borrow an underlying asset against provided collateral

### Repay Borrow (repay_borrow)
[repay_borrow.py](examples/repay_borrow.py)
This example shows how to repay borrowed collateral


# License

algofi-py-sdk is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.
