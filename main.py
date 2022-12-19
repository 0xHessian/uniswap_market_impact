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
    Reserves in Pool: [41521488.740648, 35211.15755779401]
    Current Pool Price: 0.000848022521006661
    Reversed Pool Price: 1179.2139657009714
    Desired Reverse Price: 1200
    Swap to Acquire Desired Reverse Price: [365447913361.0411, 0]
    '''
    return


if __name__ == '__main__':
    execute()
