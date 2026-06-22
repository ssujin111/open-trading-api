# Samsung Auto Trader 프로젝트 결과 보고서
## 1. 프로젝트 개요
본 프로젝트는 한국투자증권(KIS) 모의투자 Open API를 활용하여, 지정된 로직에 따라 삼성전자(005930) 주식의 자동 매매를 수행하는 파이썬(Python) 기반의 시스템을 구축하는 것을 목표로 한다. API 연동부터 시간대 동기화, 예외 처리 및 방어적 프로그래밍 로직을 적용하여 실제 금융 환경에서 안정적으로 동작할 수 있도록 구현하였다.

## 2. 주요 수행 작업 및 문제 해결 과정
1) 환경 변수 및 크리덴셜(Credential) 보안 관리
- 하드코딩으로 인한 보안 취약점을 방지하기 위해 python-dotenv 라이브러리를 활용하였다.
- API Key, Secret Key, 계좌번호(CANO) 등 핵심 인증 정보를 .env 파일에 분리하여 안전하게 관리하고, 시스템 시작 시 main.py에서 이를 성공적으로 검증하도록 구현하였다.

2) 시간대(Timezone) 인식 및 거래 시간 제어 오류 해결
- 이슈: 서버의 기본 시간대(UTC)와 한국 시간(KST) 간의 차이, 그리고 파이썬의 offset-naive와 offset-aware datetime 객체 간의 비교 연산에서 TypeError가 발생하였다.
- 해결: pytz 등을 활용하여 프로그램이 한국 시간(Asia/Seoul)을 명시적으로 인식하도록 수정하였다. 이를 통해 주식 시장 개장 시간(09:10 ~ 15:30)을 정확히 판별하고, 해당 시간이 아닐 경우 불필요한 API 호출을 막고 대기(Sleep) 모드로 전환되도록 시간 제어 로직을 완성하였다.

3) API 통신 에러 대처 (방어적 프로그래밍 구현)
- 이슈: 모의투자 서버의 불안정성으로 인해 주가 및 잔고 조회 시 간헐적인 500 Internal Server Error 및 Read Timeout 오류가 발생하였다.
- 해결: 에러 발생 시 프로그램이 강제 종료되지 않도록 try-except 구문을 통한 예외 처리를 구현하였다. 통신 실패 시 즉각 종료하는 대신, 일정 시간(1초) 대기 후 재시도(Retry)를 수행하고, 지속적인 통신 불량 시 300초(5분) 대기 후 다음 사이클을 도는 안정적인 방어 로직을 구축하였다.

4) 매매 로직 검증 및 자산 보호(Skipping) 로직
- --test --cycle 인자를 활용한 가상 테스트 모드를 구현하여, 실제 자본 소모 없이 목표 매수/매도 가격(현재가 기준 산출) 계산 및 조건 분기 로직을 검증하였다.
- 실전 구동 시 현재 잔고(Cash)와 보유 주식(Holdings)을 API로 직접 조회하며, 매수 잔고가 부족하거나 매도할 주식이 없을 경우 강제로 주문을 발생시키지 않고 안전하게 건너뛰는(Skipping) 자산 보호 로직이 정상 작동함을 확인하였다.

## 3. 코드 구조 이해도 핵심 요약
- main.py: 시스템의 진입점(Entry point) 역할을 한다. 환경 변수를 불러오고 API 접근 권한을 확인한 후, 매매 로직의 핵심인 Trader 인스턴스를 생성하고 실행루프를 가동한다.
- trader.py: 실제 매매의 두뇌 역할을 하는 모듈이다. 한국투자증권 API와 통신하여 현재 가격을 조회하고(inquire-price), 계좌 상태를 파악한 뒤(inquire-balance), 설정된 조건식에 맞춰 주문을 실행하거나 대기하는 전체 사이클을 관리한다.

## 4. 결론
초기 환경 세팅 및 데이터 통신 과정에서 발생하는 다양한 예외 상황들을 성공적으로 디버깅하였다. 결과적으로 지정된 시간 내에 스스로 시장 상황과 계좌 잔고를 파악하여 유연하게 대처할 수 있는, 완전한 형태의 자동매매 시스템을 완성하였다.

<img width="1920" height="1080" alt="주식매매 최종4실제모투" src="https://github.com/user-attachments/assets/9d59098d-6dfe-49d8-a4e2-251bb88bc2ac" />

-------------------------------------------------
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
