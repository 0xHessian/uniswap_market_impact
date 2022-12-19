## uniswap_market_impact

Some scripts to calculate the swap quantities required for a specific amount of price impact in a Uniswap V2 pool.

See `README.pdf` for an explanation of the calculations required.

See `main.py` for an example calculation.

Note, this repository requires a `.env` file of the format:

```
POOL = 'UNISWAP_V2_POOL_ON_ETHEREUM'
ETHERSCAN_TOKEN = 'ETHERSCAN_API_KEY'
```

Unit tests for this library can be run using `python -m pytest tests`. 

These unit tests require a local fork of the Ethereum network, which can be configured as follows:

```
development:
- cmd: ganache-cli
  cmd_settings:
    accounts: 10
    fork: https://eth-mainnet.g.alchemy.com/v2/[ALCHEMY-API-KEY]
    mnemonic: brownie
    port: 8545
  host: http://127.0.0.1
  id: uniswap-market-impact2
  explorer: https://api.etherscan.io/api
  name: uniswap-market-impact2
 ```