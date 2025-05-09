import { useState } from 'react';
import './App.css';

function App() {
  const [longUrl, setLongUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [shortInput, setShortInput] = useState('');

  const handleShorten = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://34.57.93.16//shorten_url?url=${encodeURIComponent(longUrl)}`);
      const data = await res.json();
      setShortUrl(data.short_url);
    } catch (error) {
      console.error('Error shortening URL:', error);
    }
  };

  const handleRedirect = async () => {
    try {
      const res = await fetch(`http://34.57.93.16/actual_url?url=${encodeURIComponent(shortInput)}`);
      const data = await res.json();
      if (data.actual_url) {
        window.location.href = data.actual_url;
      } else {
        alert('Short URL not found.');
      }
    } catch (error) {
      console.error('Error redirecting:', error);
    }
  };

  return (
    <div className="App">
      <h1>URL Shortener</h1>

      <form onSubmit={handleShorten}>
        <input
          type="url"
          placeholder="Enter long URL"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
          required
        />
        <button type="submit">Shorten</button>
      </form>

      {shortUrl && (
        <p>
          Shortened URL: <a href={shortUrl}>{shortUrl}</a>
        </p>
      )}

      <hr />

      <h2>Redirect using Short URL</h2>
      <input
        type="text"
        placeholder="Enter short URL"
        value={shortInput}
        onChange={(e) => setShortInput(e.target.value)}
      />
      <button onClick={handleRedirect}>Redirect</button>
    </div>
  );
}

export default App;
