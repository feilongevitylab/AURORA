import { useMode, MODES } from '../../contexts/ModeContext'
import DynamicBackground from '../Background/DynamicBackground'
import ModeSwitch from './ModeSwitch'
import ChatbotInput from './ChatbotInput'
import AuroraLogo from './AuroraLogo'
import { useEffect, useMemo, useState } from 'react'

const DEFAULT_PROMPTS = {
  [MODES.COMPANION]: {
    placeholder: 'In Companion Mode, tell me what is on your heart today.',
    quickPrompts: [],
  },
  [MODES.MIRROR]: {
    placeholder: 'Good day - your rhythm feels steady. What would you like to reflect on?',
    quickPrompts: ["I'm feeling a little tired.", "I'm doing alright.", "Show me today's mirror."],
  },
  [MODES.SCIENCE]: {
    placeholder: 'In Science Exploration Mode, ask me about physiology or psychology.',
    quickPrompts: [],
  },
}

function HeroSection({ onResponse, onLoading, onError, hasSubmitted, responseData }) {
  const { modeConfig, currentMode } = useMode()
  const [placeholder, setPlaceholder] = useState(DEFAULT_PROMPTS[currentMode].placeholder)
  const [quickPrompts, setQuickPrompts] = useState(DEFAULT_PROMPTS[currentMode].quickPrompts)

  const timeGreeting = useMemo(() => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Good morning'
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
  }, [])

  useEffect(() => {
    const defaults = DEFAULT_PROMPTS[currentMode] || DEFAULT_PROMPTS[MODES.COMPANION]

    if (currentMode === MODES.MIRROR) {
      const dynamicGreeting =
        responseData?.hero?.greeting ||
        `${timeGreeting}, your rhythm feels steady today. Ready to listen to what your body is saying?`
      const promptList =
        responseData?.hero?.quick_prompts && responseData.hero.quick_prompts.length > 0
          ? responseData.hero.quick_prompts
          : defaults.quickPrompts

      setPlaceholder(dynamicGreeting)
      setQuickPrompts(promptList)
    } else {
      setPlaceholder(defaults.placeholder)
      setQuickPrompts(defaults.quickPrompts)
    }
  }, [currentMode, responseData, timeGreeting])

  return (
    <div 
      className={`
        relative flex flex-col items-center justify-center px-4
        transition-all duration-700 ease-in-out
        ${hasSubmitted 
          ? 'min-h-[50vh] py-8' 
          : 'min-h-screen py-16'
        }
      `}
    >
      <DynamicBackground />
      
      {/* Aurora Logo - Top Left (only when hasSubmitted) */}
      {hasSubmitted && <AuroraLogo />}
      
      {/* Hero Content */}
      <div className="relative z-10 w-full max-w-6xl mx-auto text-center">
        {/* Title - Hidden when hasSubmitted */}
        {!hasSubmitted && (
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 drop-shadow-lg transition-opacity duration-500">
            AURORA
          </h1>
        )}
        
        {/* Subtitle - Hidden when hasSubmitted */}
        {!hasSubmitted && (
          <p className="text-xl md:text-2xl text-white/90 mb-8 drop-shadow-md transition-opacity duration-500">
            {modeConfig.description}
          </p>
        )}
        
        {/* Mode Switch */}
        <div className={hasSubmitted ? 'mt-4' : ''}>
          <ModeSwitch />
        </div>
        
        {/* Chatbot Input - Position adjusts based on hasSubmitted */}
        <div className={hasSubmitted ? 'mt-6' : 'mt-12'}>
          <div className={hasSubmitted ? 'max-w-2xl mx-auto' : ''}>
            <ChatbotInput 
              onResponse={onResponse} 
              onError={onError}
              compact={hasSubmitted}
              placeholder={placeholder}
              quickPrompts={quickPrompts}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default HeroSection

