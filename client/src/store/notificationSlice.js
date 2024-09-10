import { createSlice } from '@reduxjs/toolkit';

const notificationSlice = createSlice({
  name: 'notifications',
  initialState: {
    list: [],
  },
  reducers: {
    addNotification: (state, action) => {
      state.list.push(action.payload);
    },
    removeNotification: (state, action) => {
      state.list = state.list.filter(notif => notif.id !== action.payload);
    },
  },
});

export const { addNotification, removeNotification } = notificationSlice.actions;
export default notificationSlice.reducer;