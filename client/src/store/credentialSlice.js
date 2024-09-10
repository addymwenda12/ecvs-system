import { createSlice } from '@reduxjs/toolkit';

const credentialSlice = createSlice({
  name: 'credentials',
  initialState: {
    list: [],
    isLoading: false,
    error: null,
  },
  reducers: {
    setCredentials: (state, action) => {
      state.list = action.payload;
    },
    addCredential: (state, action) => {
      state.list.push(action.payload);
    },
    updateCredential: (state, action) => {
      const index = state.list.findIndex(cred => cred.id === action.payload.id);
      if (index !== -1) {
        state.list[index] = action.payload;
      }
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const { setCredentials, addCredential, updateCredential, setLoading, setError } = credentialSlice.actions;
export default credentialSlice.reducer;