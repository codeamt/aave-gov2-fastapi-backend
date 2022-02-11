import os
import requests


class InfuraIpfsV3(object):
    """Explainer"""
    def __init__(self):
        self._base_url = f"{os.getenv('INFURA_IPFS_ENDPOINT')}/api/v0/"
        self._creds = (os.getenv("INFURA_IPFS_PROJECT_ID"),
                       os.getenv("INFURA_IPFS_SECRET"))

    def cat(self, params):
        """"""
        response = requests.post(f"{self._base_url}/cat",
                                 params=params,
                                 auth=self._creds)
        return response.json()

    @staticmethod
    def ipfs_url(h):
        """"""
        return f"https://ipfs.io/ipfs/{h}"