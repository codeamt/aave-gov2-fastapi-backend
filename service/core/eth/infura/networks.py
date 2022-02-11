import os
import json
from typing import Any, Union
from pydantic import BaseModel
from web3 import Web3, HTTPProvider
from ..infura import KOVAN_ABI_DIR, MAINET_ABI_DIR
from ..contracts.mainnet.addresses import *
from ..contracts.kovan.addresses import *


class Contract(BaseModel):
    address: Union[str, bytes]
    abi: Any


class AAVEContracts(object):
    def __init__(self):
        self.kovan_client = Web3(HTTPProvider(os.getenv("INFURA_KOVAN_ENDPOINT")))
        self.mainet_client = Web3(HTTPProvider(os.getenv("INFURA_MAINET_ENDPOINT")))
        self._kovan_contract_dir = KOVAN_ABI_DIR.absolute()
        self._mainet_contract_dir = MAINET_ABI_DIR.absolute()

    @property
    def kovan_aave_gov_contract(self):
        contract = self.kovan_client.eth.contract(
            address=self.kovan_client.toChecksumAddress(KOVAN_AAVE_GOV),
            abi=json.load(open(str(self._kovan_contract_dir) + "/" + "aave_gov.json"))
        )
        return contract

    @property
    def mainet_aave_gov_contract(self):
        contract = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(MAINET_AAVE_GOV),
            abi=json.load(open(str(self._mainet_contract_dir) + "/" + "aave_gov.json"))
        )
        return contract

    @property
    def kovan_aave_gov2_helper(self):
        contract = self.kovan_client.eth.contract(
            address=self.kovan_client.toChecksumAddress(KOVAN_GOV_V2_HELP),
            abi=json.load(open(str(self._kovan_contract_dir) + "/" + "gov_v2_helper.json"))
        )
        return contract

    @property
    def mainet_aave_gov2_helper(self):
        contract = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(MAINET_GOV_V2_HELPER),
            abi=json.load(open(str(self._mainet_contract_dir) + "/" + "gov_v2_helper.json"))
        )
        return contract

    @property
    def kovan_aave_gov_strategy(self):
        contract = self.kovan_client.eth.contract(
            address=self.kovan_client.toChecksumAddress(KOVAN_GOV_STRATEGY),
            abi=json.load(open(str(self._kovan_contract_dir) + "/" + "gov_strategy.json"))
        )
        return contract

    @property
    def mainet_aave_gov_strategy(self):
        contract = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(MAINET_GOV_STRATEGY),
            abi=json.load(open(str(self._mainet_contract_dir) + "/" + "gov_strategy.json"))
        )
        return contract

    @property
    def kovan_aave_token(self):
        contract = self.kovan_client.eth.contract(
            address=self.kovan_client.toChecksumAddress(KOVAN_AAVE),
            abi=json.load(open(str(self._kovan_contract_dir) + "/" + "aave.json"))
        )
        return contract

    @property
    def mainet_aave_token(self):
        contract = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(MAINET_AAVE),
            abi=json.load(open(str(self._mainet_contract_dir) + "/" + "aave.json"))
        )
        return contract

    @property
    def kovan_stkaave_token(self):
        contract = self.kovan_client.eth.contract(
            addresss=self.kovan_client.toChecksumAddress(KOVAN_STKAAVE),
            abi=json.load(open(str(self._kovan_contract_dir) + "/" + "stkaave.json"))
        )
        return contract

    @property
    def mainet_stkaave_token(self):
        contract = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(MAINET_STKAAVE),
            abi=json.load(open(str(self._mainet_contract_dir) + "/" + "stkaave.json"))
        )
        return contract

    @property
    def infura_auth_headers(self):
        creds = (os.getenv("INFURA_ETH_PROJECT_ID"),
                 os.getenv("INFURA_ETH_SECRET"))
        return creds


"""
    def kovan_contract_instance(self, addr, f_name):
        instance = self.kovan_client.eth.contract(
            address=self.kovan_client.toChecksumAddress(addr),
            abi=json.load(open(self.kovan_abi_path(f_name))))
        return instance

    def contract_instance(self, addr, f_name):
        instance = self.mainet_client.eth.contract(
            address=self.mainet_client.toChecksumAddress(addr),
            abi=json.load(open(self.mainet_abi_path(f_name))))
        return instance

        def kovan_abi_path(self, f_name) -> str:
        return str(self._kovan_contract_dir) + "/" + f_name

    def mainet_abi_path(self, f_name) -> str:
        return str(self._mainet_contract_dir) + "/" + f_name
"""
