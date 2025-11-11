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
  MIRROR: 'mirror',
  SCIENCE: 'science'
}

export const MODE_CONFIG = {
  [MODES.MIRROR]: {
    name: 'Energy Insight',
    nameEn: 'Energy Insight',
    description: 'Decode your energy rhythms across body, mind, and meaning',
    bgGradient: 'from-blue-500 via-indigo-600 to-purple-600',
    bgColor: 'bg-gradient-to-br from-blue-50 to-indigo-50',
    textColor: 'text-blue-900',
    icon: '⚡️'
  },
  [MODES.SCIENCE]: {
    name: 'Longevity Exploration',
    nameEn: 'Longevity Exploration',
    description: 'Evidence-based analysis to extend performance and recovery',
    bgGradient: 'from-cyan-500 via-blue-600 to-teal-600',
    bgColor: 'bg-gradient-to-br from-cyan-50 to-teal-50',
    textColor: 'text-cyan-900',
    icon: '🔬'
  }
}

export const ModeProvider = ({ children }) => {
  const [currentMode, setCurrentMode] = useState(MODES.MIRROR)

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

