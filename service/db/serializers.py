from datetime import datetime, timedelta, date
from typing import List, Any, Union, Optional
from pydantic import BaseModel


class Executor(BaseModel):
    id: str
    authorized: bool
    propositionThreshold: Union[int, str]
    votingDuration: Union[int, str]
    voteDifferential: Union[int, str]
    minimumQuorum: Union[int, str]
    gracePeriod: Union[int, str]
    executionDelay: Union[int, str]

    def serialized(self):
        data = self.dict()
        for k, v in data.items():
            if type(v) == "<class 'str'>":
                data[k] = int(v)
        return data


class Vote(BaseModel):
    id: str
    voter: str
    proposal: str
    support: bool
    votingPower: Union[int, str]
    timestamp: Any


class Delegate(BaseModel):
    id: str
    address: Union[str, bytes]
    vote: bool
    proposal_id: str
    votingPower: Union[int, str]


class ProposalSerializer(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    creator: Optional[Union[str, bytes]] = None
    shortDescription: Optional[str] = None
    executor: Optional[dict] = None
    createdTimestamp: Optional[date] = None
    startBlock: Optional[Union[str, int]] = None
    endBlock: Optional[Union[str, int]] = None
    state: Optional[str] = None
    currentYesVote: Optional[Union[int, str]] = None
    currentNoVote: Optional[Union[int, str]] = None
    minimumQuorum: Optional[Union[int, str]] = None
    voteDifferential: Optional[Union[int, str]] = None
    ipfsHash: Optional[Union[str, bytes]] = None
    votes: Optional[List[dict]] = None
    delegates: Optional[List[dict]] = None
    totalVotingSupply: Optional[Union[int, str]] = None
    governanceStrategy: Optional[Union[str, bytes]] = None
    createdBlockNumber: Optional[Union[str, int]] = None
    exec_w_grace: Optional[date] = None
    propositionThreshold: Optional[Union[int, str]] = None
    targets: Optional[List[Union[str, bytes]]] = None
    values: Optional[List[Union[str, bytes]]] = None
    signatures: Optional[List[Union[str, bytes]]] = None
    embeddings: Optional[List[float]] = None
    text: Optional[str] = None

    @staticmethod
    def edit_name(name):
        if name == 'Na':
            return "Untitled"
        return name

    @staticmethod
    def edit_summary(summary):
        if summary == 'Na':
            return "This proposal does not have a short description."
        return summary

    @staticmethod
    def parse_vote(v: dict) -> dict:
        formatted_date = datetime.fromtimestamp(v["timestamp"]).date()
        vote: Vote = Vote.construct(**v)
        vote.timestamp = formatted_date
        vote.votingPower = str(int(v["votingPower"]))
        return vote.dict()

    @staticmethod
    def parse_delegates(v: dict):
        data = dict(
            address=v["voter"],
            vote=v["support"],
            proposal_id=v["proposal"],
            votingPower=v["votingPower"]
        )
        delegate = Delegate.construct(**data)
        return delegate.dict()

    @staticmethod
    def parse_to_vote_objs(_gql_res: list):
        votes = [ProposalSerializer.parse_vote(item) for item in _gql_res]
        delegates = [ProposalSerializer.parse_delegates(item) for item in votes]
        return votes, delegates


class MainNetSerializer(ProposalSerializer):
    chain: str = "main_net"

    def format_fields(self):
        self.createdBlockNumber = str(self.createdBlockNumber)
        self.creator = str(self.creator)
        self.voteDifferential = str(int(self.voteDifferential))
        self.minimumQuorum = str(int(self.minimumQuorum))
        self.ipfsHash = str(self.ipfsHash)
        self.propositionThreshold = str(int(self.propositionThreshold))
        self.governanceStrategy = str(self.governanceStrategy)
        self.totalVotingSupply = str(int(self.totalVotingSupply))
        self.startBlock = str(int(self.startBlock))
        self.endBlock = str(int(self.endBlock))
        self.currentYesVote = str(int(self.currentYesVote))
        self.currentNoVote = str(int(self.currentNoVote))
        self.votes = [self.parse_vote(v) for v in self.votes]
        self.delegates = [self.parse_delegates(v) for v in self.votes]
        return self


class KovanSerializer(ProposalSerializer):
    chain: str = "kovan"

    @staticmethod
    def gql_eth_merge(gql_res, w3_res):
        _exec = Executor.construct(**gql_res["executor"])
        _exec.propositionThreshold = str(int(_exec.propositionThreshold))
        _exec.votingDuration = str(int(_exec.votingDuration))
        _exec.voteDifferential = str(int(_exec.voteDifferential))
        _exec.minimumQuorum = str(int(_exec.minimumQuorum))
        _exec.gracePeriod = str(int(_exec.gracePeriod))
        _exec.executionDelay = str(int(_exec.executionDelay))
        votes, delegates = ProposalSerializer.parse_to_vote_objs(gql_res["votes"])
        data = dict(
            id=str(w3_res[5]),
            title=gql_res['title'],
            author=gql_res['author'],
            creator=str(w3_res[6]),
            shortDescription=gql_res["shortDescription"],
            executor=_exec.dict(),
            createdTimestamp=datetime.fromtimestamp(gql_res['createdTimestamp']).date(),
            startBlock=str(int(w3_res[13])),
            endBlock=str(int(w3_res[14])),
            state=str(w3_res[22]),
            currentYesVote=str(int(w3_res[16])),
            currentNoVote=str(int(w3_res[17])),
            minimumQuorum=str(int(w3_res[1])),
            voteDifferential=str(int(w3_res[2])),
            ipfsHash=str(gql_res['ipfsHash']),
            votes=votes,
            delegates=delegates,
            totalVotingSupply=str(int(w3_res[0])),
            governanceStrategy=str(w3_res[20]),
            createdBlockNumber=str(int(gql_res['createdBlockNumber'])),
            exec_w_grace=datetime.fromtimestamp(int(w3_res[3])).date(),
            propositionThreshold=_exec.propositionThreshold,
            targets=w3_res[8],
            values=w3_res[9],
            signatures=w3_res[10]
        )
        return data