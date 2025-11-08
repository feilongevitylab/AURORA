import { useMode, MODE_CONFIG } from '../../contexts/ModeContext'

function DynamicBackground() {
  const { currentMode } = useMode()
  const config = MODE_CONFIG[currentMode]

  return (
    <div 
      className={`fixed inset-0 -z-10 transition-all duration-700 ease-in-out ${config.bgGradient}`}
      style={{
        background: `linear-gradient(135deg, var(--tw-gradient-stops))`,
      }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>
      
      {/* Gradient overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/10"></div>
    </div>
  )
}

export default DynamicBackground

