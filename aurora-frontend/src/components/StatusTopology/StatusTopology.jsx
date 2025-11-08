import { useMemo } from 'react'

function StatusTopology({ data }) {
  // Extract topology data from API response
  const topologyData = useMemo(() => {
    if (!data?.data) return null

    const stats = data.data.statistics || {}
    const hrvByStress = data.data.hrv_by_stress_level || {}

    return {
      physiology: {
        hrv: stats.hrv?.mean || 0,
        sleep: null, // Placeholder - would come from sleep API
        heart: stats.hrv?.mean || 0
      },
      mind: {
        stress: stats.stress_score?.mean || 0,
        mood: null // Placeholder - would come from mood API
      },
      meaning: {
        purpose: null, // Placeholder
        fulfillment: null // Placeholder
      }
    }
  }, [data])

  if (!topologyData) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>Awaiting data...</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Physiology */}
      <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-6 border-2 border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-4 flex items-center gap-2">
          <span>🧬</span>
          Physiology
        </h3>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-blue-700 mb-1">HRV</p>
            <p className="text-2xl font-bold text-blue-900">
              {topologyData.physiology.hrv.toFixed(1)}
            </p>
          </div>
          <div>
            <p className="text-sm text-blue-700 mb-1">Sleep/Heart</p>
            <p className="text-lg font-semibold text-blue-800">
              {topologyData.physiology.sleep ? `${topologyData.physiology.sleep}` : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Mind */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border-2 border-purple-200">
        <h3 className="text-lg font-semibold text-purple-900 mb-4 flex items-center gap-2">
          <span>🧠</span>
          Mind
        </h3>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-purple-700 mb-1">Stress</p>
            <p className="text-2xl font-bold text-purple-900">
              {topologyData.mind.stress.toFixed(1)}
            </p>
          </div>
          <div>
            <p className="text-sm text-purple-700 mb-1">Mood</p>
            <p className="text-lg font-semibold text-purple-800">
              {topologyData.mind.mood || 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Meaning */}
      <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-6 border-2 border-amber-200">
        <h3 className="text-lg font-semibold text-amber-900 mb-4 flex items-center gap-2">
          <span>✨</span>
          Meaning
        </h3>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-amber-700 mb-1">Purpose</p>
            <p className="text-lg font-semibold text-amber-800">
              {topologyData.meaning.purpose || 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-sm text-amber-700 mb-1">Fulfillment</p>
            <p className="text-lg font-semibold text-amber-800">
              {topologyData.meaning.fulfillment || 'N/A'}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatusTopology

