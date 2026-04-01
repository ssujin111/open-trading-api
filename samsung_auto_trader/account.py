from typing import Dict, Any, Tuple
from api_client import APIClient
from auth import Auth
from logger import logger

class Account:
    def __init__(self, api_client: APIClient, auth: Auth, account: str, acnt_prdt_cd: str):
        self.api_client = api_client
        self.auth = auth
        self.account = account
        self.acnt_prdt_cd = acnt_prdt_cd

    def get_balance(self) -> Tuple[float, Dict[str, int]]:
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
        # output1: holdings, output2: summary
        holdings = {}
        for item in response.get('output1', []):
            if item['pdno'] == '005930':
                holdings['005930'] = int(item['hldg_qty'])
        cash = float(response['output2'][0]['dnca_tot_amt']) if response.get('output2') else 0.0
        logger.info(f"Cash: {cash}, Holdings: {holdings}")
        return cash, holdings