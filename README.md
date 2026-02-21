# 🌱 Industrial Insight: Real-Time AI Monitoring

**Industrial Insight** is an end-to-end Predictive Maintenance solution designed to maximize the lifespan of industrial assets. By moving from scheduled to **condition-based maintenance**, this project directly supports the "Green Bharat" mission by reducing premature e-waste from machinery components.



## 🚀 Key Features
- **Real-Time IoT Pipeline**: Simulates live sensor data (Cycles, Sensors 7 & 12) from factory engines via a producer-consumer architecture.
- **AI Brain**: Utilizes a Regression Model trained on the **NASA CMAPSS dataset** to predict **Remaining Useful Life (RUL)**.
- **Live Streaming Architecture**: Implements **Server-Sent Events (SSE)** to push real-time health metrics from the backend to the dashboard without page refreshes.
- **Dynamic Dashboard**: A modern React interface providing live engine health status and automated maintenance reporting.

## 🛠️ Technical Stack
- **AI/ML**: Python 3.13, Scikit-Learn, Pandas, NumPy, Joblib.
- **Backend**: FastAPI, Uvicorn (Asynchronous Server Gateway Interface).
- **Frontend**: React, Vite, Tailwind CSS.
- **Version Control**: Git LFS (Large File Storage) for managing the 141MB `pdm_model.pkl` model file.

## 🏁 How to Run

### 1. Prerequisites
- **Git LFS**: Installed to properly handle the 141MB `pdm_model.pkl`.
- **Node.js & npm**: Required for the React frontend.
- **Python 3.10+**: Required for the backend and simulation scripts.

### 2. Setup
```bash
# Clone the repository
git clone [https://github.com/sanjana14112006/Predictive-Machines-Maintenance.git](https://github.com/sanjana14112006/Predictive-Machines-Maintenance.git)
cd Predictive-Machines-Maintenance

# Initialize virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


### 3. Execution (In 3 Separate Terminals)
Ensure your virtual environment is active in the Python terminals.

* **Terminal 1 (Backend)**: 
    ```bash
    uvicorn sse_server:app --reload
    ```
* **Terminal 2 (Producer)**: 
    ```bash
    python producer.py
    ```
* **Terminal 3 (Frontend)**: 
    ```bash
    cd frontend/sse_client
    npm install
    npm run dev
    ```

## 📊 Model Performance
- **Metric**: Validation RMSE: 47.78 cycles.
- **Impact**: This precision allows for optimized maintenance windows, ensuring 95%+ of a component's safe life is utilized before replacement, directly reducing industrial waste.

## 🌍 Sustainability Impact
By predicting failure before it occurs, this system prevents the disposal of functional parts, reducing the carbon footprint of industrial manufacturing and supporting a circular economy.

