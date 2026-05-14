import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

function App() {
  const [symbol, setSymbol] = useState('ABB'); // The active symbol
  const [companyData, setCompanyData] = useState(null);
  const [search, setSearch] = useState(''); // What the user is typing
  const [loading, setLoading] = useState(true);

  const fetchData = (targetSymbol) => {
    setLoading(true);
    axios.get(`http://127.0.0.1:8000/api/companies/${targetSymbol}/intelligence/`)
      .then(response => {
        setCompanyData(response.data);
        setLoading(false);
      })
      .catch(err => {
        alert("Company not found!");
        setLoading(false);
      });
  };

  // This triggers whenever the 'symbol' state changes
  useEffect(() => {
    fetchData(symbol);
  }, [symbol]);

  if (loading) return <div style={{ padding: '2rem' }}>Loading Financial Intelligence...</div>;
  if (!companyData) return <div style={{ padding: '2rem' }}>Error loading data. Is Django running?</div>;

  const { profile, profit_loss } = companyData;

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      
      {/* Search Bar */}
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

      {/* Profile Header */}
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
      
      <p style={{ color: '#555', lineHeight: '1.5', marginBottom: '3rem' }}>
        {profile.description}
      </p>

      {/* Interactive Recharts Graph */}
      <h2>Revenue vs Net Profit (₹ Crores)</h2>
      <div style={{ width: '100%', height: '400px', backgroundColor: '#f9f9f9', padding: '1rem', borderRadius: '8px' }}>
        <ResponsiveContainer>
          <LineChart data={profit_loss} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey={(val) => {
    // Check if the year is NaN, null, undefined, or "0"
                 const year = val.year;
                 if (!year || year === "0.0" || year === 0 || year === "NaN") {
                      return "N/A";
                 }
                 return year;
              }} 
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="revenue" 
              name="Revenue" 
              stroke="#8884d8" 
              strokeWidth={3} 
              activeDot={{ r: 8 }} 
            />
            <Line 
              type="monotone" 
              dataKey="net_profit" 
              name="Net Profit" 
              stroke="#82ca9d" 
              strokeWidth={3} 
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

export default App;