from flask import Flask
import redis

app = Flask(__name__)

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return "Redis is running on Windows!"

@app.route("/visit")
def visit():
    count = r.incr("visits")
    return f"Total visits: {count}"

@app.route("/set/<key>/<value>")
def set_value(key, value):
    r.set(key, value)
    return f"Saved {key} = {value}"

@app.route("/get/<key>")
def get_value(key):
    value = r.get(key)
    return f"{key} = {value}"

# --- Leaderboard Feature (Sorted Sets) ---
@app.route("/leaderboard/add/<player>/<score>")
def add_score(player, score):
    # ZADD: Add player with score to "leaderboard" sorted set
    r.zadd("leaderboard", {player: float(score)})
    return f"Added {player} with score {score}"

@app.route("/leaderboard")
def get_leaderboard():
    # ZREVRANGE: Get top 3 players (highest score first) with scores
    # withscores=True returns list of tuples [(player, score), ...]
    top_players = r.zrevrange("leaderboard", 0, 2, withscores=True)
    result = "<h1>🏆 Leaderboard 🏆</h1><br>"
    for rank, (player, score) in enumerate(top_players, 1):
        result += f"{rank}. {player}: {int(score)}<br>"
    return result

# --- Self-Destructing Message Feature (TTL) ---
@app.route("/secret/<message>")
def set_secret(message):
    # SET with EX (Expiration) in seconds
    r.set("secret_msg", message, ex=10)
    return "Secret message saved! It will self-destruct in 10 seconds."

@app.route("/get_secret")
def get_secret():
    msg = r.get("secret_msg")
    if msg:
        return f"🤫 The secret is: {msg}"
    else:
        return "👻 This message has self-destructed (or never existed)."

if __name__ == "__main__":
    app.run(debug=True)
