import React, { useState, useEffect } from 'react';
import { getWalletBalance, generateWalletAddress } from '../api/api';

function Wallet() {
  const [balance, setBalance] = useState(0);
  const [address, setAddress] = useState('');

  useEffect(() => {
    fetchWalletBalance();
  }, []);

  const fetchWalletBalance = async () => {
    try {
      const response = await getWalletBalance();
      setBalance(response.data.balance);
      setAddress(response.data.address);
    } catch (error) {
      console.error('Error fetching wallet balance:', error);
    }
  };

  const handleGenerateAddress = async () => {
    try {
      const response = await generateWalletAddress();
      setAddress(response.data.address);
      fetchWalletBalance();
    } catch (error) {
      console.error('Error generating wallet address:', error);
    }
  };

  return (
    <div>
      <h2>Your Wallet</h2>
      <p>Balance: {balance} ETH</p>
      <p>Address: {address}</p>
      <button onClick={handleGenerateAddress}>Generate New Address</button>
    </div>
  );
}

export default Wallet;