from neomodel import BooleanProperty, StringProperty, UniqueIdProperty, \
    ArrayProperty, DateProperty, DateTimeFormatProperty, \
    StructuredNode, RelationshipTo, Relationship, RelationshipFrom


class Comment(StructuredNode):
    id = UniqueIdProperty()
    timestamp = DateTimeFormatProperty()
    message = StringProperty()


class UpVote(Comment):
    poi = Relationship('PointOfInterest', 'UP_VOTE')
    user = RelationshipFrom('User', 'UP_VOTED')


class DownVote(Comment):
    poi = Relationship('PointOfInterest', 'DOWN_VOTE')
    user = RelationshipFrom('User', 'DOWN_VOTED')


class User(StructuredNode):
    address = StringProperty()
    created_at = DateTimeFormatProperty()
    last_login = DateTimeFormatProperty()
    nonce = StringProperty()

    sessions = RelationshipTo('Online', 'IS')
    delegations = RelationshipFrom('Delegate', 'DELEGATING_AS')
    comments = RelationshipTo('Comment', 'POSTED')
    threads = RelationshipTo('Proposal', 'IS_SUBSCRIBED_TO')
    up_votes = RelationshipTo('PointOfInterest', 'UP_VOTED')
    down_votes = RelationshipTo('PointOfInterest', 'DOWN_VOTED')


class Online(StructuredNode):
    timestamp = DateTimeFormatProperty()
    token = StringProperty()

    user = RelationshipFrom('User', 'IS')


class Vote(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    chain = StringProperty()
    voter = StringProperty()
    support = BooleanProperty()
    votingPower = StringProperty()
    timestamp = DateProperty()
    election = RelationshipTo('Proposal', 'ON')
    casted_by = RelationshipTo('Delegate', 'CASTED_BY')


class Delegate(StructuredNode):
    id = UniqueIdProperty()
    address = StringProperty()
    chain = StringProperty()
    voting_record = RelationshipTo('Vote', 'CASTED')
    proposals = RelationshipTo('Proposal', 'VOTED_ON')
    pois = RelationshipTo('PointOfInterest', 'RAISED')
    user = RelationshipTo('User', 'DELEGATING_AS')


class PointOfInterest(Comment):
    point = StringProperty()
    timestamp = DateTimeFormatProperty()

    proposal = RelationshipTo('Proposal', 'RAISED_IN')
    delegate = RelationshipFrom('Delegate', 'RAISED')
    up_votes = RelationshipFrom('User', 'UP_VOTED')
    down_votes = RelationshipFrom('User', 'DOWN_VOTED')


class Proposal(StructuredNode):
    id = StringProperty()
    chain = StringProperty(required=True)
    title = StringProperty()
    author = StringProperty()
    creator = StringProperty()
    shortDescription = StringProperty()
    executor = StringProperty()
    createdTimestamp = DateProperty()
    startBlock = StringProperty()
    endBlock = StringProperty()
    state = StringProperty()
    currentYesVote = StringProperty()
    currentNoVote = StringProperty()
    minimumQuorum = StringProperty()
    voteDifferential = StringProperty()
    ipfsHash = StringProperty()
    totalVotingSupply = StringProperty()
    governanceStrategy = StringProperty()
    createdBlockNumber = StringProperty()
    exec_w_grace = DateProperty()
    propositionThreshold = StringProperty()
    votes = ArrayProperty()
    targets = ArrayProperty()
    values = ArrayProperty()
    signatures = ArrayProperty()
    embeddings = ArrayProperty()
    text = StringProperty()

    created_by = RelationshipTo('Delegate', 'PROPOSED')
    casted_votes = RelationshipFrom('Vote', 'ON')
    voters = RelationshipFrom('Delegate', 'VOTED_ON')
    subscribers = RelationshipFrom('User', 'IS_SUBSCRIBED_TO')
    discussion = RelationshipFrom('PointOfInterest', 'RAISED_IN')

    def brief(self):
        data = dict()
        return data

    def top_similar(self):
        query = f'''
        MATCH (p: Proposal {{chain={self.chain}}}, id(p)={self}) 
        MATCH (o:Proposal {{chain={self.chain}}})
        WITH p, collect(o) as others
        UNWIND others as other
        apoc.text.distance(p.text, other.text) as similarity
        WHERE similarity > 0.5
        CREATE (p)-[:SIMILAR_TO {{score: similarity}}]-> (o)
        '''
        top_sim, columns = StructuredNode.cypher(query)
        return [StructuredNode.inflate(row[0] for row in top_sim)]