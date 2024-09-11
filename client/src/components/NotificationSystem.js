import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { removeNotification } from '../store/notificationSlice';

function NotificationSystem() {
  const dispatch = useDispatch();
  const notifications = useSelector(state => state.notifications.list);

  return (
    <div className="notification-system">
      {notifications.map(notif => (
        <div key={notif.id} className="notification">
          {notif.message}
          <button onClick={() => dispatch(removeNotification(notif.id))}>Dismiss</button>
        </div>
      ))}
    </div>
  );
}

export default NotificationSystem;