import urllib.request, json
from shutil import copyfile
from termcolor import colored
from tinydb import TinyDB, Query

db = TinyDB("/home/nepmia/Myazu/db/db.json")

def api_get():
    print(colored("[Myazu]","cyan"), colored("Fetching WynncraftAPI...", "white"))
    try:
        with urllib.request.urlopen("https://api.wynncraft.com/public_api.php?action=guildStats&command=Spectral%20Cabbage") as u1:
            api_1 = json.loads(u1.read().decode())
            count = 0
            if members := api_1.get("members"):
                print(colored("[Myazu]","cyan"),
                      colored("Got expecteded answer, starting saving process.", "white"))
                for member in members:
                    nick = member.get("name")
                    ur2 = f"https://api.wynncraft.com/v2/player/{nick}/stats"
                    u2 = urllib.request.urlopen(ur2)
                    api_2 = json.loads(u2.read().decode())
                    data = api_2.get("data")
                    for item in data:
                            meta = item.get("meta")
                            playtime = meta.get("playtime")
                            print(colored("[Myazu]","cyan"),
                                  colored("Saving playtime for player", "white"),
                                  colored(f"{nick}...","green"))
                            db.insert({"username": nick, "playtime": playtime})
                            count += 1
            else: 
                print(colored("[Myazu]","cyan"), 
                      colored("Unexpected answer from WynncraftAPI [ERROR 1]", "white"))
    except:
        print(colored("[Myazu]","cyan"), 
              colored("Unhandled error in saving process [ERROR 2]", "white"))
    finally:
        print(colored("[Myazu]","cyan"),
              colored(f"Finished saving data for", "white"),
              colored(f"{count}", "green"), 
              colored("players.", "white"))

# def purge_db():
#     print(colored("[Myazu]","cyan"), colored("Purging database...", "white"))
#     f = open("/home/nepmia/Myazu/db/db.json", "w")
#     f.seek(0)
#     f.truncate()
#     print(colored("[Myazu]","cyan"), colored("Purged database.", "white"))
#     print(colored("[Myazu]","cyan"), colored("Starting api_get process.", "white"))

# def deploy_db():
#     print(colored("[Myazu]", "cyan"), colored("Deploying database...", "white"))
#     copyfile("/home/nepmia/Myazu/db/db.json", "/var/lib/docker/volumes/nginx_data/_data/api/spc/db.json")
#     print(colored("[Myazu]", "cyan"), colored("Deployed database.", "white"))

purge_db()
api_get()
# deploy_db()
