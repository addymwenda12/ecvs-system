import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setCredentials } from '../store/credentialSlice';
import { getCredentials } from '../api/api';
import CredentialList from './CredentialList';
import CredentialStats from './CredentialStats';
import SearchBar from './SearchBar';

function Dashboard() {
  const dispatch = useDispatch();
  const { currentUser } = useSelector(state => state.user);
  const { list: credentials } = useSelector(state => state.credentials);

  useEffect(() => {
    const fetchCredentials = async () => {
      try {
        const response = await getCredentials();
        dispatch(setCredentials(response.data));
      } catch (error) {
        console.error('Error fetching credentials:', error);
      }
    };
    fetchCredentials();
  }, [dispatch]);

  return (
    <div>
      <h2>Welcome, {currentUser.username}!</h2>
      <SearchBar />
      <CredentialList credentials={credentials} />
      <CredentialStats credentials={credentials} />
    </div>
  );
}

export default Dashboard;