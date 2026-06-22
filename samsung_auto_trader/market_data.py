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
            'FID_INPUT_ISCD': symbol,
        }
        response = self.api_client.get('/uapi/domestic-stock/v1/quotations/inquire-price', params, headers)
        output = response.get('output', {})
        price_text = output.get('stck_prpr')
        if price_text is None:
            raise ValueError('Price response did not contain stck_prpr')

        price = float(price_text)
        logger.info(f'Current price for {symbol}: {price}')
        return price
