import { useMemo } from 'react'
import PropTypes from 'prop-types'
import { useAuth } from '../contexts/AuthContext'

function LandingPage({ onLearnMore }) {
  const { openAuthModal } = useAuth()

  const highlights = useMemo(
    () => [
      {
        title: 'Precision Longevity',
        body: 'Translate frontier aging biology into actionable insights designed for elite operators.',
      },
      {
        title: 'Energy Intelligence',
        body: 'Model how psychological stress and physiological aging compound to drain mind-body energy.',
      },
      {
        title: 'Strategic Health',
        body: 'Aurora transforms health management from crisis control to calm, continuous stewardship.',
      },
    ],
    []
  )

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.25),_transparent_55%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_rgba(99,102,241,0.3),_transparent_55%)]" />

      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6 py-16 sm:px-12">
        <div className="max-w-4xl text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.5em] text-sky-300/80">
            Aurora Longevity Advisory
          </p>
          <h1 className="mt-6 text-5xl font-bold tracking-tight sm:text-6xl md:text-7xl">AURORA</h1>
          <p className="mt-6 text-xl font-medium text-sky-200 sm:text-2xl">
            Energize with Intelligence. Longevity by Design.
          </p>
          <p className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-slate-200 sm:text-lg">
            Aurora is a premier longevity science advisory platform for elites. We translate complex aging biology
            through a systemic lens and accessible business metaphors, spotlighting how psychological stress and
            physiological aging synergize to erode mind-body energy.
            {onLearnMore && (
              <>
                {' '}
                <button
                  type="button"
                  onClick={onLearnMore}
                  className="inline-flex items-center gap-2 font-semibold text-sky-300 underline-offset-4 transition hover:text-sky-200 hover:underline"
                >
                  Learn more about Aurora
                  <span aria-hidden="true">→</span>
                </button>
              </>
            )}
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <button
              type="button"
              onClick={() => openAuthModal('sign-up')}
              className="rounded-full bg-white/95 px-8 py-3 text-sm font-semibold text-slate-900 shadow-xl shadow-sky-500/20 transition hover:-translate-y-0.5 hover:bg-white"
            >
              Sign Up
            </button>
            <button
              type="button"
              onClick={() => openAuthModal('sign-in')}
              className="rounded-full border border-white/60 px-8 py-3 text-sm font-semibold text-white/90 transition hover:border-white hover:text-white"
            >
              Sign In
            </button>
          </div>
        </div>

        <div className="mt-16 grid w-full max-w-5xl gap-6 sm:grid-cols-3">
          {highlights.map((item) => (
            <div
              key={item.title}
              className="rounded-3xl border border-white/10 bg-white/5 p-6 text-left shadow-lg shadow-slate-900/30 backdrop-blur"
            >
              <h3 className="text-sm font-semibold uppercase tracking-[0.3em] text-sky-300/80">{item.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-200/90">{item.body}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

LandingPage.propTypes = {
  onLearnMore: PropTypes.func,
}

LandingPage.defaultProps = {
  onLearnMore: undefined,
}

export default LandingPage

