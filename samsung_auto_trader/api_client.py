import requests
import json
from typing import Dict, Any
from logger import logger

class APIClient:
    def __init__(self, base_url: str, appkey: str, appsecret: str):
        self.base_url = base_url
        self.appkey = appkey
        self.appsecret = appsecret
        self.session = requests.Session()
        self.session.headers.update({
            'content-type': 'application/json',
            'appkey': self.appkey,
            'appsecret': self.appsecret,
        })

    def post(self, endpoint: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        if headers:
            self.session.headers.update(headers)
        try:
            response = self.session.post(url, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    def get(self, endpoint: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        if headers:
            self.session.headers.update(headers)
        try:
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise