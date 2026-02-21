# Predictive Machines Maintenance: Factory AI Monitor

A real-time monitoring system that predicts the **Remaining Useful Life (RUL)** of industrial engines using Machine Learning.

## 🛠️ Technology Stack
- **AI/ML**: Python, Scikit-Learn (RUL Regression Model)
- **Backend**: FastAPI (Python), Uvicorn, Server-Sent Events (SSE)
- **Frontend**: React, Vite, Tailwind CSS
- **Data**: Real-time simulation via a Producer-Consumer architecture

## 🚀 How it Works
1. **Producer**: Simulates live sensor data (Cycles, Sensors 7 & 12) from factory engines.
2. **Backend**: Receives data and performs real-time inference using the `pdm_model.pkl` model.
3. **Frontend**: Displays a live dashboard with RUL predictions and engine health status via a stream.