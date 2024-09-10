import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../store/credentialSlice';
import { getCredentials } from '../api/api';

function SearchBar() {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useDispatch();

  const handleSearch = async () => {
    try {
      const response = await getCredentials(searchTerm);
      dispatch(setCredentials(response.data));
    } catch (error) {
      console.error('Error searching credentials:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search credentials or users"
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchBar;