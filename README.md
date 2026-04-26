# API Rate Limiter with Redis & MongoDB

## Overview
This project implements a high-performance API rate limiter using FastAPI, Redis, and MongoDB.  
It uses a **sliding window algorithm** to control request rates efficiently and prevent burst traffic, while logging request data for analytics.

---

## Architecture

---

## Key Features
- Sliding window rate limiting using **Redis Sorted Sets**
- Optimized Redis operations using **pipelining**
- Low-latency request control using **in-memory data store**
- Persistent request logging with **MongoDB**
- Analytics APIs for monitoring usage patterns

---

## Tech Stack
- **FastAPI** – API framework
- **Redis** – real-time rate limiting
- **MongoDB** – logging & analytics
- **Uvicorn** – ASGI server

---

## Rate Limiting Strategy
This project uses a **Sliding Window Algorithm**:

- Each request timestamp is stored in a Redis Sorted Set
- Old requests outside the time window are removed
- Current request count is calculated dynamically
- Prevents burst traffic issues seen in fixed window approaches

---

## Why Redis?
- In-memory storage → **very low latency**
- Atomic operations → **safe under concurrency**
- Efficient data structures → ideal for rate limiting

---

## Why MongoDB?
- Stores large volumes of request logs
- Enables aggregation for analytics
- Decouples real-time processing from storage

---

## API Endpoints

### Rate Limiting
- `GET /api?user_id=123`  
  → Access API with rate limiting

---

### Analytics

- `GET /analytics/top-users`  
  → Returns top users by request count

- `GET /analytics/status`  
  → Shows allowed vs blocked requests

- `GET /analytics/user/{user_id}`  
  → Returns recent request history for a user

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
