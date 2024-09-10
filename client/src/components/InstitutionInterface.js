import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addCredential } from '../store/credentialSlice';
import { createCredential } from '../api/api';
import { addNotification } from '../store/notificationSlice';

function InstitutionInterface() {
  const dispatch = useDispatch();
  const [newCredential, setNewCredential] = useState({
    degree: '',
    institution: '',
    date_issued: '',
    credential_id: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createCredential(newCredential);
      dispatch(addCredential(response.data));
      dispatch(addNotification({ id: Date.now(), message: 'New credential issued successfully' }));
      setNewCredential({ degree: '', institution: '', date_issued: '', credential_id: '' });
    } catch (error) {
      console.error('Error creating credential:', error);
    }
  };

  return (
    <div>
      <h2>Issue New Credential</h2>
      <form onSubmit={handleSubmit}>
        {/* Add form inputs for newCredential fields */}
        <button type="submit">Issue Credential</button>
      </form>
    </div>
  );
}

export default InstitutionInterface;