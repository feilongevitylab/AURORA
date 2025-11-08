import { createContext, useContext, useState } from 'react'

const ModeContext = createContext()

export const useMode = () => {
  const context = useContext(ModeContext)
  if (!context) {
    throw new Error('useMode must be used within a ModeProvider')
  }
  return context
}

export const MODES = {
  COMPANION: 'companion',
  MIRROR: 'mirror',
  SCIENCE: 'science'
}

export const MODE_CONFIG = {
  [MODES.COMPANION]: {
    name: 'Companion Mode',
    nameEn: 'Companion Mode',
    description: 'Warm emotional support and guided reflection',
    bgGradient: 'from-orange-400 via-pink-500 to-rose-500',
    bgColor: 'bg-gradient-to-br from-orange-50 to-pink-50',
    textColor: 'text-orange-900',
    icon: '🤗'
  },
  [MODES.MIRROR]: {
    name: 'Mirror Mode',
    nameEn: 'Mirror Mode',
    description: 'See your operating patterns across body, mind, and meaning',
    bgGradient: 'from-blue-500 via-indigo-600 to-purple-600',
    bgColor: 'bg-gradient-to-br from-blue-50 to-indigo-50',
    textColor: 'text-blue-900',
    icon: '🪞'
  },
  [MODES.SCIENCE]: {
    name: 'Science Exploration Mode',
    nameEn: 'Science Exploration Mode',
    description: 'Evidence-based analysis and scientific insight',
    bgGradient: 'from-cyan-500 via-blue-600 to-teal-600',
    bgColor: 'bg-gradient-to-br from-cyan-50 to-teal-50',
    textColor: 'text-cyan-900',
    icon: '🔬'
  }
}

export const ModeProvider = ({ children }) => {
  const [currentMode, setCurrentMode] = useState(MODES.COMPANION)

  const switchMode = (mode) => {
    if (Object.values(MODES).includes(mode)) {
      setCurrentMode(mode)
    }
  }

  return (
    <ModeContext.Provider value={{ currentMode, switchMode, modeConfig: MODE_CONFIG[currentMode] }}>
      {children}
    </ModeContext.Provider>
  )
}

