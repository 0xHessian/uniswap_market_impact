from typing import Union
import numpy as np


def get_touch_price(X: Union[int, np.int], Y: Union[int, np.int]):
    '''
    Given reserves of a Uniswap V2 pool (X,Y), get the "touch price" of the pool, defined as the instantaneous price,
    ie. the price for a swap of 1 unit of X -> Y in the order X/Y.

    For the price of Y in terms of X, take the reciprocal.

    The pool quotes according to the invariant XY = k, so we require |dY/dX| = |-Y/X| = Y/X.
    '''
    return np.double(Y/X)


def get_swap_amount(desired_price, current_price, fee, X, Y):
    if desired_price < current_price:
        # We need to sell units of X into the pool
        deltaX = X * (np.sqrt(current_price / desired_price) - 1) / fee
        return [deltaX, np.int(0)]
    else:
        # We need to sell units of Y into the pool
        deltaY = Y * (np.sqrt(desired_price / current_price) - 1) / fee
        return [np.int(0), deltaY]
