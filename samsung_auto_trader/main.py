import argparse

from api_client import APIClient
from auth import Auth
from config import Config
from account import Account
from market_data import MarketData
from orders import Orders
from trader import Trader
from datetime import datetime
from zoneinfo import ZoneInfo


def main() -> None:
    print('Samsung Auto Trader starting...')
    # Always print current KST time on startup
    try:
        print(f'Current KST time: {datetime.now(ZoneInfo("Asia/Seoul"))}')
    except Exception:
        print('Current KST time: unavailable')

    parser = argparse.ArgumentParser(description='Samsung Auto Trader')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no real API calls)')
    parser.add_argument('--cycle', action='store_true', help='Run a single cycle instead of continuous loop')
    args = parser.parse_args()

    print(f'Arguments: --test={args.test} --cycle={args.cycle}')

    config = Config()
    print('Loaded configuration from environment and .env')
    if not args.test:
        print('Validating required API credentials...')
        try:
            config.validate()
            print('Credential validation passed')
        except Exception as e:
            print(f'Exiting: credential validation failed: {type(e).__name__}: {e}')
            return
    else:
        print('Test mode enabled; skipping credential validation')

    api_client = APIClient(config.base_url, config.appkey, config.appsecret)
    print(f'API client initialized for base URL: {config.base_url}')
    auth = Auth(config, api_client)
    market_data = MarketData(api_client, auth)
    account = Account(api_client, auth, config.cano, config.acnt_prdt_cd)
    orders = Orders(api_client, auth, config.cano, config.acnt_prdt_cd)
    trader = Trader(market_data, account, orders, test_mode=args.test)

    print('Trader instance created')
    if args.cycle:
        print('Running single cycle (cycle mode)')
        try:
            trader.run_cycle()
        except Exception as e:
            print(f'Error during run_cycle: {type(e).__name__}: {e}')
    else:
        print('Running trader loop (run mode)')
        try:
            trader.run()
        except Exception as e:
            print(f'Error during run: {type(e).__name__}: {e}')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Top-level catch to ensure any unexpected error is printed before exit
        print(f'Fatal error: {type(e).__name__}: {e}')
        raise
