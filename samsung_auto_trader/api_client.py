import time
from typing import Any, Dict, Optional

import requests

from logger import logger


class APIClient:
    MAX_RETRIES = 2
    TIMEOUT_SECONDS = 10

    def __init__(self, base_url: str, appkey: str, appsecret: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'content-type': 'application/json',
            'appkey': appkey,
            'appsecret': appsecret,
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.info(f"API request {method} {endpoint} attempt {attempt}")
                if method == 'GET':
                    response = self.session.get(
                        url,
                        params=params,
                        headers=request_headers,
                        timeout=self.TIMEOUT_SECONDS,
                    )
                else:
                    response = self.session.post(
                        url,
                        json=json_data,
                        headers=request_headers,
                        timeout=self.TIMEOUT_SECONDS,
                    )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:
                logger.error(f"API request failed ({method} {endpoint}): {exc}")
                if attempt == self.MAX_RETRIES:
                    raise
                backoff = 2 ** (attempt - 1)
                logger.info(f"Retrying in {backoff} seconds")
                time.sleep(backoff)

        raise RuntimeError('Reached API retry limit')

    def post(self, endpoint: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._request('POST', endpoint, json_data=data, headers=headers)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._request('GET', endpoint, params=params, headers=headers)
