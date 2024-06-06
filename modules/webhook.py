import json
import requests

def send_discord_message(message):
    with open("config.json") as file:
        config = json.load(file)
        webhook_url = config["webhook"]
        
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 204:
        print("\033[94m+ Log sent successfully to Discord.\033[0m")
    

