from .nodes import Vote, Delegate, User, Proposal
from neomodel import config
from dotenv import find_dotenv, load_dotenv


class NeoModelDB(object):
    env_path = find_dotenv(".env")
    load_dotenv(env_path)
    config.DATABASE_URL = "bolt://neo4j:attesting-ally-craft@3.86.97.131:7687"  # os.getenv('NEO_DB_URL')

    def __init__(self):
        self.chains = ["kovan", "mainnet"]

    @staticmethod
    def clear_proposals():
        proposals = Proposal.nodes.all()
        for prop in proposals:
            for vote in prop.casted_votes:
                vote.delete()
            for delegate in prop.voters:
                delegate.delete()
            prop.delete()
            return True
        return False

    @staticmethod
    def build_proposal_rels(item, chain):
        prop = Proposal(**item)
        proposer = Delegate.nodes.get_or_none(address=item["creator"], chain=chain)
        if proposer is None:
            proposer = Delegate(address=item["creator"], chain=chain)
        prop.created_by.connect(proposer)
        votes = [Vote(**v, chain=chain) for v in item["votes"]]
        delegates = Delegate.get_or_create(*item["delegates"])
        for (v, d) in list(zip(votes, delegates)):
            #voting_power = {"timestamp": date.fromtimestamp(v.timestamp),
            #                "support": v.support,
            #                "votingPower": int(v.votingPower)}
            prop.casted_votes.connect(v)
            prop.voters.connect(d)
            v.election.connect(prop)
            v.casted_by.connect(d)
            d.voting_record.connect(v)
            d.proposals.connect(prop)
            d.user = User.nodes.get_or_none(address=d.address)
            v.save()
            d.save()
            prop.save()
        return prop.id

    def rewrite_proposals(self, new_data, chain):
        old_height = len(Proposal.nodes.filter(chain=chain))
        rules = [new_data is not None,
                 len(new_data) > 1,
                 len(new_data) >= old_height,
                 chain in self.chains]
        if all(rules):
            self.clear_proposals()
            prop_index = [self.build_proposal_rels(item, chain)
                          for item in new_data]
            if len(prop_index) >= old_height:
                return True
        return False

    def get_proposal(self, _id, chain):
        rules = [
            id is not None,
            chain in self.chains
        ]
        if all(rules):
            prop = Proposal.nodes.get_or_none(id=_id, chain=chain)
            votes = prop.casted_votes
            delegates = prop.voters
            response = dict(proposal=prop, votes=votes, delegates=delegates)
            return response

    def get_briefs(self, chain):
        rules = [
            chain in self.chains
        ]
        if all(rules):
            props = Proposal.nodes.filter(chain=chain)
            briefs = [prop.brief() for prop in props]
            return briefs
        return None
