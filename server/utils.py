import requests
import config
import math
import json

def get_logo(name):
    if name == "AOK":
        return "https://api.aok.network/static/logo/aok.svg"

    elif name == "ARTL":
        return "https://api.aok.network/static/logo/artl.svg"

    elif name == "CCA":
        return "https://api.aok.network/static/logo/cca.svg"

    elif name == "MEC":
        return "https://api.aok.network/static/logo/mec.svg"

    elif name == "SERG":
        return "https://api.aok.network/static/logo/serg.svg"

    return f"https://source.boringavatars.com/bauhaus/120/{name}?colors=264653,2a9d8f,e9c46a,f4a261,e76f51"

def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid, pagination=None):
    result = {"error": error, "id": rid, "result": result}

    if pagination:
        result["pagination"] = pagination

    return result

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def reward(height):
    halvings = height // 525960

    if halvings >= 10:
        return 0

    return int(satoshis(4) // (2 ** halvings))

def supply(height):
    premine = satoshis(2100000000)
    reward = satoshis(4)
    halvings = 525960
    halvings_count = 0
    supply = premine + reward

    while height > halvings:
        total = halvings * reward
        reward = reward / 2
        height = height - halvings
        halvings_count += 1

        supply += total

        if halvings > 10:
            reward = 0
            break

    supply = supply + height * reward

    return {
        "halvings": int(halvings_count),
        # "supply": int(supply),
        # ToDo: fix supply calculation
        "supply": satoshis(1_000_000_000)
    }

def satoshis(value):
    return int(float(value) * math.pow(10, 8))

def amount(value, decimals=8):
    return round(float(value) / math.pow(10, decimals), decimals)
