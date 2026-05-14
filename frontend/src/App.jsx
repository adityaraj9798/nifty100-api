import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

function App() {
  const [symbol, setSymbol] = useState('ABB'); 
  const [companyData, setCompanyData] = useState(null);
  const [search, setSearch] = useState(''); 
  const [loading, setLoading] = useState(false); // Set to false initially if you want to show form first
  
  // Registration state
  const [email, setEmail] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);

  const BASE_URL = 'https://nifty100-api.onrender.com';

  // Registration Handler
  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${BASE_URL}/v1/b2b/register`, { email, businessName });
      setIsRegistered(true);
      fetchData(symbol); // Load data after registration
    } catch (error) {
      alert(`Registration failed: ${error.response?.data?.error || error.message}`);
    }
  };

  const fetchData = (targetSymbol) => {
    setLoading(true);
    axios.get(`${BASE_URL}/api/companies/${targetSymbol}/intelligence/`)
      .then(response => {
        setCompanyData(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        alert("Company not found or API connection error!");
        setLoading(false);
      });
  };

  useEffect(() => {
    if (isRegistered) fetchData(symbol);
  }, [symbol, isRegistered]);

  // UI: Show registration form if not registered
  if (!isRegistered) {
    return (
      <div style={{ maxWidth: '500px', margin: '50px auto', textAlign: 'center' }}>
        <h1>SkillPath B2B Portal</h1>
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <p>Register your business to access dashboard.</p>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={{padding:'10px'}} />
          <input type="text" placeholder="Business Name" value={businessName} onChange={(e) => setBusinessName(e.target.value)} required style={{padding:'10px'}} />
          <button type="submit" style={{ padding: '10px', backgroundColor: '#6366f1', color: 'white', border: 'none', cursor: 'pointer' }}>Register Business</button>
        </form>
      </div>
    );
  }

  if (loading) return <div style={{ padding: '2rem' }}>Loading Financial Intelligence...</div>;
  if (!companyData) return <div style={{ padding: '2rem' }}>Error loading data.</div>;

  const { profile, profit_loss } = companyData;

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem', display: 'flex', gap: '10px' }}>
        <input 
          type="text" 
          placeholder="Enter Symbol (e.g. ADANIENSOL)" 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: '8px', width: '200px' }}
        />
        <button onClick={() => setSymbol(search)} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Search
        </button>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
        <img 
           src={profile.logo_url} 
           alt={`${profile.company_name} logo`} 
           style={{ width: '80px', borderRadius: '8px', backgroundColor: '#e0e0e0' }} 
           onError={(e) => { e.target.src = `https://ui-avatars.com/api/?name=${profile.symbol}&background=random&size=80`; }} 
        />
        <div>
          <h1 style={{ margin: 0 }}>{profile.company_name} ({profile.symbol})</h1>
          <a href={profile.website} target="_blank" rel="noreferrer" style={{ color: '#0066cc' }}>Visit Website</a>
        </div>
      </div>
      
      <p style={{ color: '#555', lineHeight: '1.5', marginBottom: '3rem' }}>{profile.description}</p>

      <h2>Revenue vs Net Profit (₹ Crores)</h2>
      <div style={{ width: '100%', height: '400px', backgroundColor: '#f9f9f9', padding: '1rem', borderRadius: '8px' }}>
        <ResponsiveContainer>
          <LineChart data={profit_loss}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke="#8884d8" strokeWidth={3} />
            <Line type="monotone" dataKey="net_profit" stroke="#82ca9d" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;