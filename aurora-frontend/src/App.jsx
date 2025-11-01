import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    // Check backend connection
    axios.get('http://localhost:8000/health')
      .then(() => setStatus('connected'))
      .catch(() => setStatus('disconnected'))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AURORA
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            AI-powered Data Analysis Platform
          </p>
          <div className={`inline-block px-6 py-3 rounded-lg ${
            status === 'connected' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            Backend: {status === 'connected' ? 'Connected' : 'Disconnected'}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

