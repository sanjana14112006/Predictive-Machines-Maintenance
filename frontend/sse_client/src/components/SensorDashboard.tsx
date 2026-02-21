import React, { useState, useEffect } from 'react';

interface SensorPayload {
  sensor_data: any;
  prediction: number | null;
  is_ready: boolean;
  status: string;
}

const SensorDashboard: React.FC = () => {
  const [latestData, setLatestData] = useState<SensorPayload | null>(null);
  const [history, setHistory] = useState<SensorPayload[]>([]);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:8000/stream');

    eventSource.addEventListener('sensor', (event: MessageEvent) => {
      const parsed: SensorPayload = JSON.parse(event.data);
      setLatestData(parsed);
      setHistory(prev => [parsed, ...prev].slice(0, 10));
    });

    return () => eventSource.close();
  }, []);

  if (!latestData) return <div style={{padding: '20px'}}>Connecting to Factory Stream...</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#0c0c0c', minHeight: '100vh' }}>
      <h1>🏭 Factory AI Monitor</h1>
      
      {/* Top Metrics Cards */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ ...cardStyle, borderTop: '5px solid #3b82f6' }}>
          <h3>Unit Number</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>#{latestData.sensor_data.unit_nr}</p>
        </div>

        <div style={{ 
          ...cardStyle, 
          borderTop: `5px solid ${latestData.status === 'CRITICAL' ? '#ef4444' : '#10b981'}` 
        }}>
          <h3>Predicted RUL</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>
            {latestData.is_ready ? `${latestData.prediction?.toFixed(1)} Cycles` : "Calculating..."}
          </p>
          <small>{latestData.is_ready ? `Status: ${latestData.status}` : "Need 20 samples"}</small>
        </div>
      </div>

      {/* Mini Table for Recent Events */}
      <div style={cardStyle}>
        <h3>Recent Telemetry</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ textAlign: 'left', borderBottom: '1px solid #eee' }}>
              <th>Cycles</th>
              <th>Sensor 7</th>
              <th>Sensor 12</th>
              <th>RUL Prediction</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, i) => (
              <tr key={i} style={{ borderBottom: '1px solid #f1f1f1' }}>
                <td>{item.sensor_data.time_cycles}</td>
                <td>{item.sensor_data.s_7.toFixed(2)}</td>
                <td>{item.sensor_data.s_12.toFixed(2)}</td>
                <td style={{ color: item.status === 'CRITICAL' ? 'red' : 'green' }}>
                  {item.is_ready ? item.prediction?.toFixed(1) : '---'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const cardStyle: React.CSSProperties = {
  background: 'black',
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  flex: 1
};

export default SensorDashboard;