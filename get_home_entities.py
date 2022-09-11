import requests


def map_entities(state):
    return state["entity_id"]


def fetch_entities(url, access_token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(access_token)}
    r = requests.get("{}/states".format(url), headers=headers)
    states = r.json()
    entities = map(map_entities, states)
    return list(entities)
