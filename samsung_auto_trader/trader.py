from datetime import datetime, time
from zoneinfo import ZoneInfo
import time as time_module
from typing import Dict

from account import Account
from logger import logger
from market_data import MarketData
from orders import Orders


class Trader:
    def __init__(self, market_data: MarketData, account: Account, orders: Orders, test_mode: bool = False):
        self.market_data = market_data
        self.account = account
        self.orders = orders
        self.symbol = '005930'
        self.offset = 2000  # KRW
        self.quantity = 1
        self.poll_interval_seconds = 300
        self.test_mode = test_mode

    @staticmethod
    def _trading_window_times() -> tuple[time, time]:
        return time(9, 10), time(15, 30)

    def is_trading_window(self) -> bool:
        now = datetime.now(ZoneInfo("Asia/Seoul")).time()
        start, end = self._trading_window_times()
        return start <= now <= end

    def _sleep_until(self, target: datetime) -> None:
        tz = target.tzinfo or ZoneInfo("Asia/Seoul")
        delay = (target - datetime.now(tz)).total_seconds()
        if delay > 0:
            logger.info(f'Waiting {int(delay)} seconds until trading window opens')
            time_module.sleep(delay)

    def run_cycle(self) -> None:
        logger.info('Starting trading cycle')
        print('Starting trading cycle')
        try:
            if not self.is_trading_window() and not self.test_mode:
                logger.info('Outside trading window: skipping cycle')
                print('Outside trading window: skipping cycle')
                return

            if self.test_mode:
                price = 70000.0
                logger.info(f'Test mode: using dummy price {price}')
                print(f'Test mode active. Using dummy price: {price}')
                cash_before = 1_000_000.0
                holdings_before: Dict[str, int] = {self.symbol: 0}
            else:
                print(f'Retrieving current price for {self.symbol}...')
                price = self.market_data.get_current_price(self.symbol)
                print(f'Current price obtained: {price}')
                cash_before, holdings_before = self.account.get_cash_and_holdings(self.symbol)
                print(f'Account cash: {cash_before}, holdings: {holdings_before}')

            buy_price = max(1, int(price) - self.offset)
            sell_price = int(price) + self.offset
            logger.info(f'Calculated prices: buy={buy_price}, sell={sell_price}')
            print(f'Calculated prices: buy={buy_price}, sell={sell_price}')

            qty_str = str(self.quantity)

            if self.test_mode:
                logger.info(f'Test mode: would place buy order for {qty_str} shares at {buy_price}')
                logger.info(f'Test mode: would place sell order for {qty_str} shares at {sell_price}')
                cash_after = cash_before
                holdings_after = holdings_before
            else:
                if cash_before >= buy_price * self.quantity:
                    logger.info(f'Placing buy order for {qty_str} shares at {buy_price}')
                    self.orders.place_buy_order(self.symbol, qty_str, str(buy_price))
                else:
                    logger.info('Insufficient cash for buy order; skipping buy order')

                if holdings_before.get(self.symbol, 0) >= self.quantity:
                    logger.info(f'Placing sell order for {qty_str} shares at {sell_price}')
                    self.orders.place_sell_order(self.symbol, qty_str, str(sell_price))
                else:
                    logger.info('No holdings available for sell order; skipping sell order')

                cash_after, holdings_after = self.account.get_cash_and_holdings(self.symbol)

            executed = (
                holdings_after.get(self.symbol, 0) != holdings_before.get(self.symbol, 0) or
                cash_after != cash_before
            )
            logger.info(f'Holdings before: {holdings_before}')
            logger.info(f'Holdings after: {holdings_after}')
            logger.info(f'Cash before: {cash_before}, cash after: {cash_after}')
            logger.info(f'Order execution detected: {executed}')

        except Exception as error:
            logger.error(f'Error in trading cycle: {error}')
            print(f'Error in trading cycle: {type(error).__name__}: {error}')

    def run(self) -> None:
        logger.info('Trader started')
        print('Trader started')
        try:
            tz = ZoneInfo("Asia/Seoul")
            now = datetime.now(tz)
            start_time, end_time = self._trading_window_times()
            start_datetime = now.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
            end_datetime = now.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

            logger.info(f'Current KST time: {now}')
            print(f'Current KST time: {now}')
            logger.info(f'Trading window: {start_time} ~ {end_time}')
            print(f'Trading window: {start_time} ~ {end_time}')

            if now >= end_datetime:
                logger.info('Trading window already closed for today')
                print('Trading window already closed for today')
                return

            if now < start_datetime:
                print('Current time is before trading window; waiting until open')
                self._sleep_until(start_datetime)

            logger.info('Trading window is open')
            print('Trading window is open')
            while datetime.now(tz) < end_datetime:
                self.run_cycle()
                if datetime.now(tz) >= end_datetime:
                    break
                sleep_seconds = min(self.poll_interval_seconds, (end_datetime - datetime.now(tz)).total_seconds())
                if sleep_seconds > 0:
                    logger.info(f'Sleeping for {int(sleep_seconds)} seconds until next cycle')
                    print(f'Sleeping for {int(sleep_seconds)} seconds until next cycle')
                    time_module.sleep(sleep_seconds)

            logger.info('Trading window ended')
            print('Trading window ended')
        except Exception as e:
            logger.error(f'Unhandled error in run(): {e}')
            print(f'Unhandled error in run(): {type(e).__name__}: {e}')
