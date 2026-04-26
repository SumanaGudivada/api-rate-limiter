# API Rate Limiter with Redis & MongoDB

## Overview
This project implements a high-performance API rate limiter using FastAPI, Redis, and MongoDB.

## Features
- Sliding window rate limiting using Redis
- FastAPI-based backend
- MongoDB logging and analytics
- Endpoints for usage insights

## Tech Stack
- FastAPI
- Redis
- MongoDB

## How it Works
Client → FastAPI → Redis (rate limiting) → MongoDB (logging)

## Endpoints
- `/api?user_id=123` → Access API
- `/analytics/top-users` → Top users
- `/analytics/status` → Allowed vs Blocked
- `/analytics/user/{id}` → User history

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
