import { useMode, MODE_CONFIG, MODES } from '../../contexts/ModeContext'

function DynamicBackground() {
  const { currentMode } = useMode()
  const config = MODE_CONFIG[currentMode]

  if (currentMode === MODES.MIRROR) {
    return (
      <div className="fixed inset-0 -z-10 overflow-hidden transition-all duration-700 ease-in-out">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.28),_transparent_55%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_rgba(99,102,241,0.32),_transparent_55%)]" />
        <div className="absolute top-1/4 left-1/5 h-72 w-72 rounded-full bg-sky-300/20 blur-3xl" />
        <div className="absolute bottom-1/4 right-1/5 h-72 w-72 rounded-full bg-indigo-400/20 blur-3xl" />
      </div>
    )
  }

  return (
    <div
      className={`fixed inset-0 -z-10 transition-all duration-700 ease-in-out ${config.bgGradient}`}
      style={{
        background: `linear-gradient(135deg, var(--tw-gradient-stops))`,
      }}
    >
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-0 h-96 w-96 animate-pulse rounded-full bg-white blur-3xl"></div>
        <div className="absolute bottom-0 right-0 h-96 w-96 animate-pulse rounded-full bg-white blur-3xl delay-1000"></div>
      </div>

      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/10"></div>
    </div>
  )
}

export default DynamicBackground

