from brownie import Contract
from typing import Union, List
import numpy as np
from .utils import get_swap_amount, get_touch_price, get_amount_out


class UniswapV2Pool():
    def __init__(self, address: str):
        self.address = address
        # NOTE: The following line requires verified contract code on Etherscan, otherwise, you can use `from_abi`
        self.contract = Contract.from_explorer(address=self.address)

        pool_reserves = self.contract.getReserves()
        # Get pool reserves, denote these [X,Y] in all further treatments for ease of notation
        self.reserves = pool_reserves[:2]
        # The block at which we last fetched reserves
        self.reserves_last_updated = pool_reserves[2]

        # TODO: Fetch the pool swap fee dynamically?
        self.fee = 0.997 # 30 basis points

        self.token0 = self.contract.token0()
        # NOTE: The following line requires verified contract code on Etherscan, otherwise, you can use `from_abi`
        self.token0_object = Contract.from_explorer(address=self.token0)
        self.symbol0 = self.token0_object.symbol()
        self.token0_decimals = self.token0_object.decimals()

        self.token1 = self.contract.token1()
        # NOTE: The following line requires verified contract code on Etherscan, otherwise, you can use `from_abi`
        self.token1_object = Contract.from_explorer(address=self.token1)
        self.symbol1 = self.token1_object.symbol()
        self.token1_decimals = self.token1_object.decimals()

        # Get reserves normalised by token decimals
        self.normalised_reserves = [self.reserves[0] / (10**self.token0_decimals), self.reserves[1] / (10**self.token1_decimals)]
        return

    def __str__(self):
        return self.symbol0 + '/' + self.symbol1

    def price(self):
        return get_touch_price(*self.normalised_reserves)

    def reverse_price(self):
        return 1.0 / get_touch_price(*self.normalised_reserves)

    def get_swap_amount(self, desired_price: Union[float, np.float]):
        current_price = self.price()
        return get_swap_amount(desired_price, current_price, self.fee, *self.reserves)

    def update_reserves(self):
        pool_reserves = self.contract.getReserves()
        self.reserves = pool_reserves[:2]
        self.reserves_last_updated = pool_reserves[2]
        self.normalised_reserves = [self.reserves[0] / (10 ** self.token0_decimals), self.reserves[1] / (10 ** self.token1_decimals)]
        return

    def get_amount_out(self, amount_in: list):
        # Note: This function accepts non-normalised inputs
        return get_amount_out(amount_in, self.fee, *self.reserves)
