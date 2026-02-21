#sse_server.py

import asyncio
import json
import joblib
import pandas as pd
import numpy as np
from collections import deque
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import contextlib
from main_consumer import sensor_queue, start_mqtt

# --- ML Setup ---
MODEL_PATH = 'pdm_model.pkl'
SCALER_PATH = 'scaler.pkl'
BUFFER_SIZE = 20
constant_sensors = ['s_1','s_5','s_10','s_16','s_18','s_19']
feature_cols = [f's_{i}' for i in range(1,22) if f's_{i}' not in constant_sensors]

# Dictionary to store history for multiple engines {unit_nr: deque}
engine_buffers = {}

def calculate_fft_energy(signal):
    return np.mean(np.abs(np.fft.fft(signal)))

# Add this to your imports/setup
feature_names = joblib.load('feature_names.pkl')

def get_prediction(unit_nr, model, scaler):
    history = list(engine_buffers[unit_nr])
    if len(history) < BUFFER_SIZE:
        return None

    df = pd.DataFrame(history)
    latest_row_dict = df.iloc[-1].to_dict() # Start with raw data

    # 1. Calculate Rolling Means (Match training names)
    for s in feature_cols:
        latest_row_dict[f'{s}_rolling_mean'] = df[s].tail(10).mean()

    # 2. Calculate FFT (Match training names)
    latest_row_dict['s_7_fft_energy'] = calculate_fft_energy(df['s_7'])
    latest_row_dict['s_12_fft_energy'] = calculate_fft_energy(df['s_12'])

    # 3. CRITICAL: Convert to DataFrame and RE-ORDER columns
    input_df = pd.DataFrame([latest_row_dict])
    
    # This line ensures the order is EXACTLY what the model saw during training
    input_df = input_df[feature_names] 

    scaled = scaler.transform(input_df)
    prediction = model.predict(scaled)[0]
    return float(prediction)
# --- FastAPI App ---
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Load AI Artifacts
    app.state.model = joblib.load(MODEL_PATH)
    app.state.scaler = joblib.load(SCALER_PATH)
    mqtt_client = start_mqtt()
    yield
    mqtt_client.loop_stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

async def event_generator():
    while True:
        try:
            if not sensor_queue.empty():
                payload = sensor_queue.get_nowait()
                unit_nr = payload.get('unit_nr')

                # Maintain buffer for this specific unit
                if unit_nr not in engine_buffers:
                    engine_buffers[unit_nr] = deque(maxlen=BUFFER_SIZE)
                engine_buffers[unit_nr].append(payload)

                # Run Prediction
                rul = get_prediction(unit_nr, app.state.model, app.state.scaler)

                # Send combined data to Frontend
                out_payload = {
                    "sensor_data": payload,
                    "prediction": rul,
                    "is_ready": rul is not None,
                    "status": "CRITICAL" if (rul and rul < 25) else "OK"
                }

                yield {
                    "event": "sensor",
                    "data": json.dumps(out_payload)
                }
            else:
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Server Error: {e}")
            await asyncio.sleep(1)

@app.get("/stream")
async def stream():
    return EventSourceResponse(event_generator())