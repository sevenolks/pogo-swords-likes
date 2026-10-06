# Copies Pogo Swords' public like count (games.roblox.com) into likes.json, which the game reads through
# raw.githubusercontent.com (Roblox game servers can't call roblox.com). Run every 5 minutes by the "likes" workflow.
# "updated" is stamped on every run (the game ignores a copy older than 30 minutes), so every run commits.
import json, subprocess, time, urllib.request

UNIVERSE = 10769462162
URL = f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE}"

with urllib.request.urlopen(URL, timeout=20) as r:
    row = json.load(r)["data"][0]
assert row["id"] == UNIVERSE and isinstance(row["upVotes"], int) and row["upVotes"] >= 0
out = {"data": [{"id": row["id"], "upVotes": row["upVotes"], "downVotes": row["downVotes"]}], "updated": int(time.time())}
with open("likes.json", "w") as f:
    json.dump(out, f)
    f.write("\n")
if True:
    subprocess.run(["git", "config", "user.name", "likes-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "likes-bot@users.noreply.github.com"], check=True)
    subprocess.run(["git", "commit", "-am", f"likes {row['upVotes']}"], check=True)
    subprocess.run(["git", "push"], check=True)
