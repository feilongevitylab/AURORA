import { useMode } from '../../contexts/ModeContext'

function ScienceModeContent({ data }) {
  const { modeConfig } = useMode()

  if (!data) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">{modeConfig.icon}</div>
        <p className="text-gray-600 text-lg">In Science Exploration Mode I can unpack technical terms and scientific concepts.</p>
        <p className="text-gray-500 text-sm mt-2">Ask about emerging research, precise definitions, or physiological principles.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {data.insight && (
        <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-8 shadow-lg border border-cyan-200">
          <div className="flex items-start gap-4">
            <div className="text-4xl flex-shrink-0">{modeConfig.icon}</div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Scientific Explanation</h3>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {data.insight}
                </p>
              </div>
            </div>
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

