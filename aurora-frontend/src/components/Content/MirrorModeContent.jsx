import { useMemo } from 'react'
import { useMode } from '../../contexts/ModeContext'
import { useAuth } from '../../contexts/AuthContext'
import Plot from 'react-plotly.js'
import SignUpLink from '../common/SignUpLink'

const FALLBACK_LAYERS = {
  physiology: {
    title: 'Physiology',
    description: 'HRV · Sleep Quality · Heart Coherence',
    metrics: [
      { label: 'HRV', value: '--' },
      { label: 'Sleep Quality', value: '--' },
      { label: 'Heart Coherence', value: '--' },
    ],
  },
  mind: {
    title: 'Mind',
    description: 'Stress Index · Mood Balance',
    metrics: [
      { label: 'Stress Index', value: '--' },
      { label: 'Mood Balance', value: '--' },
    ],
  },
  meaning: {
    title: 'Meaning',
    description: 'Purpose · Fulfillment',
    metrics: [
      { label: 'Purpose', value: '--' },
      { label: 'Fulfillment', value: '--' },
    ],
  },
}

function MirrorLayerCard({ layerKey, layer }) {
  return (
    <div className="flex flex-col gap-4 rounded-3xl border border-indigo-200 bg-gradient-to-br from-white/80 to-white/30 p-6 shadow-sm shadow-indigo-400/10 backdrop-blur">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-indigo-900">{layer.title}</h3>
        <span className="text-base text-indigo-500/80">{layerKey === 'physiology' ? '🩺' : layerKey === 'mind' ? '🧠' : '✨'}</span>
      </div>
      <p className="text-sm text-indigo-800/80">{layer.description}</p>
      <div className="space-y-3">
        {layer.metrics.map((metric) => (
          <div key={metric.label} className="flex items-baseline justify-between border-b border-indigo-100 pb-2 last:border-none">
            <span className="text-sm text-indigo-700/80">{metric.label}</span>
            <span className="text-xl font-semibold text-indigo-900">{metric.value ?? '--'}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function MirrorModeContent({ data }) {
  const { modeConfig } = useMode()
  const { isRegistered } = useAuth()

  if (!isRegistered) {
    return (
      <div className="mx-auto max-w-3xl space-y-6 py-16 text-center">
        <section className="rounded-3xl border border-indigo-300/40 bg-gradient-to-br from-indigo-700 via-indigo-600 to-indigo-500 p-10 text-white shadow-2xl shadow-indigo-900/40 backdrop-blur">
          <p className="text-sm uppercase tracking-[0.4em] text-indigo-100/80">{modeConfig.nameEn}</p>
          <h2 className="mt-4 text-3xl font-semibold leading-relaxed">
            Traveler, I feel your presence. Let me learn who you are so I can reflect your mirror with fidelity.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-indigo-100/90">
            Share your name and rhythms—please{' '}
            <SignUpLink variant="light">Sign Up</SignUpLink>
            . With your story remembered, I can weave physiology, mind, and meaning into the mirror meant for you.
          </p>
        </section>
        <p className="text-sm text-indigo-600/80">
          I will still answer gentle questions, yet personalized Energy insights bloom once Aurora recognizes you.
        </p>
      </div>
    )
  }

  const mirrorData = useMemo(() => data || {}, [data])
  const mirrorPayload = mirrorData?.data || {}
  const hasMirrorPayload = Boolean(mirrorPayload?.mirror_layers)

  const mirrorMeta = mirrorData?.hero || {}
  const layers = mirrorPayload?.mirror_layers || FALLBACK_LAYERS
  const coordinationScore = mirrorPayload?.coordination_score ?? 78
  const shortInsight =
    mirrorPayload?.insight_summary || mirrorData?.insight || 'You are staying focused, though recovery is slightly below baseline.'

  const energyNarrative =
    mirrorPayload?.energy_pattern ||
    mirrorData?.insight ||
    'Over the past few days your heart rhythm dipped while focus rose, signaling that your body is working to match your intent.'

  const topDialog =
    mirrorMeta?.top_dialog ||
    'Good day, traveler. Your system is waking in a gentle cadence - let us trace the waves of body and mind together.'

  const energySummary =
    mirrorMeta?.mirror_summary ||
    'Your purpose alignment is strongly correlated with recovery, suggesting meaning is sustaining your nervous balance.'

  const quickInsights = mirrorPayload?.insights || []

  if (!hasMirrorPayload) {
    return (
      <div className="py-16 text-center">
        <div className="mb-4 text-6xl">{modeConfig.icon}</div>
        <p className="text-lg text-gray-600">
          Energy Insight is waiting for your invitation. Ask for today's pulse or share how your body and mind feel.
        </p>
        <p className="mt-2 text-sm text-gray-500">
          When you are ready, I will surface the links across physiology, mind, and meaning to map your awareness topology.
        </p>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl space-y-10 px-6 py-16 bg-white text-gray-900">
      <section className="rounded-3xl border border-indigo-100 bg-white p-8 shadow-xl shadow-indigo-100/70">
        <div className="flex items-start justify-between gap-6">
          <div>
            <p className="text-sm uppercase tracking-[0.4em] text-indigo-500/70">{modeConfig.nameEn}</p>
            <h2 className="mt-3 text-3xl font-semibold leading-relaxed text-gray-900">{topDialog}</h2>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-indigo-700">
            <span className="text-sm uppercase tracking-[0.3em]">Energy</span>
            <span className="text-lg">{modeConfig.icon}</span>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-[1fr_2fr]">
        <div className="rounded-3xl border border-slate-800/80 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 shadow-xl shadow-slate-900/50 text-white">
          <p className="text-sm uppercase tracking-[0.3em] text-sky-200/80">Today's Coordination Index</p>
          <div className="mt-4 flex items-baseline gap-4">
            <span className="text-5xl font-bold text-sky-200">{coordinationScore}%</span>
            <span className="text-sky-200/80">Body × Mind × Meaning</span>
          </div>
          <p className="mt-4 text-base text-slate-100/90">{energySummary}</p>
        </div>

        <div className="rounded-3xl border border-sky-100 bg-gradient-to-br from-white via-sky-50 to-indigo-100/60 p-6 shadow-lg shadow-sky-200/60">
          <p className="text-sm uppercase tracking-[0.3em] text-indigo-500/70">Today's Insight</p>
          <p className="mt-4 text-lg font-medium text-gray-800">{shortInsight}</p>
          {quickInsights.length > 0 && (
            <ul className="mt-6 grid gap-3 md:grid-cols-2">
              {quickInsights.slice(0, 4).map((insight, index) => (
                <li
                  key={`${insight}-${index}`}
                  className="rounded-2xl border border-indigo-100 bg-indigo-50/60 px-4 py-3 text-sm text-gray-700 shadow-sm"
                >
                  {insight}
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {Object.entries(layers).map(([key, layer]) => (
          <MirrorLayerCard key={key} layerKey={key} layer={layer} />
        ))}
      </section>

      {mirrorData?.chart && mirrorData.chart.data?.length > 0 && (
        <section className="rounded-3xl border border-indigo-100 bg-white p-6 shadow-xl shadow-indigo-100/60">
          <div className="flex flex-wrap items-center justify-between gap-3 text-gray-800">
            <h3 className="text-2xl font-semibold">HRV · Stress · Focus Trend</h3>
            <span className="text-sm text-indigo-500/70">Past 7 days · refreshed hourly</span>
          </div>
          <div className="mt-6 h-[460px] w-full">
            <Plot
              data={mirrorData.chart.data || []}
              layout={{
                ...mirrorData.chart.layout,
                autosize: true,
                height: 460,
                margin: { t: 40, r: 20, b: 60, l: 50 },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#0F172A' },
              }}
              config={{
                responsive: true,
                displayModeBar: false,
                displaylogo: false,
              }}
              style={{ width: '100%', height: '100%' }}
              useResizeHandler={true}
            />
          </div>
        </section>
      )}

      <section className="rounded-3xl border border-indigo-100 bg-gradient-to-br from-indigo-600/10 via-white to-sky-100/70 p-8 text-gray-800 shadow-xl shadow-indigo-200/60">
        <h3 className="text-sm uppercase tracking-[0.4em] text-indigo-500/70">Energy Pattern</h3>
        <p className="mt-4 text-lg leading-relaxed text-gray-700">{energyNarrative}</p>
      </section>
    </div>
  )
}

export default MirrorModeContent

