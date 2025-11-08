import { useState } from 'react'
import { ModeProvider } from './contexts/ModeContext'
import TopNav from './components/TopNav'
import HeroSection from './components/HeroSection/HeroSection'
import ContentArea from './components/Content/ContentArea'

function App() {
  const [responseData, setResponseData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [hasSubmitted, setHasSubmitted] = useState(false)

  const handleResponse = (data) => {
    setResponseData(data)
    setLoading(false)
    setError(null)
    if (!hasSubmitted) {
      setHasSubmitted(true)
    }
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
  }

  const handleError = (err) => {
    setError(err)
    setLoading(false)
  }

  return (
    <ModeProvider>
      <div className="relative min-h-screen">
        <TopNav />

        <HeroSection 
          onResponse={handleResponse}
          onLoading={handleLoading}
          onError={handleError}
          hasSubmitted={hasSubmitted}
          responseData={responseData}
        />
        
        {/* Content Area - Below Hero Section */}
        <div
          className={`
            relative z-10 bg-white min-h-screen px-4
            transition-all duration-700 ease-in-out
            ${hasSubmitted ? 'py-8' : 'py-16'}
          `}
        >
          <ContentArea 
            data={responseData}
            loading={loading}
            error={error}
          />
        </div>
      </div>
    </ModeProvider>
  )
}

export default App
