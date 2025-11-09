import { useState, useRef, useEffect } from 'react'
import { useMode } from '../../contexts/ModeContext'
import { useAuth } from '../../contexts/AuthContext'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function ChatbotInput({ onResponse, onError, onLoading, compact = false, placeholder, quickPrompts = [] }) {
  const { currentMode } = useMode()
  const { isRegistered, userProfile } = useAuth()
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showScrollbar, setShowScrollbar] = useState(false)
  const [scrollIndicator, setScrollIndicator] = useState({
    trackHeight: 0,
    thumbHeight: 0,
    thumbTop: 0,
    topOffset: 0,
  })
  const textareaRef = useRef(null)

  const submitQuery = async (text, preserve = false) => {
    const trimmed = text.trim()
    if (!trimmed) {
      return
    }
    try {
      setLoading(true)
      if (onLoading) {
        onLoading(true)
      }
      setError(null)
      
      const response = await axios.post(`${API_BASE_URL}/api/insight`, {
        query: trimmed,
        mode: currentMode,
        user_id: userProfile?.id || null,
        is_registered: isRegistered,
      })
      
      if (onResponse) {
        onResponse(response.data)
      }
      if (!preserve) {
        setQuery('')
      }
    } catch (err) {
      console.error('Error fetching insight:', err)
      const errorMessage = err.response?.data?.detail || err.message
      setError(errorMessage)
      if (onError) {
        onError(errorMessage)
      }
    } finally {
      setLoading(false)
      if (onLoading) {
        onLoading(false)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await submitQuery(query)
  }

  const updateScrollIndicatorMetrics = () => {
    const textarea = textareaRef.current
    if (!textarea) {
      return
    }

    if (!showScrollbar) {
      setScrollIndicator({
        trackHeight: 0,
        thumbHeight: 0,
        thumbTop: 0,
        topOffset: 0,
      })
      return
    }

    const { scrollHeight, clientHeight, scrollTop } = textarea
    const topPadding = compact ? 12 : 16
    const buttonReservedSpace = compact ? 54 : 70
    const availableHeight = Math.max(clientHeight - topPadding - buttonReservedSpace, 24)

    const visibleRatio = clientHeight / scrollHeight
    const thumbHeight = Math.max(availableHeight * visibleRatio, 10)
    const scrollableHeight = scrollHeight - clientHeight
    const maxThumbTop = availableHeight - thumbHeight
    const thumbTop = scrollableHeight > 0 ? maxThumbTop * (scrollTop / scrollableHeight) : 0

    setScrollIndicator({
      trackHeight: availableHeight,
      thumbHeight,
      thumbTop,
      topOffset: topPadding,
    })
  }

  // Auto-resize textarea based on content and check if scrollbar is needed
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      const scrollHeight = textareaRef.current.scrollHeight
      const maxHeight = compact ? 120 : 200 // max-h based on compact mode
      const currentHeight = Math.min(scrollHeight, maxHeight)
      textareaRef.current.style.height = `${currentHeight}px`

      // Check if scrollbar is needed (content exceeds max height)
      const needsScrollbar = scrollHeight > maxHeight
      setShowScrollbar(needsScrollbar)
      if (!needsScrollbar) {
        setScrollIndicator({
          trackHeight: 0,
          thumbHeight: 0,
          thumbTop: 0,
          topOffset: 0,
        })
      }
    }
  }, [query, compact])

  // Update custom scrollbar indicator position and size
  useEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) return

    updateScrollIndicatorMetrics()
    textarea.addEventListener('scroll', updateScrollIndicatorMetrics)
    window.addEventListener('resize', updateScrollIndicatorMetrics)

    return () => {
      textarea.removeEventListener('scroll', updateScrollIndicatorMetrics)
      window.removeEventListener('resize', updateScrollIndicatorMetrics)
    }
  }, [showScrollbar, compact])

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleChange = (e) => {
    setQuery(e.target.value)
  }

  const handlePromptClick = async (prompt) => {
    if (loading) return
    setQuery(prompt)
    await submitQuery(prompt, true)
  }

  return (
    <div className={`w-full ${compact ? 'max-w-2xl' : 'max-w-3xl'} mx-auto transition-all duration-500`}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={query}
            onChange={handleChange}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            disabled={loading}
            rows={1}
            className={`
              chat-textarea
              w-full
              bg-white/90 backdrop-blur-md
              border-2 border-white/50
              rounded-2xl
              text-gray-900 placeholder-gray-500
              focus:outline-none focus:ring-4 focus:ring-white/50
              disabled:opacity-50 disabled:cursor-not-allowed
              shadow-xl
              transition-all duration-500
              resize-none
              overflow-y-auto
              pr-20
              ${compact 
                ? 'pl-4 py-2.5 text-sm min-h-[44px] max-h-[120px]' 
                : 'pl-6 py-4 min-h-[56px] max-h-[200px]'
              }
            `}
            style={{
              height: 'auto',
              lineHeight: '1.5',
              scrollbarWidth: 'none',
              msOverflowStyle: 'none',
            }}
          />

          {showScrollbar && scrollIndicator.trackHeight > 0 && (
            <div
              className="absolute right-5 flex justify-center"
              style={{
                top: scrollIndicator.topOffset,
              }}
            >
              <div
                className="relative w-1.5 bg-white/30 rounded-full overflow-hidden"
                style={{
                  height: scrollIndicator.trackHeight,
                }}
              >
                <div
                  className="absolute left-0 right-0 bg-white rounded-full shadow-sm"
                  style={{
                    top: scrollIndicator.thumbTop,
                    height: scrollIndicator.thumbHeight,
                  }}
                ></div>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className={`
              absolute right-3
              bg-gradient-to-r from-blue-600 to-indigo-600
              text-white
              rounded-full
              hover:from-blue-700 hover:to-indigo-700
              disabled:opacity-60 disabled:cursor-not-allowed
              transition-all duration-200
              shadow-lg hover:shadow-xl
              flex items-center justify-center
              ${compact 
                ? 'w-9 h-9 bottom-2' 
                : 'w-11 h-11 bottom-3'
              }
            `}
            title="Send"
          >
            {loading ? (
              <div className={`animate-spin rounded-full border-b-2 border-white ${compact ? 'h-4 w-4' : 'h-5 w-5'}`}></div>
            ) : (
              <svg 
                className={`${compact ? 'w-4 h-4' : 'w-5 h-5'}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </button>
        </div>
        
        {error && (
          <div className="mt-2 px-4 py-2 bg-red-100 border border-red-300 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}
      </form>

      {quickPrompts.length > 0 && (
        <div className="mt-4 flex flex-wrap justify-center gap-3">
          {quickPrompts.map((prompt, index) => (
            <button
              key={`${prompt}-${index}`}
              type="button"
              onClick={() => handlePromptClick(prompt)}
              disabled={loading}
              className={`
                rounded-full border px-4 py-2 text-sm transition
                ${loading ? 'cursor-not-allowed border-white/30 text-white/40' : 'border-white/60 text-white hover:border-white hover:bg-white/10'}
              `}
            >
              {prompt}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default ChatbotInput

