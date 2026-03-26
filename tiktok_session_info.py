import requests
import time
from datetime import datetime

sid = input("Enter TikTok session ID: ")

cookies = {
    "sessionid": sid
}

url = "https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/"

try:
    req = requests.get(url, cookies=cookies)
    json_data = req.json()
    if "data" not in json_data:
    	print(req.text)
    	exit()

    data = json_data.get("data", {})
    
    description = data.get("description", "")
    if "expired" in description.lower():
    	print(" • ", description)
    	exit()
        
    user_id = data.get("user_id") or None
    username = data.get("username") or None
    screen_name = data.get("screen_name") or None
    email = data.get("email") or None
    session_key = data.get("session_key") or None
    user_create_time = data.get("user_create_time")

    connects = data.get("connects", [])
    if connects:
        c = connects[0]
        expire_in = c.get("expires_in")
        expire_time = c.get("expired_time")

        if expire_time:
            now = int(time.time())
            remaining = max(0, expire_time - now)  
            days = remaining // 86400
            hours = (remaining % 86400) // 3600
            minutes = (remaining % 3600) // 60
            expire_date = datetime.fromtimestamp(expire_time)
        else:
            days = hours = minutes = None
            expire_date = None
    else:
        expire_in = expire_time = None
        days = hours = minutes = None
        expire_date = None

    create_date = datetime.fromtimestamp(user_create_time) if user_create_time else None
    
    if days is None:
    	expires_text = "None"
    else:
    	expires_text = f"{days}d {hours}h {minutes}m"
    print()
    print(f" • Session Key: {session_key}")
    print(f" • Session expires in: {expires_text}")
    print(f" • Exact expire date: {expire_date}")
    print()
    print(f" • User ID: {user_id}")
    print(f" • Username: {username}")
    print(f" • Screen Name: {screen_name}")
    print(f" • Email: {email}")
    print(f" • User created: {create_date}")

except Exception as e:
    print("Error:", e)