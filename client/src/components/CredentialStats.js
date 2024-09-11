import React from 'react';
import { Bar } from 'react-chartjs-2';

function CredentialStats({ credentials }) {
  const institutionCounts = credentials.reduce((acc, cred) => {
    acc[cred.institution] = (acc[cred.institution] || 0) + 1;
    return acc;
  }, {});

  const data = {
    labels: Object.keys(institutionCounts),
    datasets: [
      {
        label: 'Credentials per Institution',
        data: Object.values(institutionCounts),
        backgroundColor: 'rgba(75,192,192,0.6)',
      },
    ],
  };

  return (
    <div>
      <h3>Credential Statistics</h3>
      <Bar data={data} />
    </div>
  );
}

export default CredentialStats;