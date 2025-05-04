import React, { useState } from 'react';

const App = () => {
  const [currentView, setCurrentView] = useState('');

  const renderIframe = () => {
    if (!currentView) {
      return (
        <div style={{ marginTop: '40px', color: '#888', fontSize: '18px', textAlign: 'center' }}>
          Please select a dashboard above to view its content.
        </div>
      );
    }

    return (
      <iframe
        src={currentView}
        title="Dashboard View"
        width="100%"
        height="800px"
        style={{
          border: '1px solid #ccc',
          marginTop: '30px',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        }}
      />
    );
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '30px', backgroundColor: '#f4f4f4', minHeight: '100vh' }}>
      <h1 style={{ color: '#222', textAlign: 'center', marginBottom: '30px' }}>
        Unified Dashboard Portal
      </h1>

      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <button onClick={() => setCurrentView('http://127.0.0.1:8000/admin-dashboard/')} style={buttonStyle}>
          Admin Dashboard
        </button>
        <button onClick={() => setCurrentView('http://127.0.0.1:8000/end-user-dashboard/')} style={buttonStyle}>
          End-User Dashboard
        </button>
        <button onClick={() => setCurrentView('http://127.0.0.1:8000/ai-dashboard/')} style={buttonStyle}>
          AI Dashboard
        </button>
        <button onClick={() => setCurrentView('http://127.0.0.1:8000/finance-dashboard/')} style={buttonStyle}>
          Finance Dashboard
        </button>
      </div>

      {renderIframe()}
    </div>
  );
};

const buttonStyle = {
  margin: '0 10px',
  padding: '12px 20px',
  fontSize: '16px',
  backgroundColor: '#4CAF50',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  transition: 'background-color 0.3s ease',
};

export default App;
