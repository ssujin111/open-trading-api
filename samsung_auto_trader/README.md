# Samsung Auto Trader

A simple automated trading system for Samsung Electronics (`005930`) using the Korea Investment & Securities Open API in a mock trading environment.

## Folder Structure

- `main.py` - entrypoint and CLI arguments
- `config.py` - environment and client configuration
- `auth.py` - authentication and same-day token caching
- `api_client.py` - REST API request wrapper, timeouts, and retries
- `market_data.py` - current price lookup for 005930
- `account.py` - account cash and holdings inquiry
- `orders.py` - buy/sell order submission
- `trader.py` - trading loop and order coordination
- `logger.py` - shared logging configuration
- `requirements.txt` - Python dependencies
- `token_cache.json` - generated at runtime to store the current-day token

## Setup

1. Set environment variables (do not hardcode credentials):
   - `GH_ACCOUNT`
   - `GH_APPKEY`
   - `GH_APPSECRET`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the trader:
   ```bash
   python main.py
   ```

4. For a single test cycle without real API calls:
   ```bash
   python main.py --test --cycle
   ```

## Behavior

- Trades only during the trading window: **09:10 to 15:30**.
- Uses REST only, no websocket.
- Caches token for same-day reuse in `token_cache.json`.
- Orders are placed conservatively and verified by checking account information again.
- Buy order is placed at current_price - 2000 KRW.
- Sell order is placed at current_price + 2000 KRW.

## Notes

- Mock trading environments usually have strict request limits; this app uses conservative polling and avoids unnecessary repeated requests.
- The order-side field and some API field names are isolated in `orders.py` as placeholders so they can be updated if the API contract changes.
- Logs are written to `trading.log` and also printed to the console.
