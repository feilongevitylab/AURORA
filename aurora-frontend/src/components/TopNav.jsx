import { useState } from 'react'

const socialIcons = [
  {
    name: 'X',
    href: '#share-x',
    svg: (
      <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current">
        <path d="M4 3h3.5l4.5 6.3L16.5 3H20l-6.6 9.1L20.5 21H17l-5-6.8L6.7 21H4l7-9.6L4 3z" />
      </svg>
    ),
  },
  {
    name: 'Instagram',
    href: '#share-instagram',
    svg: (
      <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current">
        <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5m0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm10.75 1.5a1.25 1.25 0 1 1-1.26 1.25 1.25 1.25 0 0 1 1.26-1.25M12 7a5 5 0 1 1-5 5 5 5 0 0 1 5-5m0 2a3 3 0 1 0 3 3 3 3 0 0 0-3-3" />
      </svg>
    ),
  },
  {
    name: 'Facebook',
    href: '#share-facebook',
    svg: (
      <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current">
        <path d="M13.5 22h-3v-7H8v-3h2.5V9a3.75 3.75 0 0 1 4-4h2.5v3H15c-1 0-1.5.5-1.5 1.5v2h2.75l-.5 3H13.5z" />
      </svg>
    ),
  },
]

function TopNav() {
  const [isSignedIn, setIsSignedIn] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [credentials, setCredentials] = useState({
    email: '',
    password: '',
  })

  const handleFieldChange = (event) => {
    const { name, value } = event.target
    setCredentials((prev) => ({ ...prev, [name]: value }))
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setCredentials({ email: '', password: '' })
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    setIsSignedIn(true)
    handleCloseModal()
  }

  return (
    <>
      <div className="pointer-events-none fixed inset-x-0 top-0 z-40 flex justify-center">
        <div className="flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 pointer-events-auto" />

          <div className="flex items-center gap-4 pointer-events-auto">
            {isSignedIn && (
              <div className="flex items-center gap-3">
                {socialIcons.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    aria-label={item.name}
                    className="flex h-8 w-8 items-center justify-center rounded-full border border-white/40 text-white transition hover:border-white/80 hover:bg-white/10"
                  >
                    {item.svg}
                  </a>
                ))}
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/90 shadow-md shadow-slate-900/30">
                  <span className="text-sm font-semibold text-indigo-600">U</span>
                </div>
              </div>
            )}

            {!isSignedIn && (
              <button
                type="button"
                className="rounded-full border border-white/60 px-5 py-2 text-sm font-semibold text-white transition hover:border-white hover:bg-white/10"
                onClick={() => setShowModal(true)}
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4">
          <div className="w-full max-w-md rounded-3xl bg-white/95 p-8 shadow-2xl shadow-slate-900/40 backdrop-blur">
            <div className="mb-6 text-center">
              <p className="text-sm uppercase tracking-[0.35em] text-indigo-400">Aurora Access</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-900">Sign in to continue the journey</h2>
              <p className="mt-2 text-sm text-slate-600">
                Enter your credentials to sync your data and personalize the experience.
              </p>
            </div>

            <form className="space-y-5" onSubmit={handleSubmit}>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={credentials.email}
                  onChange={handleFieldChange}
                  required
                  className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-700">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  value={credentials.password}
                  onChange={handleFieldChange}
                  required
                  className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  placeholder="Enter your password"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:from-indigo-600 hover:to-blue-700"
                >
                  Sign In
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

export default TopNav

