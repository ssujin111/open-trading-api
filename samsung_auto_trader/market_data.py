from typing import Dict, Any
from api_client import APIClient
from auth import Auth
from logger import logger

class MarketData:
    def __init__(self, api_client: APIClient, auth: Auth):
        self.api_client = api_client
        self.auth = auth

    def get_current_price(self, symbol: str) -> float:
        token = self.auth.get_token()
        headers = {'authorization': f'Bearer {token}', 'tr_id': 'FHKST01010100'}
        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': symbol
        }
        response = self.api_client.get('/uapi/domestic-stock/v1/quotations/inquire-price', params, headers)
        price = float(response['output']['stck_prpr'])
        logger.info(f"Current price for {symbol}: {price}")
        return price