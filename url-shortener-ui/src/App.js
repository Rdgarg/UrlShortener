
import {useState, useEffect} from 'react';
import './App.css';
import { useAuth } from './AuthContext';

import GoogleSignIn from './GoogleSignIn';

// <script src="https://apis.google.com/js/platform.js" async defer></script>

function App() {
  const { token } = useAuth();
  const [tab, setTab] = useState('shorten');

  const [longUrl, setLongUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');

  const [shortInput, setShortInput] = useState('');
  const [stats, setStats] = useState([]);

  const handleShorten = async (e) => {
    e.preventDefault();
    try {
      console.log("In app.js")
      console.log(token)
      const res = await fetch(`https://api.my-short-url.com/shorten_url?url=${encodeURIComponent(longUrl)}`,{
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
      const data = await res.json();
      setShortUrl(data.short_url);
    } catch (error) {
      console.error('Error shortening URL:', error);
    }
  };

  const handleRedirect = async () => {
    try {
      const res = await fetch(`https://api.my-short-url.com/actual_url?url=${encodeURIComponent(shortInput)}`,{
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
      const data = await res.json();
      if (data.actual_url) {
        // window.location.href = data.actual_url;
        window.open(data.actual_url);
      } else {
        alert('Short URL not found.');
      }
    } catch (error) {
      console.error('Error redirecting:', error);
    }
  };

  useEffect(() => {
    if (tab === 'stats') {
      fetch('https://api.my-short-url.com/stats', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      })
          .then((res) => {
            if (!res.ok) {
              throw new Error('Network response was not ok');
            }
            return res.json();
      })
          .then((res) => res.json())
          .then((data) => setStats(data))
          .catch((err) => console.error('Error fetching stats:', err));
    }
  }, [tab]);

  return (
      <div className="App">
        <h1>URL Shortener</h1>
        <GoogleSignIn />
        <div style={{marginBottom: '1rem'}}>
          <button onClick={() => setTab('shorten')}>Shorten</button>
          <button onClick={() => setTab('redirect')}>Redirect</button>
          <button onClick={() => setTab('stats')}>Stats</button>
        </div>

        {tab === 'shorten' && (
            <form onSubmit={handleShorten}>
              <input
                  type="url"
                  placeholder="Enter long URL"
                  value={longUrl}
                  onChange={(e) => setLongUrl(e.target.value)}
                  required
              />
              <button type="submit">Shorten</button>
              {shortUrl && (
                  <p>
                    Shortened URL: <a href={shortUrl}>{shortUrl}</a>
                  </p>
              )}
            </form>
        )}

        {tab === 'redirect' && (
            <>
              <input
                  type="text"
                  placeholder="Enter short URL"
                  value={shortInput}
                  onChange={(e) => setShortInput(e.target.value)}
              />
              <button onClick={handleRedirect}>Redirect</button>
            </>
        )}

        {tab === 'stats' && (
            <div>
              <h2>Stats</h2>

              <input
                  type="text"
                  placeholder="Enter short URL (optional)"
                  value={shortInput}
                  onChange={(e) => setShortInput(e.target.value)}
              />
              <button
                  onClick={async () => {
                    const endpoint = shortInput
                        ? `https://api.my-short-url.com/stats?url=${encodeURIComponent(shortInput)}`
                        : `https://api.my-short-url.com/stats`;
                    try {
                      const res = await fetch(endpoint, {
                        method: 'GET',
                        headers: {
                          Authorization: `Bearer ${token}`,
                      }});
                      const data = await res.json();
                      // Ensure data is an array
                      setStats(Array.isArray(data) ? data : [data]);
                    } catch (err) {
                      console.error('Error fetching stats:', err);
                    }
                  }}
              >
                Get Stats
              </button>

              <br/><br/>

              {stats.length === 0 ? (
                  <p>No stats available.</p>
              ) : (
                  <table border="1" cellPadding="8">
                    <thead>
                    <tr>
                      <th>Short URL</th>
                      <th>Hits</th>
                      <th>Created at</th>
                    </tr>
                    </thead>
                    <tbody>
                    {stats.map((item, idx) => (
                        <tr key={idx}>
                          <td>{item.short_url}</td>
                          <td>{item.hits}</td>
                          <td>{new Date(item.timestamp).toLocaleString()}</td>
                        </tr>
                    ))}
                    </tbody>
                  </table>
              )}
            </div>
        )}

      </div>

  );
}

export default App;
