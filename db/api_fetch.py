import urllib.request, json
from tinydb import TinyDB, Query

db = TinyDB("db.json")

def api_get():
    print("[Myazu] Fetching WynncraftAPI...")
    try:
        with urllib.request.urlopen("https://api.wynncraft.com/public_api.php?action=guildStats&command=Spectral%20Cabbage") as u1:
            api_1 = json.loads(u1.read().decode())
            count = 0
            if members := api_1.get("members"):
                print("[Myazu] Got expecteded answer, starting saving process.")
                for member in members:
                    nick = member.get("name")
                    ur2 = f"https://api.wynncraft.com/v2/player/{nick}/stats"
                    u2 = urllib.request.urlopen(ur2)
                    api_2 = json.loads(u2.read().decode())
                    data = api_2.get("data")
                    for item in data:
                            meta = item.get("meta")
                            playtime = meta.get("playtime")
                            play_mult = playtime * 4.7
                            print(f"[Myazu] Saving playtime for player {nick}...")
                            db.insert({"username": nick, "playtime": play_mult})
                            count += 1
            else: 
                print("[Myazu] Unexpected answer from WynncraftAPI [ERROR 1]")
    except:
        print("[Myazu] Unhandled error in saving process [ERROR 2]")
    finally:
        print(f"[Myazu] Finished saving data for {count} players.")

def purge_db():
    

api_get()
# def db_user_addition():
#     for item in db:
#         print(item)
