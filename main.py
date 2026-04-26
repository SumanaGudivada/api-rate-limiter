from fastapi import FastAPI, HTTPException
import redis
from datetime import datetime
from db import collection

app = FastAPI()

LIMIT = 5
WINDOW = 60

# Redis connection
r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1
)

# ---------------------------
# Helper: Log request
# ---------------------------
def log_request(user_id, status):
    collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "status": status
    })

# ---------------------------
# Health Check
# ---------------------------
@app.get("/test")
def test():
    return {"status": "working"}

# ---------------------------
# Rate Limiter API
# ---------------------------
@app.get("/api")
def access_api(user_id: str):
    key = f"user:{user_id}"
    now = datetime.utcnow().timestamp()

    # Redis pipeline (optimized)
    pipe = r.pipeline()
    pipe.zadd(key, {now: now})
    pipe.zremrangebyscore(key, 0, now - WINDOW)
    pipe.zcard(key)
    pipe.expire(key, WINDOW)

    _, _, count, _ = pipe.execute()

    if count > LIMIT:
        log_request(user_id, "blocked")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    log_request(user_id, "allowed")

    return {
        "message": "Request successful",
        "count": count
    }

# ---------------------------
# Analytics: Top Users
# ---------------------------
@app.get("/analytics/top-users")
def top_users():
    pipeline = [
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    return list(collection.aggregate(pipeline))

# ---------------------------
# Analytics: Allowed vs Blocked
# ---------------------------
@app.get("/analytics/status")
def status_stats():
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    return list(collection.aggregate(pipeline))

# ---------------------------
# Analytics: User History
# ---------------------------
@app.get("/analytics/user/{user_id}")
def user_history(user_id: str):
    logs = list(collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(10))
    return logs