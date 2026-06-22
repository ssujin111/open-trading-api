from typing import Dict, Tuple

from api_client import APIClient
from auth import Auth
from logger import logger


class Account:
    def __init__(self, api_client: APIClient, auth: Auth, account: str, acnt_prdt_cd: str):
        self.api_client = api_client
        self.auth = auth
        self.account = account
        self.acnt_prdt_cd = acnt_prdt_cd

    def get_cash_and_holdings(self, symbol: str) -> Tuple[float, Dict[str, int]]:
        token = self.auth.get_token()
        headers = {'authorization': f'Bearer {token}', 'tr_id': 'VTTC8434R'}
        params = {
            'CANO': self.account,
            'ACNT_PRDT_CD': self.acnt_prdt_cd,
            'AFHR_FLPR_YN': 'N',
            'INQR_DVSN': '02',  # 종목별
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '00'
        }
        response = self.api_client.get('/uapi/domestic-stock/v1/trading/inquire-balance', params, headers)

        holdings_qty = 0
        for item in response.get('output1', []):
            if item.get('pdno') == symbol:
                holdings_qty = int(item.get('hldg_qty', 0))

        cash = 0.0
        if response.get('output2'):
            cash_text = response['output2'][0].get('dnca_tot_amt', '0').replace(',', '')
            try:
                cash = float(cash_text)
            except ValueError:
                logger.warning(f"Unable to parse cash amount '{cash_text}'")
                cash = 0.0

        holdings = {symbol: holdings_qty}
        logger.info(f'Cash: {cash}, Holdings: {holdings}')
        return cash, holdings
