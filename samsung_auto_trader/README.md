# Samsung Auto Trader

A simple automated trading system for Samsung Electronics (005930) using Korea Investment & Securities Open API in mock trading environment.

## Setup

1. In GitHub Codespace, set the following secrets in your repository settings:
   - `GH_ACCOUNT`: Your account number
   - `GH_APPKEY`: Your app key
   - `GH_APPSECRET`: Your app secret

2. The devcontainer will automatically load these secrets into environment variables and create a `.env` file.

3. Install dependencies (automatically done in devcontainer):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the trader:
   ```bash
   python main.py
   ```

   For testing (no real API calls):
   ```bash
   python main.py --test --cycle
   ```

   Options:
   - `--test`: Run in test mode with dummy data
   - `--cycle`: Run a single cycle instead of continuous loop

## Features

- Polls current price every 5 minutes during trading window (09:10 - 15:30)
- Places buy order at current_price - 2000 KRW
- Places sell order at current_price + 2000 KRW
- Checks balance before and after orders to confirm execution
- Caches token for same-day reuse
- Logs all actions

## Safety

- Mock trading only
- Conservative polling intervals
- No websocket, REST API only
- Minimal API calls