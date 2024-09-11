import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { verifyCredential } from '../api/api';
import { updateCredential } from '../store/credentialSlice';
import { addNotification } from '../store/notificationSlice';

function EmployerInterface() {
  const dispatch = useDispatch();
  const [credentialId, setCredentialId] = useState('');

  const handleVerify = async () => {
    try {
      const response = await verifyCredential(credentialId);
      dispatch(updateCredential(response.data));
      dispatch(addNotification({ id: Date.now(), message: 'Credential verified successfully' }));
    } catch (error) {
      console.error('Error verifying credential:', error);
    }
  };

  return (
    <div>
      <h2>Verify Credential</h2>
      <input
        type="text"
        value={credentialId}
        onChange={(e) => setCredentialId(e.target.value)}
        placeholder="Enter Credential ID"
      />
      <button onClick={handleVerify}>Verify</button>
    </div>
  );
}

export default EmployerInterface;