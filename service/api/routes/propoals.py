from fastapi import APIRouter, WebSocket
from service.db import graph_db

aave_proposals_router = APIRouter()


@aave_proposals_router.get("/proposals/off_chain/all")
async def all_off_chain():
    p = graph_db.get_briefs(chain="kovan")
    return p


@aave_proposals_router.websocket("/ws/proposals/off_chain/all")
async def off_chain_briefs(websocket: WebSocket):
    p = graph_db.get_briefs(chain="kovan")
    while True:
        await websocket.send_json(p)


@aave_proposals_router.get("/proposals/on_chain/all")
async def all_on_chain():
    p = graph_db.get_briefs(chain="mainnet")
    return p


@aave_proposals_router.websocket("/ws/proposals/on_chain/all")
async def on_chain_briefs(websocket: WebSocket):
    p = graph_db.get_briefs(chain="mainnet")
    while True:
        await websocket.send_json(p)


@aave_proposals_router.get("/proposals/off_chain/{_id}")
async def off_chain_by_id(_id):
    p = await graph_db.get_proposal_by_id(_id, chain="kovan")
    return p


@aave_proposals_router.websocket("/ws/proposals/off_chain/{id}")
async def send_one_by_id_off_chain(_id, websocket: WebSocket):
    p = await graph_db.get_proposal_by_id(_id, chain="kovan")
    while True:
        await websocket.send_json(p)


@aave_proposals_router.get("/proposals/on_chain/{_id}")
async def on_chain_by_id(_id):
    p = await graph_db.get_proposal_by_id(_id, chain="mainnet")
    return p


@aave_proposals_router.websocket("/ws/proposals/on_chain/{id}")
async def send_one_by_id_on_chain(_id, websocket: WebSocket):
    p = await graph_db.get_proposal_by_id(_id, chain="mainnet")
    while True:
        await websocket.send_json(p)
