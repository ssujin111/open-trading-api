from typing import Dict, Any
from api_client import APIClient
from auth import Auth
from logger import logger

class Orders:
    def __init__(self, api_client: APIClient, auth: Auth, account: str, acnt_prdt_cd: str):
        self.api_client = api_client
        self.auth = auth
        self.account = account
        self.acnt_prdt_cd = acnt_prdt_cd

    def place_buy_order(self, symbol: str, qty: str, price: str):
        token = self.auth.get_token()
        headers = {'authorization': f'Bearer {token}', 'tr_id': 'VTTC0012U'}
        data = {
            'CANO': self.account,
            'ACNT_PRDT_CD': self.acnt_prdt_cd,
            'PDNO': symbol,
            'ORD_DVSN': '00',  # 지정가
            'ORD_QTY': qty,
            'ORD_UNPR': price,
            'EXCG_ID_DVSN_CD': 'KRX'
        }
        response = self.api_client.post('/uapi/domestic-stock/v1/trading/order-cash', data, headers)
        logger.info(f"Buy order placed: {response}")
        return response

    def place_sell_order(self, symbol: str, qty: str, price: str):
        token = self.auth.get_token()
        headers = {'authorization': f'Bearer {token}', 'tr_id': 'VTTC0011U'}
        data = {
            'CANO': self.account,
            'ACNT_PRDT_CD': self.acnt_prdt_cd,
            'PDNO': symbol,
            'ORD_DVSN': '00',
            'ORD_QTY': qty,
            'ORD_UNPR': price,
            'EXCG_ID_DVSN_CD': 'KRX'
        }
        response = self.api_client.post('/uapi/domestic-stock/v1/trading/order-cash', data, headers)
        logger.info(f"Sell order placed: {response}")
        return response