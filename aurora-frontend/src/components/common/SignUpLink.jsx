import { useAuth } from '../../contexts/AuthContext'

const VARIANT_CLASSES = {
  primary: 'text-indigo-600 hover:text-indigo-500 underline decoration-indigo-400',
  light: 'text-indigo-100 hover:text-white underline decoration-white/70',
}

function SignUpLink({ children = 'Sign Up', variant = 'primary', className = '' }) {
  const { openAuthModal } = useAuth()

  const handleClick = (event) => {
    event.preventDefault()
    openAuthModal('sign-up')
  }

  const variantClass = VARIANT_CLASSES[variant] || VARIANT_CLASSES.primary

  return (
    <button
      type="button"
      onClick={handleClick}
      className={`inline-flex items-center font-semibold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white ${variantClass} ${className}`}
    >
      {children}
    </button>
  )
}

export default SignUpLink


