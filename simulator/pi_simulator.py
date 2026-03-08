import time
import random
import requests

API_URL = "http://localhost:8000/api/analyze"

def generate_sensor_data():
    return {
        "age": 65,          
        "gender": 1,        
        "heartRate": round(random.uniform(70.0, 120.0), 1),
        "spo2": round(random.uniform(88.0, 99.0), 1),
        "systolic": round(random.uniform(110.0, 155.0), 1),
        "diastolic": round(random.uniform(70.0, 95.0), 1),
        "temperature": round(random.uniform(36.5, 38.5), 1)
    }

print("Starting Edge Sensor Simulator...")
while True:
    try:
        vitals = generate_sensor_data()
        response = requests.post(API_URL, json=vitals)
        if response.status_code == 200:
            print(f"Sent Vitals... AI Reply: {response.json()['Status']}")
    except requests.exceptions.ConnectionError:
        print("Waiting for FastAPI server...")
    time.sleep(3) # Simulating your 2-3 second sampling interval