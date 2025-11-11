import { useEffect, useState } from 'react'
import { ModeProvider, useMode, MODES } from './contexts/ModeContext'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import TopNav from './components/TopNav'
import HeroSection from './components/HeroSection/HeroSection'
import ContentArea from './components/Content/ContentArea'
import LandingPage from './components/LandingPage'

const createEmptyState = () =>
  Object.values(MODES).reduce((acc, mode) => {
    acc[mode] = null
    return acc
  }, {})

function AppContent() {
  const { currentMode } = useMode()
  const { isRegistered } = useAuth()
  const [responses, setResponses] = useState(() => createEmptyState())
  const [errors, setErrors] = useState(() => createEmptyState())
  const [loadingMode, setLoadingMode] = useState(null)
  const [hasSubmitted, setHasSubmitted] = useState(false)
  const [showLanding, setShowLanding] = useState(!isRegistered)

  useEffect(() => {
    setShowLanding(!isRegistered)
  }, [isRegistered])

  const handleResponse = (mode, data) => {
    setResponses((prev) => ({ ...prev, [mode]: data }))
    setErrors((prev) => ({ ...prev, [mode]: null }))
    setLoadingMode((prev) => (prev === mode ? null : prev))
    if (!hasSubmitted) {
      setHasSubmitted(true)
    }
  }

  const handleLoading = (mode, isLoading) => {
    setLoadingMode((prev) => {
      if (isLoading) {
        return mode
      }
      return prev === mode ? null : prev
    })
  }

  const handleError = (mode, err) => {
    setErrors((prev) => ({ ...prev, [mode]: err }))
    setLoadingMode((prev) => (prev === mode ? null : prev))
  }

  const currentResponse = responses[currentMode] || null
  const currentError = errors[currentMode] || null
  const isLoading = loadingMode === currentMode

  if (showLanding) {
    return (
      <>
        <TopNav isLanding />
        <LandingPage />
      </>
    )
  }

  return (
    <div className="relative min-h-screen">
      <TopNav />

      <HeroSection
        onResponse={handleResponse}
        onLoading={handleLoading}
        onError={handleError}
        hasSubmitted={hasSubmitted}
        responseData={currentResponse}
      />

      {hasSubmitted && (
        <div
          className={`
            relative z-10 bg-white min-h-screen px-4
            transition-all duration-700 ease-in-out
            py-8
          `}
        >
          <ContentArea data={currentResponse} loading={isLoading} error={currentError} />
        </div>
      )}
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <ModeProvider>
        <AppContent />
      </ModeProvider>
    </AuthProvider>
  )
}

export default App
