import React, { useState } from 'react';
import { scanVerify } from '../api/api';
import './ScanVerify.css';

const ScanVerify = () => {
  const [identifier, setIdentifier] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    try {
      const response = await scanVerify(identifier);
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError('Credential or institution not found');
      setResult(null);
    }
  };

  return (
    <div className="scan-verify">
      <h2>Scan and Verify Credential</h2>
      <input
        type="text"
        value={identifier}
        onChange={(e) => setIdentifier(e.target.value)}
        placeholder="Enter Credential ID or Institution Name"
      />
      <button onClick={handleScan}>Scan</button>
      {result && (
        <div className="result">
          <h3>Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default ScanVerify;