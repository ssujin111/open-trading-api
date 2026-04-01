import argparse
from config import Config
from api_client import APIClient
from auth import Auth
from market_data import MarketData
from account import Account
from orders import Orders
from trader import Trader
from logger import logger

def main():
    parser = argparse.ArgumentParser(description='Samsung Auto Trader')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no real API calls)')
    parser.add_argument('--cycle', action='store_true', help='Run a single cycle instead of loop')
    args = parser.parse_args()

    config = Config()
    if not args.test:
        config.validate()

    api_client = APIClient(config.base_url, config.appkey, config.appsecret)
    auth = Auth(config, api_client)
    market_data = MarketData(api_client, auth)
    account = Account(api_client, auth, config.cano, config.acnt_prdt_cd)
    orders = Orders(api_client, auth, config.cano, config.acnt_prdt_cd)
    trader = Trader(market_data, account, orders, test_mode=args.test)

    if args.cycle:
        trader.run_cycle()
    else:
        trader.run()

if __name__ == '__main__':
    main()