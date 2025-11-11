import { useMode, MODES, MODE_CONFIG } from '../../contexts/ModeContext'

const MODE_TOOLTIPS = {
  [MODES.MIRROR]: "Ask Aurora to interpret your body’s energy patterns.",
  [MODES.SCIENCE]: "Let Aurora reveal evidence-based longevity intelligence.\nFrom frontier science to practical health strategy."
}

function ModeSwitch() {
  const { currentMode, switchMode } = useMode()

  const modes = [
    { key: MODES.MIRROR, config: MODE_CONFIG[MODES.MIRROR] },
    { key: MODES.SCIENCE, config: MODE_CONFIG[MODES.SCIENCE] }
  ]

  return (
    <div className="flex items-center justify-center gap-4 mb-8">
      {modes.map(({ key, config }) => {
        const tooltip = MODE_TOOLTIPS[key]
        const isMirror = key === MODES.MIRROR
        const tooltipPositionClasses = isMirror
          ? 'right-full mr-3 top-1/2 -translate-y-1/2'
          : 'left-full ml-3 top-1/2 -translate-y-1/2'
        const tooltipTextAlign = isMirror ? 'text-left' : 'text-left'
        return (
          <div key={key} className="relative group">
            <button
              type="button"
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
                <span className="hidden sm:inline">{config.name}</span>
                <span className="sm:hidden text-sm font-semibold uppercase tracking-wide">{config.nameEn || config.name}</span>
              </div>
            </button>
            {tooltip && (
              <div
                className={`
                  pointer-events-none absolute z-20 hidden w-64 rounded-2xl bg-slate-900/90 p-4 text-sm whitespace-normal
                  text-slate-100 shadow-xl ring-1 ring-white/10 group-hover:block ${tooltipPositionClasses} ${tooltipTextAlign}
                `}
              >
                {tooltip.split('\n').map((line, idx) => (
                  <p key={idx} className={idx > 0 ? 'mt-2 text-slate-300' : undefined}>
                    {line}
                  </p>
                ))}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default ModeSwitch

