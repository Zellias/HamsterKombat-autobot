import requests
import json
import time
from modules.formal import get_sync, collect_taps, get_boosts, buy_boost, get_upgrade, buy_upgrade
from modules.webhook import send_discord_message
from scheduler import Scheduler
import datetime as dt

base_url = "https://api.hamsterkombat.io/"
with open("config.json") as file:
    token = json.load(file)["token"]

schedule = Scheduler()


def collect():
    sync_result = get_sync()

    if sync_result["av_taps"] >= 1:
        print(
            "\033[92m+ Collected " + str(sync_result["av_taps"]) + " taps\033[0m"
        )  # Green text
        collect_taps(sync_result)
    else:
        print(
            "\033[91m- Not enough taps available | "
            + str(sync_result["av_taps"])
            + "\033[0m"
        )  # Red text


def update_boosts():
    boost_res = get_boosts()
    sync_result = get_sync()

    balance = sync_result["balance"]

    if (int(balance) / 2) > boost_res[1]["price"]:
        if buy_boost("BoostMaxTaps"):
            print("\033[93m+ Boosted max taps\033[0m")
            send_discord_message(
                "\n### Boost Update\n+ Successfully boosted max taps.\n"
            )
        else:
            print("\033[91m- Failed to boost max taps\033[0m")
            send_discord_message("\n### Boost Update\n- Failed to boost max taps.\n")

    if boost_res[2]["cooldownSeconds"] < 1:
        if buy_boost("BoostFullAvailableTaps"):
            print("\033[93m+ Boosted available taps\033[0m")
            send_discord_message(
                "\n### Boost Update\n+ Successfully boosted available taps.\n"
            )
        else:
            print("\033[91m- Failed to boost available taps\033[0m")
            send_discord_message(
                "\n### Boost Update\n- Failed to boost available taps.\n"
            )


def update_upgrades():
    upgrade_res = get_upgrade()
    sync_result = get_sync()

    balance = sync_result["balance"]
    available_upgrades = [
        upgrade for upgrade in upgrade_res['upgradesForBuy']
        if upgrade['isAvailable'] and not upgrade['isExpired'] and ('cooldownSeconds' not in upgrade or upgrade['cooldownSeconds'] <= 0)
    ]
    if available_upgrades:
        lowest_price_upgrade = min(available_upgrades, key=lambda x: x['price'])
        if int(lowest_price_upgrade['price']) <= int((balance/5)):
            buy_upgrade(lowest_price_upgrade['id'])
            print("\033[93m+ Bought upgrade: " + lowest_price_upgrade['name'] + "\033[0m")
            send_discord_message(f"\n### Upgrade Update\n+ Successfully bought upgrade: {lowest_price_upgrade['name']} for {lowest_price_upgrade['price']}.\n")
        else:
            return
    else:
        print("\033[91m- No available upgrades\033[0m")


schedule.cyclic(dt.timedelta(seconds=5), collect)
schedule.cyclic(dt.timedelta(seconds=10), update_boosts)
schedule.cyclic(dt.timedelta(seconds=1), update_upgrades)


while True:
    schedule.exec_jobs()
    time.sleep(1)
