import React, { useState, useEffect } from 'react';
import api from '../api/api';

function BlockchainInfo() {
  const [blockchainInfo, setBlockchainInfo] = useState(null);

  useEffect(() => {
    fetchBlockchainInfo();
  }, []);

  const fetchBlockchainInfo = async () => {
    try {
      const response = await api.get('/blockchain-info/');
      setBlockchainInfo(response.data);
    } catch (error) {
      console.error('Error fetching blockchain info:', error);
    }
  };

  if (!blockchainInfo) {
    return <div>Loading blockchain information...</div>;
  }

  return (
    <div>
      <h3>Blockchain Information</h3>
      <p>Network: {blockchainInfo.network}</p>
      <p>Latest Block: {blockchainInfo.latest_block}</p>
      <p>Gas Price: {blockchainInfo.gas_price} Gwei</p>
    </div>
  );
}

export default BlockchainInfo;