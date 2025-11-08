import { useMode } from '../../contexts/ModeContext'

function CompanionModeContent({ data }) {
  const { modeConfig } = useMode()

  if (!data) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">{modeConfig.icon}</div>
        <p className="text-gray-600 text-lg">In Companion Mode you can talk to me about any emotional or mental questions.</p>
        <p className="text-gray-500 text-sm mt-2">I'll respond with warmth, validation, and gentle guidance.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {data.insight && (
        <div className="bg-gradient-to-br from-orange-50 to-pink-50 rounded-2xl p-8 shadow-lg border border-orange-200">
          <div className="flex items-start gap-4">
            <div className="text-4xl flex-shrink-0">{modeConfig.icon}</div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Companion Insight</h3>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {data.insight}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {data.data?.insights && (
        <div className="mt-6 bg-white rounded-xl p-6 shadow-md">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">Key Reflections</h4>
          <ul className="space-y-3">
            {data.data.insights.slice(0, 5).map((insight, index) => (
              <li key={index} className="flex items-start gap-3 text-gray-700">
                <span className="text-orange-500 mt-1">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default CompanionModeContent

