import { useMode, MODES, MODE_CONFIG } from '../../contexts/ModeContext'

function ModeSwitch() {
  const { currentMode, switchMode } = useMode()

  const modes = [
    { key: MODES.COMPANION, config: MODE_CONFIG[MODES.COMPANION] },
    { key: MODES.MIRROR, config: MODE_CONFIG[MODES.MIRROR] },
    { key: MODES.SCIENCE, config: MODE_CONFIG[MODES.SCIENCE] }
  ]

  return (
    <div className="flex items-center justify-center gap-4 mb-8">
      {modes.map(({ key, config }) => (
        <button
          key={key}
          onClick={() => switchMode(key)}
          className={`
            relative px-6 py-3 rounded-xl font-semibold transition-all duration-300
            ${currentMode === key
              ? 'bg-white text-gray-900 shadow-lg scale-105'
              : 'bg-white/20 text-white hover:bg-white/30 backdrop-blur-sm'
            }
          `}
        >
          <div className="flex items-center gap-2">
            <span className="text-xl">{config.icon}</span>
            <span className="hidden sm:inline">{config.name}</span>
            <span className="sm:hidden">{config.icon}</span>
          </div>
        </button>
      ))}
    </div>
  )
}

export default ModeSwitch

