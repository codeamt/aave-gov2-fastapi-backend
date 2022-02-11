executor_fields = f"""{{
    id, 
    authorized, 
    propositionThreshold, 
    votingDuration, 
    voteDifferential, 
    gracePeriod, 
    executionDelay 
    minimumQuorum }}
    """

votes_fields = f"""{{
     id, 
     proposal{{ id }}
     voter, 
     support, 
     votingPower, 
     timestamp }}
    """

kovan_missing_fields = f"""
     title
     author 
     shortDescription 
     ipfsHash
     createdTimestamp
     executor {executor_fields}
     votes {votes_fields}
     governanceStrategy
     createdBlockNumber
"""

main_net_fields = f"""
    id 
    title
    author
    creator
    shortDescription 
    executor {executor_fields} 
    createdTimestamp
    startBlock
    endBlock
    state
    currentYesVote
    currentNoVote
    ipfsHash
    totalVotingSupply
    votes {votes_fields}
    governanceStrategy
    createdBlockNumber
    executionTime
    targets
    values
    signatures
"""


def kovan_missing_fields_by_id(_id):
    param = f"(id: {str(_id)})"
    q = f"""query {{ proposal { param } {{ { kovan_missing_fields } }} }}"""
    return q


def main_net_proposals(p=None):
    params = f"{p}" if p else """(first: 50, orderDirection: desc)"""
    q = f"""query {{ proposals { params } {{ { main_net_fields } }} }}"""
    return q