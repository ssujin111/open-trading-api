from datetime import datetime, time
import time as time_module
from market_data import MarketData
from account import Account
from orders import Orders
from logger import logger

class Trader:
    def __init__(self, market_data: MarketData, account: Account, orders: Orders, test_mode: bool = False):
        self.market_data = market_data
        self.account = account
        self.orders = orders
        self.symbol = '005930'
        self.offset = 2000  # KRW
        self.test_mode = test_mode

    def is_trading_window(self) -> bool:
        now = datetime.now().time()
        start = time(9, 10)
        end = time(15, 30)
        return start <= now <= end

    def run_cycle(self):
        """Run a single trading cycle for testing"""
        logger.info("Running single trading cycle")
        try:
            # For testing, skip trading window check
            # if not self.is_trading_window():
            #     logger.info("Outside trading window")
            #     return

            # Get current price
            if self.test_mode:
                price = 70000.0  # Dummy price for testing
                logger.info(f"Test mode: Using dummy price {price}")
            else:
                price = self.market_data.get_current_price(self.symbol)
            buy_price = str(int(price) - self.offset)
            sell_price = str(int(price) + self.offset)

            # Get balance
            if self.test_mode:
                cash, holdings = 1000000.0, {self.symbol: 0}  # Dummy balance
                logger.info(f"Test mode: Using dummy balance {cash}, holdings {holdings}")
            else:
                cash, holdings = self.account.get_balance()

            qty = '1'  # Simple, buy/sell 1 share

            # Place buy order
            if self.test_mode:
                logger.info(f"Test mode: Would place buy order for {qty} shares at {buy_price}")
            else:
                self.orders.place_buy_order(self.symbol, qty, buy_price)

            # Place sell order
            if self.test_mode:
                logger.info(f"Test mode: Would place sell order for {qty} shares at {sell_price}")
            else:
                self.orders.place_sell_order(self.symbol, qty, sell_price)

            # Check balance again
            if self.test_mode:
                cash_after, holdings_after = cash, holdings  # No change in test mode
                logger.info(f"Test mode: Dummy balance after {cash_after}, holdings {holdings_after}")
            else:
                cash_after, holdings_after = self.account.get_balance()
            # Simple check: if holdings changed, assume execution
            executed = holdings_after.get(self.symbol, 0) != holdings.get(self.symbol, 0)
            logger.info(f"Order execution check: {executed}")

        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")

    def run(self):
        logger.info("Starting trading loop")
        while True:
            self.run_cycle()
            time_module.sleep(300)  # Poll every 5 minutes