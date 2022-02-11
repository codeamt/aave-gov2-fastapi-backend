import datetime
import requests
import polling2
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

from ..graphql.queries import main_net_proposals, kovan_missing_fields_by_id
from ..eth.infura.networks import AAVEContracts
from service.db import graph_db
from service.db.serializers import MainNetSerializer, KovanSerializer


contracts = AAVEContracts()


class MainNetScraper(object):
    def __init__(self):
        self.subgraph_ep = \
            "https://api.thegraph.com/subgraphs/name/aave/governance-v2"
        self.gql_data = []
        thread = Thread(target=self.poll)
        thread.start()

    def get_data(self):
        result = requests.post(self.subgraph_ep,
                               json={"query": main_net_proposals()},
                               headers={"Content-Type": "application/json"})
        # print(result)
        self.gql_data = result.json()["data_index"]["proposals"]
        return dict(status_code=200)

    def callback(self, response):
        # print(response)
        if response["status_code"] == 200:
            proposals = []
            for obj in self.gql_data:
                prop: MainNetSerializer = MainNetSerializer.construct(**obj).format_fields()
                prop.createdTimestamp = datetime.date.fromtimestamp(obj["createdTimestamp"])
                proposals += [prop]
            stored_proposals = graph_db.rewrite_proposals(
                [x.dict() for x in proposals], chain="mainnet"
            )
            if stored_proposals is not None:
                return response["status_code"] == 200
            return False

    def poll(self):
        polling2.poll(
            lambda: self.get_data(),
            step=1,
            timeout=10,
            check_success=self.callback
        )


class KovanNetScraper(object):
    def __init__(self):
        self.subgraph_ep = \
            "https://api.thegraph.com/subgraphs/name/aave/governance-v2-kovan"
        self.gql_res = []
        self.eth_res = []
        thread = Thread(target=self.poll)
        thread.start()

    def get_data(self):
        self.eth_res = contracts.kovan_aave_gov2_helper \
            .functions \
            .getProposals(0, 50, contracts.kovan_aave_gov_contract.address) \
            .call()
        result = [requests.post(self.subgraph_ep,
                                json={"query": kovan_missing_fields_by_id(item[5])},
                                headers={"Content-Type": "application/json"})
                  for item in self.eth_res]
        # print(result)
        self.gql_res = [dict(r.json()["data_index"]["proposal"]) for r in result]
        return dict(status_code=200)

    def callback(self, response):
        if response["status_code"] == 200:
            data = [(gql_r, eth_r) for gql_r, eth_r in list(zip(self.gql_res, self.eth_res))]
            proposals = [KovanSerializer.gql_eth_merge(item[0], item[1]) for item in data]
            proposals = [KovanSerializer.construct(**item).dict() for item in proposals]
            _ = graph_db.rewrite_proposals(proposals, chain="kovan")
            return response["status_code"] == 200

    def poll(self):
        polling2.poll(
            lambda: self.get_data(),
            step=1,
            timeout=10,
            check_success=self.callback
        )


main_net_scraper = MainNetScraper()
kovan_net_scraper = KovanNetScraper()

schedule = BackgroundScheduler(job_defaults={'max_instances': 2})

schedule.add_job(main_net_scraper.poll)
schedule.add_job(kovan_net_scraper.poll)

schedule.start()

