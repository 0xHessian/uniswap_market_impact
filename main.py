from brownie import network
import os
import dotenv

from src.uniswap import UniswapV2Pool

# Load environment variables
dotenv.load_dotenv()


def execute():
    network.connect('mainnet')

    pool = UniswapV2Pool(os.environ['POOL'])

    print(f'''Pool Name: {str(pool)}\nReserves in Pool: {pool.normalised_reserves}\nCurrent Pool Price: {pool.price()}\nReversed Pool Price: {pool.reverse_price()}''')

    desired_reverse_price = 1200
    desired_price = 1.0 / desired_reverse_price

    print(f'''Desired Reverse Price: {desired_reverse_price}\nSwap to Acquire Desired Reverse Price: {pool.get_swap_amount(desired_price)}''')

    '''
    Pool Name: USDC/WETH
    Reserves in Pool: [41604502.976621, 35136.776561843944]
    Current Pool Price: 0.0008445426347621195
    Reversed Pool Price: 1184.0728446843514
    Desired Reverse Price: 1200
    Swap to Acquire Desired Reverse Price: [279718.92399491987, 0]
    '''
    return


if __name__ == '__main__':
    execute()
