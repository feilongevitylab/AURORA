import { useState, useEffect } from 'react'
import axios from 'axios'
import Plot from 'react-plotly.js'

const API_BASE_URL = 'http://localhost:8000'

function Dashboard() {
  // State for HRV data summary
  const [hrvData, setHrvData] = useState(null)
  const [hrvLoading, setHrvLoading] = useState(true)
  const [hrvError, setHrvError] = useState(null)

  // State for Stress data
  const [stressData, setStressData] = useState(null)
  const [stressLoading, setStressLoading] = useState(true)
  const [stressError, setStressError] = useState(null)

  // State for Insight data (chart and explanation)
  const [insightData, setInsightData] = useState(null)
  const [insightLoading, setInsightLoading] = useState(false)
  const [insightError, setInsightError] = useState(null)

  // State for user query input
  const [userQuery, setUserQuery] = useState('analyze and visualize my HRV data')

  // Fetch HRV data
  useEffect(() => {
    const fetchHrvData = async () => {
      try {
        setHrvLoading(true)
        setHrvError(null)
        const response = await axios.get(`${API_BASE_URL}/api/hrv?days=7`)
        setHrvData(response.data)
      } catch (error) {
        console.error('Error fetching HRV data:', error)
        setHrvError(error.message)
      } finally {
        setHrvLoading(false)
      }
    }

    fetchHrvData()
  }, [])

  // Fetch Stress data
  useEffect(() => {
    const fetchStressData = async () => {
      try {
        setStressLoading(true)
        setStressError(null)
        const response = await axios.get(`${API_BASE_URL}/api/stress?days=7`)
        setStressData(response.data)
      } catch (error) {
        console.error('Error fetching stress data:', error)
        setStressError(error.message)
      } finally {
        setStressLoading(false)
      }
    }

    fetchStressData()
  }, [])

  // Handle Generate Insight button click
  const handleGenerateInsight = async () => {
    if (!userQuery.trim()) {
      alert('Please enter a query')
      return
    }

    try {
      setInsightLoading(true)
      setInsightError(null)
      const response = await axios.post(`${API_BASE_URL}/api/insight`, {
        query: userQuery.trim(),
        raw_query: userQuery,
        mode: 'science'
      })
      setInsightData(response.data)
    } catch (error) {
      console.error('Error generating insight:', error)
      setInsightError(error.response?.data?.detail || error.message)
    } finally {
      setInsightLoading(false)
    }
  }

  // Handle Enter key press in input
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleGenerateInsight()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              AURORA Dashboard
            </h1>
            <p className="text-lg text-gray-600">
              AI-powered Data Analysis Platform
            </p>
          </div>

          {/* Query Input and Generate Button */}
          <div className="bg-white rounded-xl shadow-lg p-4 border border-gray-200 mb-6">
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your query (e.g., 'analyze and visualize my HRV data')"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={insightLoading}
              />
              <button
                onClick={handleGenerateInsight}
                disabled={insightLoading || !userQuery.trim()}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2"
              >
                {insightLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <span>🚀</span>
                    <span>Generate Insight</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Bento Box Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:h-[calc(100vh-12rem)] lg:min-h-[800px]">
          {/* Left Panel: AI Insight (Full Height, Vertical) */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-lg p-6 border border-gray-200 flex flex-col lg:h-full min-h-[400px]">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
              <span className="mr-2">🤖</span>
              AI Insight
            </h2>
            
            <div className="flex-1 flex flex-col min-h-0">
              {insightLoading ? (
                <div className="flex flex-col items-center justify-center flex-1">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-3"></div>
                  <p className="text-gray-600 text-sm">Generating AI insights...</p>
                </div>
              ) : insightError ? (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex-1 flex flex-col justify-center">
                  <p className="text-red-800 font-semibold mb-2">Error generating insight</p>
                  <p className="text-red-700 text-sm">{insightError}</p>
                  <button
                    onClick={handleGenerateInsight}
                    className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
                  >
                    Try Again
                  </button>
                </div>
              ) : insightData?.insight ? (
                <div className="flex flex-col h-full min-h-0 space-y-4">
                  <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-lg p-5 border border-indigo-200 flex-1 overflow-y-auto min-h-0">
                    <div className="prose prose-sm max-w-none">
                      <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                        {insightData.insight}
                      </p>
                    </div>
                  </div>

                  {/* Additional insights if available */}
                  {insightData.data?.insights && (
                    <div className="pt-4 border-t border-gray-200 flex-shrink-0">
                      <p className="text-sm font-medium text-gray-700 mb-2">Key Insights</p>
                      <ul className="space-y-2 max-h-32 overflow-y-auto">
                        {insightData.data.insights.slice(0, 3).map((insight, index) => (
                          <li key={index} className="flex items-start text-sm text-gray-600">
                            <span className="mr-2 text-indigo-600">•</span>
                            <span>{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center flex-1 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border-2 border-dashed border-gray-300 p-8">
                  <span className="text-4xl mb-3">🤖</span>
                  <p className="text-gray-600 text-center mb-2 font-medium">No insight generated yet</p>
                  <p className="text-gray-500 text-sm text-center">Enter a query above and click "Generate Insight" to see AI-powered analysis</p>
                </div>
              )}
            </div>
          </div>

          {/* Right Side: Two Panels Stacked */}
          <div className="lg:col-span-2 flex flex-col gap-6 lg:h-full">
            {/* Top Right Panel: Plotly Visualization (Larger Space) */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 flex-1 flex flex-col min-h-0 min-h-[500px] lg:min-h-[60%]">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center flex-shrink-0">
                <span className="mr-2">📈</span>
                Visualization
              </h2>
              
              <div className="flex-1 min-h-0 flex items-center justify-center">
                {insightLoading ? (
                  <div className="flex flex-col items-center justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-3"></div>
                    <p className="text-gray-600 text-sm">Loading visualization...</p>
                  </div>
                ) : insightError ? (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-6 w-full max-w-md mx-auto">
                    <p className="text-red-800 font-semibold mb-2">Error loading chart</p>
                    <p className="text-red-700 text-sm mb-4">{insightError}</p>
                    <button
                      onClick={handleGenerateInsight}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
                    >
                      Try Again
                    </button>
                  </div>
                ) : insightData?.chart ? (
                  <div className="w-full h-full min-h-0">
                    <Plot
                      data={insightData.chart.data || []}
                      layout={{
                        ...insightData.chart.layout,
                        autosize: true,
                        responsive: true,
                        height: undefined,
                      }}
                      config={{
                        responsive: true,
                        displayModeBar: true,
                        displaylogo: false,
                        autosizable: true,
                      }}
                      style={{ width: '100%', height: '100%' }}
                      useResizeHandler={true}
                    />
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border-2 border-dashed border-gray-300 p-8 w-full max-w-md mx-auto">
                    <span className="text-4xl mb-3">📈</span>
                    <p className="text-gray-600 text-center mb-2 font-medium">No visualization available</p>
                    <p className="text-gray-500 text-sm text-center">Generate an insight to see interactive charts</p>
                  </div>
                )}
              </div>
            </div>

            {/* Bottom Right Panel: Physiological Data Summary (Smaller Space) */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 flex-shrink-0 lg:min-h-[40%]">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">📊</span>
                Physiological Data
              </h2>
              
              {/* HRV Data Section */}
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                  <span className="mr-1">💓</span>
                  HRV Data
                </h3>
                {hrvLoading ? (
                  <div className="flex items-center justify-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  </div>
                ) : hrvError ? (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-2">
                    <p className="text-red-800 text-xs">Error: {hrvError}</p>
                  </div>
                ) : hrvData ? (
                  <div className="space-y-2">
                    <div className="bg-blue-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Total HRV Data Points</p>
                      <p className="text-2xl font-bold text-blue-700">{hrvData.count}</p>
                    </div>

                    <div className="grid grid-cols-3 gap-2">
                      <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-2 border border-green-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg RMSSD</p>
                        <p className="text-base font-semibold text-green-800">
                          {hrvData.metrics?.avg_rmssd?.toFixed(2) || 'N/A'}
                        </p>
                      </div>

                      <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-2 border border-purple-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg SDNN</p>
                        <p className="text-base font-semibold text-purple-800">
                          {hrvData.metrics?.avg_sdnn?.toFixed(2) || 'N/A'}
                        </p>
                      </div>

                      <div className="bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg p-2 border border-orange-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg pNN50</p>
                        <p className="text-base font-semibold text-orange-800">
                          {hrvData.metrics?.avg_pnn50?.toFixed(2) || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>

              {/* Stress Data Section */}
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                  <span className="mr-1">😰</span>
                  Stress Data
                </h3>
                {stressLoading ? (
                  <div className="flex items-center justify-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  </div>
                ) : stressError ? (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-2">
                    <p className="text-red-800 text-xs">Error: {stressError}</p>
                  </div>
                ) : stressData ? (
                  <div className="space-y-2">
                    <div className="bg-red-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">Total Stress Data Points</p>
                      <p className="text-2xl font-bold text-red-700">{stressData.count}</p>
                    </div>

                    <div className="grid grid-cols-3 gap-2">
                      <div className="bg-gradient-to-r from-red-50 to-red-100 rounded-lg p-2 border border-red-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg Stress</p>
                        <p className="text-base font-semibold text-red-800">
                          {stressData.metrics?.avg_stress_level?.toFixed(2) || 'N/A'}
                        </p>
                      </div>

                      <div className="bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg p-2 border border-pink-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg HR</p>
                        <p className="text-base font-semibold text-pink-800">
                          {stressData.metrics?.avg_heart_rate?.toFixed(2) || 'N/A'}
                        </p>
                      </div>

                      <div className="bg-gradient-to-r from-rose-50 to-rose-100 rounded-lg p-2 border border-rose-200">
                        <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">Avg RR</p>
                        <p className="text-base font-semibold text-rose-800">
                          {stressData.metrics?.avg_respiratory_rate?.toFixed(2) || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
