import PropTypes from 'prop-types'

function AboutAurora({ onBack, onStart }) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.25),_transparent_55%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_rgba(99,102,241,0.3),_transparent_55%)]" />
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-0 h-96 w-96 animate-pulse rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 h-96 w-96 animate-pulse delay-1000 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto flex min-h-screen max-w-5xl flex-col gap-10 px-6 py-16 sm:px-10">
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={onBack}
            className="flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm font-semibold text-white transition hover:bg-white/20"
          >
            <span aria-hidden="true">←</span>
            Back
          </button>
          <button
            type="button"
            onClick={onStart}
            className="rounded-full bg-white/95 px-5 py-2 text-sm font-semibold text-slate-900 shadow-lg shadow-sky-500/20 transition hover:-translate-y-0.5 hover:bg-white"
          >
            Experience Aurora
          </button>
        </div>

        <header className="text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.5em] text-sky-300/80">About Aurora</p>
          <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">Aurora</h1>
          <p className="mt-4 text-lg text-sky-100/90 sm:text-xl">
            Aurora is a premier, AI-powered longevity science advisory platform designed for visionaries and elites who
            seek to understand and optimize the biology of their lifespan.
          </p>
        </header>

        <section className="space-y-6 rounded-3xl border border-white/20 bg-white/5 p-8 text-slate-100 shadow-2xl shadow-slate-900/40 backdrop-blur">
          <p className="leading-relaxed text-slate-100/90">
            We translate the complex language of aging science through a systemic lens and accessible business metaphors,
            revealing how psychological stress and physiological aging coalesce to drain energy, resilience, and clarity
            of mind. Aurora bridges the gap between frontier biology and lived human experience — transforming abstract
            science into actionable wisdom for modern leaders.
          </p>
          <p className="leading-relaxed text-slate-100/90">
            Our mission is to help you see the invisible forces shaping your vitality — and to empower you with the
            knowledge and tools to extend both healthspan and performance.
          </p>
        </section>

        <section className="rounded-3xl border border-white/25 bg-white/5 p-8 shadow-2xl shadow-slate-900/40 backdrop-blur">
          <h2 className="text-2xl font-semibold text-white">Our Two Core Modes</h2>

          <div className="mt-6 space-y-8">
            <article className="space-y-4">
              <h3 className="text-xl font-semibold text-sky-200">1. Energy Insight</h3>
              <p className="leading-relaxed text-slate-100/90">
                In this mode, Aurora functions as your intelligent body interpreter. By analyzing your personal
                physiological data, the platform decodes the subtle signals your body sends — fluctuations in energy,
                focus, recovery, and mood — and translates them into clear, science-based insights.
              </p>
              <p className="leading-relaxed text-slate-100/90">
                Energy Insight helps you understand what your biology is communicating, offering precise explanations and
                answers to your questions about how your body responds to stress, sleep, nutrition, and environment.
              </p>
            </article>

            <article className="space-y-4">
              <h3 className="text-xl font-semibold text-emerald-200">2. Longevity Exploration</h3>
              <p className="leading-relaxed text-slate-100/90">
                This mode opens a gateway to the cutting edge of longevity science. Aurora educates users through curated
                explorations into the world of aging biology, health optimization, and regenerative technology —
                transforming advanced research into practical strategies for sustainable performance and graceful aging.
              </p>
              <p className="leading-relaxed text-slate-100/90">
                From cellular rejuvenation to neuroplasticity and metabolic resilience, Longevity Exploration guides you
                toward the future of human vitality.
              </p>
            </article>
          </div>
        </section>

        <section className="rounded-3xl border border-white/20 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 shadow-2xl shadow-slate-900/40 backdrop-blur">
          <h2 className="text-2xl font-semibold text-white">Our Vision</h2>
          <p className="mt-4 leading-relaxed text-slate-100/90">
            Aurora redefines how we perceive aging — not as a decline, but as an evolvable system of energy and
            adaptation. We merge the rigor of science with the intuition of self-awareness, creating a new paradigm for
            longevity: one that integrates biology, psychology, and technology to help individuals live longer, stronger,
            and more consciously.
          </p>
        </section>
      </div>
    </div>
  )
}

AboutAurora.propTypes = {
  onBack: PropTypes.func.isRequired,
  onStart: PropTypes.func.isRequired,
}

export default AboutAurora

