import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';
import credentialReducer from './credentialSlice';
import notificationReducer from './notificationSlice';

export const store = configureStore({
  reducer: {
    user: userReducer,
    credentials: credentialReducer,
    notifications: notificationReducer,
  },
});