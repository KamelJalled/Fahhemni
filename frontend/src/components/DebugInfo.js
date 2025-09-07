import React from 'react';

const DebugInfo = () => {
  return (
    <div style={{ 
      position: 'absolute', 
      top: '100px', 
      left: '10px', 
      background: 'yellow', 
      padding: '10px', 
      fontSize: '12px',
      zIndex: 1000
    }}>
      <div><strong>Debug Info:</strong></div>
      <div>Backend URL: {process.env.REACT_APP_BACKEND_URL || 'UNDEFINED'}</div>
      <div>Environment: {process.env.NODE_ENV || 'UNDEFINED'}</div>
    </div>
  );
};

export default DebugInfo;