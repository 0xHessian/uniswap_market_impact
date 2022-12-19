import pytest
from brownie import Contract, network, accounts, chain
import dotenv
import numpy as np
import os

from src.uniswap import UniswapV2Pool


@pytest.fixture(scope="session")
def network_config():
    dotenv.load_dotenv()
    network.connect('uniswap-market-impact2')
    yield 1


@pytest.fixture(scope="session")
def pool(network_config):
    yield UniswapV2Pool(os.environ['POOL'])


@pytest.fixture(scope="session")
def router(network_config):
    router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
    yield Contract.from_explorer(router)


def test_get_swap_amount(network_config, pool, router):
    reserves = pool.reserves
    pool_price = pool.price()

    # Simulate a 0.5% price impact
    desired_price = 1.005 * pool_price

    swap_amounts = pool.get_swap_amount(desired_price)

    amounts_out = pool.get_amount_out(swap_amounts)

    amount_in, amount_out = swap_amounts[1], amounts_out[0]

    # For other pools, you may need to call a different function on the router
    router.swapETHForExactTokens(int(amount_out), [pool.token1, pool.token0], accounts[0].address, chain.time() + 15, {'from': accounts[0], 'value': int(amount_in)})

    pool.update_reserves()
    new_price = pool.price()
    new_reserves = pool.reserves

    # Prices must be identical to 6 decimal places
    assert np.absolute(new_price - desired_price) <= 1e-6

    expected_reserves = (reserves[0] - amount_out, reserves[1] + amount_in)

    # Reserves must be identical to 6 decimal places
    assert np.absolute(expected_reserves[0] - new_reserves[0]) <= 1e-6 * (10 ** pool.token0_decimals)
    assert np.absolute(expected_reserves[1] - new_reserves[1]) <= 1e-6 * (10 ** pool.token1_decimals)

    return
