# File: health_data_api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class HealthData(BaseModel):
    average_heart_rate: float
    average_temperature: float
    average_ecg: float
    average_spo2: float


def get_average_sensor_data(user_id: int, days: int = 7):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    seven_days_ago = datetime.now() - timedelta(days=days)

    c.execute("""
        SELECT 
            AVG(heart_rate) as avg_hr,
            AVG(temperature) as avg_temp,
            AVG(ecg) as avg_ecg,
            AVG(spo2) as avg_spo2
        FROM sensor_data
        WHERE user_id = ? AND timestamp >= ?
    """, (user_id, seven_days_ago))

    result = c.fetchone()
    conn.close()

    if result[0] is None:
        return None

    return HealthData(
        average_heart_rate=result[0],
        average_temperature=result[1],
        average_ecg=result[2],
        average_spo2=result[3]
    )


@app.get("/api/health_data/{user_id}")
async def health_data_api(user_id: int):
    data = get_average_sensor_data(user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="No data found for this user")
    return data


