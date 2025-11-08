import { useMode, MODES } from '../../contexts/ModeContext'
import CompanionModeContent from './CompanionModeContent'
import MirrorModeContent from './MirrorModeContent'
import ScienceModeContent from './ScienceModeContent'

function ContentArea({ data, loading, error }) {
  const { currentMode } = useMode()

  if (loading) {
    return (
      <div className="text-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Processing your request...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <p className="text-red-800 font-semibold mb-2">Something went wrong</p>
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      </div>
    )
  }

  switch (currentMode) {
    case MODES.COMPANION:
      return <CompanionModeContent data={data} />
    case MODES.MIRROR:
      return <MirrorModeContent data={data} />
    case MODES.SCIENCE:
      return <ScienceModeContent data={data} />
    default:
      return <CompanionModeContent data={data} />
  }
}

export default ContentArea

