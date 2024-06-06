import requests, time, json

base_url = "https://api.hamsterkombat.io/"
with open("config.json") as file: token = json.load(file)["token"]


def get_sync():
    sync_data = requests.post(
        base_url + "clicker/sync", headers={"Authorization": token}
    ).json()

    av_taps = sync_data["clickerUser"]["availableTaps"]
    mx_taps = sync_data["clickerUser"]["maxTaps"]
    balance = sync_data["clickerUser"]['balanceCoins']
    return {"av_taps": av_taps, "mx_taps": mx_taps, "balance": balance}


def collect_taps(sync_result):
    r = requests.post(
        base_url + "clicker/tap",
        headers={"Authorization": token},
        json={
            "availableTaps": sync_result["mx_taps"],
            "count": sync_result["av_taps"],
            "timestamp": int(time.time()),
        },
    )

    if r.status_code == 200:
        return True
    else:
        return False

def get_boosts():
    boosts = requests.post(base_url + "clicker/boosts-for-buy", headers={"Authorization": token}).json()
    return boosts['boostsForBuy']

def buy_boost(id):
    boosts = requests.post(base_url + "clicker/buy-boost", headers={"Authorization": token},json={"boostId":id,"timestamp":int(time.time())})
    if boosts.status_code == 200:
        return True
    else:
        return False

def get_upgrade():
    upgrade = requests.post(base_url + "clicker/upgrades-for-buy", headers={"Authorization": token}).json()
    return upgrade

def buy_upgrade(id):
    upgrade = requests.post(base_url + "clicker/buy-upgrade", headers={"Authorization": token},json={"upgradeId":id,"timestamp":int(time.time())})
    if upgrade.status_code == 200:
        return True
    else:
        return False


