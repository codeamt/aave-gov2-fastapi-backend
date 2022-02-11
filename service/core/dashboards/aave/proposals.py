from service.db import graph_db
from .nlp_analyzer import ProposalAnalytics

analytics = ProposalAnalytics()


class MainNetService:
    @staticmethod
    def get_briefs():
        return graph_db.get_briefs("mainnet")

    @staticmethod
    def get_proposals_by_id(_id):
        data = graph_db.get_proposal(_id, "mainnet")
        time_series = analytics.create_snapshot_series(data.votes)
        recs = data.proposal.top_similar()
        response = dict(
            proposal=data.proposal,
            time_series=time_series,
            recs=recs
        )
        return response


class KovanNetService:
    @staticmethod
    def get_briefs():
        return graph_db.get_briefs("kovan")

    @staticmethod
    def get_proposals_by_id(_id):
        data = graph_db.get_proposal(_id, "kovan")
        time_series = analytics.create_snapshot_series(data.votes)
        response = dict(
            proposal=data.proposal,
            time_series=time_series,
            recs=[]
        )
        return response