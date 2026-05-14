import { useState } from 'react';
import axios from 'axios';

function App() {
  const [email, setEmail] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [userId, setUserId] = useState(null);
  const [apiKeyData, setApiKeyData] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');

  // Your live Render backend URL
  const BASE_URL = 'https://nifty100-api.onrender.com';

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // FIX THIS LINE BELOW:
      const response = await axios.post('https://nifty100-api.onrender.com/api/register/', { 
          email, 
          businessName 
      });
      setIsRegistered(true);
      fetchData(symbol);
    } catch (error) {
      alert(`Registration failed: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleGenerateKey = async () => {
    setStatusMessage('Generating key...');
    try {
      const response = await axios.post(`${BASE_URL}/v1/b2b/keys/generate`, {
        userId: userId
      });
      setApiKeyData(response.data.data);
      setStatusMessage('Key generated successfully!');
    } catch (error) {
      setStatusMessage('Failed to generate key.');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '50px auto', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <h1>SkillPath B2B Portal</h1>
      
      {!userId ? (
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <p>Register your business to get started.</p>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={{padding:'10px'}} />
          <input type="text" placeholder="Business Name" value={businessName} onChange={(e) => setBusinessName(e.target.value)} required style={{padding:'10px'}} />
          <button type="submit" style={{ padding: '10px', backgroundColor: '#6366f1', color: 'white', border: 'none', cursor: 'pointer' }}>Register Business</button>
        </form>
      ) : (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
          <h3>Welcome, {businessName}!</h3>
          <p>User ID: {userId}</p>
          {!apiKeyData ? (
            <button onClick={handleGenerateKey} style={{ padding: '10px 20px', backgroundColor: '#10b981', color: 'white', border: 'none', cursor: 'pointer' }}>Generate My API Key</button>
          ) : (
            <div style={{ textAlign: 'left', backgroundColor: '#f9fafb', padding: '15px', marginTop: '10px' }}>
              <p><strong>API Key:</strong> <code>{apiKeyData.apiKey}</code></p>
              <p style={{ color: 'red', fontSize: '12px' }}><strong>Secret (Copy now!):</strong> <code>{apiKeyData.apiSecret}</code></p>
            </div>
          )}
        </div>
      )}

      {statusMessage && <p style={{ marginTop: '20px', color: '#666' }}>{statusMessage}</p>}
    </div>
  );
}

export default App;