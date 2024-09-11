import React from 'react';

function CredentialList({ credentials }) {
  return (
    <div>
      <h2>Credentials</h2>
      <ul>
        {credentials.map((credential) => (
          <li key={credential.id}>{credential.degree} - {credential.institution}</li>
        ))}
      </ul>
    </div>
  );
}

export default CredentialList;