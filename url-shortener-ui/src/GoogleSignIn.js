

import { useEffect } from 'react';
import {useAuth} from "./AuthContext";

function GoogleSignIn() {
  const { setToken } = useAuth();
  useEffect(() => {
    // Define the callback function first
    const handleCredentialResponse = (response) => {
      console.log("Encoded JWT ID token: " + response.credential);
      fetch('http://34.57.93.16/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({token: response.credential}),
      }).then(r => {
          console.log(r);
          setToken(response.credential);
      }
      ).catch(e => console.log(e));
      // You can decode or send this token to your backend for authentication
    };

    // Initialize and render the sign-in button
    if (window.google && window.google.accounts) {
      window.google.accounts.id.initialize({
        client_id: '251182287536-srbj0sbra4rtlh0prd5j7qobgd7u4frs.apps.googleusercontent.com',
        callback: handleCredentialResponse,
      });

      window.google.accounts.id.renderButton(
        document.getElementById('g_id_signin'),
        { theme: 'outline', size: 'large' }
      );

      // Optional: Enable One Tap
      // window.google.accounts.id.prompt();
    }
  }, [setToken]);

  return (
    <div>
      <div id="g_id_signin"></div>
    </div>
  );
}

export default GoogleSignIn;

