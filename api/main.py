import os
import socket
import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres-service"),
        database=os.getenv("DB_NAME", "webstackdb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "geheim123")
    )

@app.get("/api/name")
def get_name():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return {"name": row[0] if row else "Onbekend"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/container")
def get_container_id():
    return {"container_id": socket.gethostname()}

@app.get("/healthz")
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database unreachable")
