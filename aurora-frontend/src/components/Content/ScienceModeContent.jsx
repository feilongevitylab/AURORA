import { useEffect, useMemo, useState } from 'react'
import Plot from 'react-plotly.js'
import { useMode } from '../../contexts/ModeContext'
import { useAuth } from '../../contexts/AuthContext'
import SignUpLink from '../common/SignUpLink'

function ScienceModeContent({ data }) {
  const { modeConfig } = useMode()
  const { isRegistered } = useAuth()
  const chartPayload = data?.chart || null
  const alternateViews = chartPayload?.alternate_views || []

  const [selectedView, setSelectedView] = useState('primary')

  useEffect(() => {
    setSelectedView('primary')
  }, [chartPayload])

  const activeChart = useMemo(() => {
    if (!chartPayload) {
      return null
    }

    if (selectedView === 'primary') {
      return {
        data: chartPayload.data || [],
        layout: chartPayload.layout || {},
      }
    }

    const alternate = alternateViews.find((view) => view.id === selectedView)

    if (!alternate) {
      return {
        data: chartPayload.data || [],
        layout: chartPayload.layout || {},
      }
    }

    return {
      data: alternate.data || [],
      layout: alternate.layout || {},
    }
  }, [selectedView, chartPayload, alternateViews])

  const metadataMetrics = useMemo(() => {
    const metrics = data?.data?.metadata?.metrics || {}
    return Object.entries(metrics)
      .filter(([, value]) => value !== null && value !== undefined)
      .map(([label, value]) => ({
        label,
        value: typeof value === 'number' ? value.toFixed(2) : value,
      }))
  }, [data])

  const stressBucketSummary = useMemo(() => {
    const summary = data?.data?.stress_bucket_summary
    if (!summary) return []
    return Object.entries(summary).map(([bucket, metrics]) => ({
      bucket,
      sessions: metrics.sessions ?? null,
      avg_hrv: metrics.avg_hrv ?? null,
      avg_stress: metrics.avg_stress ?? null,
      avg_hrv_delta: metrics.avg_hrv_delta ?? null,
    }))
  }, [data])

  if (!data) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">{modeConfig.icon}</div>
        <p className="text-gray-600 text-lg">In Longevity Exploration I decode biomarkers, recovery trends, and adaptive strategies.</p>
        <p className="text-gray-500 text-sm mt-2">Ask about emerging research, precise definitions, or how physiology drives sustainable performance.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {!isRegistered && (
        <div className="mb-6 rounded-2xl border border-cyan-200 bg-cyan-50/90 p-6 text-left shadow-sm shadow-cyan-200/60">
          <p className="text-sm leading-relaxed text-cyan-900/90">
            I can dive into longevity analytics right away. To tailor future analyses to your physiology and interests, please{' '}
            <SignUpLink>Sign Up</SignUpLink>. Becoming a member helps Aurora connect the data dots uniquely for you.
          </p>
        </div>
      )}
      {data.insight && (
        <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-8 shadow-lg border border-cyan-200">
          <div className="flex items-start gap-4">
            <div className="text-4xl flex-shrink-0">{modeConfig.icon}</div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Longevity Insight</h3>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {data.insight}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {chartPayload && activeChart && (
        <div className="mt-6 rounded-2xl border border-cyan-200 bg-white shadow-lg">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-cyan-100 px-6 py-4">
            <div>
              <h4 className="text-lg font-semibold text-gray-800">Physiological Visualization</h4>
              <p className="text-sm text-gray-500">
                Explore how HRV changes as stress load accumulates across sessions.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedView('primary')}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                  selectedView === 'primary'
                    ? 'bg-cyan-600 text-white shadow'
                    : 'bg-cyan-50 text-cyan-700 hover:bg-cyan-100'
                }`}
              >
                Primary view
              </button>
              {alternateViews.map((view) => (
                <button
                  key={view.id}
                  onClick={() => setSelectedView(view.id)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                    selectedView === view.id
                      ? 'bg-cyan-600 text-white shadow'
                      : 'bg-cyan-50 text-cyan-700 hover:bg-cyan-100'
                  }`}
                >
                  {view.label}
                </button>
              ))}
            </div>
          </div>

          <div className="px-6 py-4">
            <div className="h-[420px] w-full">
              <Plot
                data={activeChart.data}
                layout={{
                  ...activeChart.layout,
                  autosize: true,
                  height: 420,
                  margin: { ...(activeChart.layout?.margin || {}), t: 40, r: 20, b: 60, l: 50 },
                }}
                config={{
                  responsive: true,
                  displayModeBar: true,
                  displaylogo: false,
                  ...(chartPayload.config || {}),
                }}
                style={{ width: '100%', height: '100%' }}
                useResizeHandler={true}
              />
            </div>
          </div>

          {chartPayload.recommendations?.length > 0 && (
            <div className="border-t border-cyan-100 bg-cyan-50 px-6 py-4">
              <h5 className="text-sm font-semibold text-cyan-900 mb-2">
                How to interpret this visualization
              </h5>
              <ul className="list-disc list-inside space-y-1 text-sm text-cyan-800">
                {chartPayload.recommendations.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {metadataMetrics.length > 0 && (
        <div className="mt-6 rounded-2xl border border-cyan-100 bg-cyan-50/70 p-6 shadow-inner">
          <h4 className="text-lg font-semibold text-cyan-900 mb-4 flex items-center gap-2">
            <span>🧪</span>
            Longevity Metrics
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {metadataMetrics.map(({ label, value }) => {
              const formattedLabel = label.replace(/_/g, ' ')
              return (
                <div
                  key={label}
                  className="rounded-xl border border-cyan-200 bg-white px-4 py-3 shadow-sm"
                >
                  <p className="text-xs uppercase tracking-wide text-cyan-500 mb-1">
                    {formattedLabel}
                  </p>
                  <p className="text-base font-semibold text-cyan-900">{value}</p>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {stressBucketSummary.length > 0 && (
        <div className="mt-6 rounded-2xl border border-cyan-100 bg-white shadow-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-cyan-100 flex items-center gap-2">
            <span className="text-xl">📉</span>
            <h4 className="text-lg font-semibold text-gray-800">HRV by Stress Bucket</h4>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50 text-gray-600">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold uppercase tracking-wide">Bucket</th>
                  <th className="px-4 py-2 text-left font-semibold uppercase tracking-wide">Sessions</th>
                  <th className="px-4 py-2 text-left font-semibold uppercase tracking-wide">Avg HRV (ms)</th>
                  <th className="px-4 py-2 text-left font-semibold uppercase tracking-wide">Avg Stress</th>
                  <th className="px-4 py-2 text-left font-semibold uppercase tracking-wide">Δ HRV (ms)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 text-gray-700">
                {stressBucketSummary.map((row) => (
                  <tr key={row.bucket}>
                    <td className="px-4 py-2 capitalize">{row.bucket}</td>
                    <td className="px-4 py-2">{row.sessions ?? '—'}</td>
                    <td className="px-4 py-2">{row.avg_hrv != null ? row.avg_hrv.toFixed(2) : '—'}</td>
                    <td className="px-4 py-2">
                      {row.avg_stress != null ? row.avg_stress.toFixed(2) : '—'}
                    </td>
                    <td className="px-4 py-2">
                      {row.avg_hrv_delta != null ? row.avg_hrv_delta.toFixed(2) : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* References Section (placeholder for future implementation) */}
      {data.references && data.references.length > 0 && (
        <div className="mt-6 bg-white rounded-xl p-6 shadow-md">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">Supporting References</h4>
          <ul className="space-y-3">
            {data.references.map((ref, index) => (
              <li key={index} className="flex items-start gap-3 text-gray-700">
                <span className="text-cyan-500 mt-1">📚</span>
                <span>{ref}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations Section (placeholder) */}
      {data.recommendations && data.recommendations.length > 0 && (
        <div className="mt-6 bg-white rounded-xl p-6 shadow-md">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">Suggested Reading</h4>
          <ul className="space-y-3">
            {data.recommendations.map((rec, index) => (
              <li key={index} className="flex items-start gap-3 text-gray-700">
                <span className="text-cyan-500 mt-1">🔗</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Terms (if available) */}
      {data.data?.insights && (
        <div className="mt-6 bg-gradient-to-br from-cyan-50 to-teal-50 rounded-xl p-6 shadow-md border border-cyan-200">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">Key Concepts</h4>
          <ul className="space-y-2">
            {data.data.insights.slice(0, 5).map((insight, index) => (
              <li key={index} className="flex items-start gap-3 text-gray-700">
                <span className="text-cyan-500 mt-1">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ScienceModeContent

