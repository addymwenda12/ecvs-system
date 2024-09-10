import React, { useState, useEffect } from 'react';
import { createCredential, verifyCredential, getCredentials } from '../api/api';
import BlockchainInfo from './BlockchainInfo';

function Dashboard({ user }) {
  const [credentials, setCredentials] = useState([]);
  const [newCredential, setNewCredential] = useState({
    degree: '',
    institution: '',
    date_issued: '',
    credential_id: '',
  });

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    try {
      const response = await getCredentials();
      setCredentials(response.data);
    } catch (error) {
      console.error('Error fetching credentials:', error);
    }
  };

  const handleCreateCredential = async (e) => {
    e.preventDefault();
    try {
      await createCredential(newCredential);
      fetchCredentials();
      setNewCredential({ degree: '', institution: '', date_issued: '', credential_id: '' });
    } catch (error) {
      console.error('Error creating credential:', error);
    }
  };

  const handleVerifyCredential = async (id) => {
    try {
      const response = await verifyCredential(id);
      alert(response.data.is_verified ? 'Credential verified!' : 'Credential not verified.');
    } catch (error) {
      console.error('Error verifying credential:', error);
    }
  };

  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <h3>Create New Credential</h3>
      <form onSubmit={handleCreateCredential}>
        <input
          type="text"
          value={newCredential.degree}
          onChange={(e) => setNewCredential({ ...newCredential, degree: e.target.value })}
          placeholder="Degree"
          required
        />
        <input
          type="text"
          value={newCredential.institution}
          onChange={(e) => setNewCredential({ ...newCredential, institution: e.target.value })}
          placeholder="Institution"
          required
        />
        <input
          type="date"
          value={newCredential.date_issued}
          onChange={(e) => setNewCredential({ ...newCredential, date_issued: e.target.value })}
          required
        />
        <input
          type="text"
          value={newCredential.credential_id}
          onChange={(e) => setNewCredential({ ...newCredential, credential_id: e.target.value })}
          placeholder="Credential ID"
          required
        />
        <button type="submit">Create Credential</button>
      </form>

      <h3>Your Credentials</h3>
      <ul>
        {credentials.map((credential) => (
          <li key={credential.id}>
            {credential.degree} - {credential.institution}
            <button onClick={() => handleVerifyCredential(credential.id)}>Verify</button>
          </li>
        ))}
      </ul>
      <BlockchainInfo />
    </div>
  );
}

export default Dashboard;