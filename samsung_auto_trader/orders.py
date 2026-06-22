from typing import Dict, Any

from api_client import APIClient
from auth import Auth
from logger import logger


class Orders:
    BUY_SIDE = '01'   # Placeholder: buy side code
    SELL_SIDE = '02'  # Placeholder: sell side code

    def __init__(self, api_client: APIClient, auth: Auth, account: str, acnt_prdt_cd: str):
        self.api_client = api_client
        self.auth = auth
        self.account = account
        self.acnt_prdt_cd = acnt_prdt_cd

    def _place_order(self, symbol: str, qty: str, price: str, side_code: str, tr_id: str) -> Dict[str, Any]:
        token = self.auth.get_token()
        headers = {
            'authorization': f'Bearer {token}',
            'tr_id': tr_id,
        }
        data = {
            'CANO': self.account,
            'ACNT_PRDT_CD': self.acnt_prdt_cd,
            'PDNO': symbol,
            'ORD_DVSN': '00',  # 지정가 주문
            'ORD_QTY': qty,
            'ORD_UNPR': price,
            'EXCG_ID_DVSN_CD': 'KRX',
            'BNS_DVSN_CD': side_code,
        }
        response = self.api_client.post('/uapi/domestic-stock/v1/trading/order-cash', data, headers)
        return response

    def place_buy_order(self, symbol: str, qty: str, price: str) -> Dict[str, Any]:
        response = self._place_order(symbol, qty, price, self.BUY_SIDE, 'VTTC0012U')
        logger.info(f'Buy order placed: symbol={symbol}, qty={qty}, price={price}, response={response}')
        return response

    def place_sell_order(self, symbol: str, qty: str, price: str) -> Dict[str, Any]:
        response = self._place_order(symbol, qty, price, self.SELL_SIDE, 'VTTC0011U')
        logger.info(f'Sell order placed: symbol={symbol}, qty={qty}, price={price}, response={response}')
        return response
