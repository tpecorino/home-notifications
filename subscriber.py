import json
import os
from win10toast import ToastNotifier
import aiohttp as aiohttp
from aiohttp import web
from dotenv import load_dotenv

import db

load_dotenv('./.env')

access_token = os.environ["ACCESS_TOKEN"]
url = os.environ["WEB_SOCKET_URL"]

db = db.DBConnection()

n = ToastNotifier()


async def state_change_notification(entity_label, state):
    n.show_toast('Entity "{}" state changed to {}.'.format(entity_label, state), duration=10)


async def subscribe_event(msg, ws):
    print(msg)
    subscription_payload = {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}
    await ws.send_str(json.dumps(subscription_payload))


async def subscribe_trigger(msg, ws):
    subscription_payload = {
        "id": 2,
        "type": "subscribe_trigger",
        "trigger": {
            "platform": "state",
            "entity_id": "camera.garage_camera",
        },
    }
    await ws.send_str(json.dumps(subscription_payload))


async def send_auth(msg, ws):
    payload = {
        "type": "auth",
        "access_token": access_token
    }
    await ws.send_str(json.dumps(payload))


async def handle_event(data):
    entities = [i[0] for i in db.fetch_entity_by_is_subscribed()]
    
    event_type = data["event"]["event_type"]
    new_state = data["event"]["data"]["new_state"]
    entity_id = new_state["entity_id"]
    state = new_state["state"]
    entity_label = new_state["attributes"]["friendly_name"]
    if event_type == "state_changed" and entity_id in entities:
        await state_change_notification(entity_label, state)


async def websocket(session):
    async with session.ws_connect(url) as ws:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                print(data)

                if data["type"] == "auth_required":
                    await send_auth(msg.data, ws)
                if data["type"] == "auth_ok":
                    await subscribe_event(msg.data, ws)
                    await subscribe_trigger(msg.data, ws)
                if data["type"] == "event":
                    await handle_event(data)

            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print('closed')
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('error')
                break


async def start(app):
    print('init')
    session = aiohttp.ClientSession()
    await websocket(session)


def init():
    app = web.Application()
    app.on_startup.append(start)
    aiohttp.web.run_app(app)
