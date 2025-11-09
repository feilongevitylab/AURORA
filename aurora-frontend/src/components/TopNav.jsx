import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { useAuth } from '../contexts/AuthContext'

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

const genderOptions = [
  { value: 'female', label: 'Female' },
  { value: 'male', label: 'Male' },
  { value: 'unspecified', label: 'Prefer not to say' },
]

const topicOptions = [
  { value: 'sleep', label: 'Sleep' },
  { value: 'anxiety', label: 'Anxiety' },
  { value: 'depression', label: 'Depression' },
  { value: 'stress', label: 'Stress' },
  { value: 'hormonal_changes', label: 'Hormonal shifts' },
  { value: 'other', label: 'Other' },
]

const wearableOptions = [
  { value: 'none', label: 'Not now' },
  { value: 'smartwatch', label: 'Smart watch' },
  { value: 'ouraring', label: 'Oura Ring' },
]

const API_BASE_URL = 'http://localhost:8000'

const initialSignUpForm = {
  email: '',
  password: '',
  nickname: '',
  gender: 'unspecified',
  topics: [],
  otherTopic: '',
  wearablePreference: 'none',
}

function TopNav() {
  const {
    isRegistered,
    userProfile,
    isAuthModalOpen,
    authModalMode,
    openAuthModal,
    closeAuthModal,
    markRegistered,
    setAuthModalMode,
  } = useAuth()

  const [signInForm, setSignInForm] = useState({ email: '', password: '' })
  const [signUpForm, setSignUpForm] = useState(initialSignUpForm)
  const [formError, setFormError] = useState(null)
  const [formLoading, setFormLoading] = useState(false)
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false)

  const accountMenuItems = [
    {
      label: 'Account settings',
      icon: (
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-slate-500" aria-hidden="true">
          <path
            fill="currentColor"
            d="M12 2a5 5 0 015 5v1.26c.71.37 1.37.85 1.97 1.45l1.07-.43a2 2 0 012.54 1.06l1 2.32a2 2 0 01-1.03 2.57l-1.05.45c.1.66.1 1.33 0 1.99l1.05.45a2 2 0 011.03 2.57l-1 2.32a2 2 0 01-2.54 1.06l-1.07-.43a8.03 8.03 0 01-1.97 1.45V22a2 2 0 01-2 2h-2a2 2 0 01-2-2v-1.26a8.03 8.03 0 01-1.97-1.45l-1.07.43a2 2 0 01-2.54-1.06l-1-2.32a2 2 0 011.03-2.57l1.05-.45a7.94 7.94 0 010-1.99l-1.05-.45a2 2 0 01-1.03-2.57l1-2.32a2 2 0 012.54-1.06l1.07.43c.6-.6 1.26-1.08 1.97-1.45V7a5 5 0 015-5zm0 7a3 3 0 100 6 3 3 0 000-6z"
          />
        </svg>
      ),
      onClick: () => {},
    },
    {
      label: 'Subscription',
      icon: (
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-slate-500" aria-hidden="true">
          <path
            fill="currentColor"
            d="M5 4h14a2 2 0 012 2v3H3V6a2 2 0 012-2zm-2 7h18v7a2 2 0 01-2 2H5a2 2 0 01-2-2v-7zm7 2v3h4v-3h-4z"
          />
        </svg>
      ),
      onClick: () => {},
    },
    {
      label: 'Feedback',
      icon: (
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-slate-500" aria-hidden="true">
          <path
            fill="currentColor"
            d="M4 3h16a2 2 0 012 2v12a2 2 0 01-2 2H8l-4 4V5a2 2 0 012-2zm4 6v2h8V9H8zm0-4v2h12V5H8zm0 8v2h6v-2H8z"
          />
        </svg>
      ),
      onClick: () => {},
    },
    {
      label: 'Paired device',
      icon: (
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-slate-500" aria-hidden="true">
          <path
            fill="currentColor"
            d="M7 2a2 2 0 00-2 2v4h2V4h10v4h2V4a2 2 0 00-2-2H7zm13 6H4a2 2 0 00-2 2v8a2 2 0 002 2h5v2h6v-2h5a2 2 0 002-2v-8a2 2 0 00-2-2zm0 10H4v-8h16v8z"
          />
        </svg>
      ),
      onClick: () => {},
    },
    {
      label: 'Sign out',
      icon: (
        <svg viewBox="0 0 24 24" className="h-5 w-5 text-slate-500" aria-hidden="true">
          <path
            fill="currentColor"
            d="M10 3a2 2 0 00-2 2v3h2V5h10v14H10v-3H8v3a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H10zm1 6l-1.41 1.41L12.17 13H3v2h9.17l-2.58 2.59L11 19l5-5-5-5z"
          />
        </svg>
      ),
      onClick: () => markRegistered(null),
    },
  ]

  const avatarInitial = useMemo(() => {
    if (!userProfile) return 'U'
    if (userProfile.nickname && userProfile.nickname.length > 0) {
      return userProfile.nickname[0].toUpperCase()
    }
    if (userProfile.email && userProfile.email.length > 0) {
      return userProfile.email[0].toUpperCase()
    }
    return 'U'
  }, [userProfile])

  useEffect(() => {
    if (!isAuthModalOpen) {
      setSignInForm({ email: '', password: '' })
      setSignUpForm(initialSignUpForm)
      setFormError(null)
      setFormLoading(false)
    }
  }, [isAuthModalOpen])

  useEffect(() => {
    setFormError(null)
  }, [authModalMode])

  const handleSignInFieldChange = (event) => {
    const { name, value } = event.target
    setSignInForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSignUpFieldChange = (field, value) => {
    setSignUpForm((prev) => ({ ...prev, [field]: value }))
  }

  const toggleTopic = (topic) => {
    setSignUpForm((prev) => {
      const alreadySelected = prev.topics.includes(topic)
      let updatedTopics = prev.topics.slice()
      let otherTopic = prev.otherTopic

      if (alreadySelected) {
        updatedTopics = updatedTopics.filter((item) => item !== topic)
        if (topic === 'other') {
          otherTopic = ''
        }
      } else {
        updatedTopics.push(topic)
      }

      return {
        ...prev,
        topics: updatedTopics,
        otherTopic,
      }
    })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setFormError(null)
    setFormLoading(true)

    try {
      if (authModalMode === 'sign-up') {
      if (!signUpForm.email.trim() || !signUpForm.nickname.trim() || !signUpForm.password.trim()) {
        throw new Error('Please share your email, password, and nickname so Aurora can remember you.')
      }

        if (signUpForm.topics.includes('other') && !signUpForm.otherTopic.trim()) {
          throw new Error('Let me know the other topic you would like Aurora to explore.')
        }

        const payload = {
          email: signUpForm.email.trim(),
        password: signUpForm.password,
          nickname: signUpForm.nickname.trim(),
          gender: signUpForm.gender,
          topics: signUpForm.topics.filter((topic) => topic !== 'other'),
          other_topic: signUpForm.topics.includes('other') ? signUpForm.otherTopic.trim() : null,
          wearable_preference: signUpForm.wearablePreference,
        }

        const response = await axios.post(`${API_BASE_URL}/api/register`, payload)
        markRegistered(response.data.user)
      } else {
        if (!signInForm.email.trim() || !signInForm.password.trim()) {
          throw new Error('Please enter the email and password linked to your Aurora profile.')
        }

        const response = await axios.post(`${API_BASE_URL}/api/login`, {
          email: signInForm.email.trim(),
          password: signInForm.password,
        })
        markRegistered(response.data.user)
      }
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        'I could not process that request. Please try again.'
      setFormError(message)
      setFormLoading(false)
      return
    }

    setFormLoading(false)
  }

  const handleResetPassword = () => {
    window.open('mailto:care@aurorawellness.ai?subject=Reset%20my%20Aurora%20password', '_blank')
  }

  return (
    <>
      <div className="pointer-events-none fixed inset-x-0 top-0 z-40 flex justify-center">
        <div className="flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 pointer-events-auto" />

          <div className="flex items-center gap-4 pointer-events-auto">
            {!isRegistered && (
              <>
                <button
                  type="button"
                  className="rounded-full bg-white/90 px-5 py-2 text-sm font-semibold text-indigo-600 shadow transition hover:bg-white"
                  onClick={() => openAuthModal('sign-up')}
                >
                  Sign Up
                </button>
                <button
                  type="button"
                  className="rounded-full border border-white/60 px-5 py-2 text-sm font-semibold text-white transition hover:border-white hover:bg-white/10"
                  onClick={() => openAuthModal('sign-in')}
                >
                  Sign In
                </button>
              </>
            )}

            {isRegistered && (
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
                <div
                  className="relative"
                  onMouseEnter={() => setIsAccountMenuOpen(true)}
                  onMouseLeave={() => setIsAccountMenuOpen(false)}
                >
                  <button
                    type="button"
                    className="flex h-10 w-10 items-center justify-center rounded-full bg-white/90 shadow-md shadow-slate-900/30 transition hover:shadow-lg"
                    title={userProfile?.nickname || userProfile?.email || 'Aurora Member'}
                  >
                    <span className="text-sm font-semibold text-indigo-600">{avatarInitial}</span>
                  </button>

                  {isAccountMenuOpen && (
                    <div className="absolute right-0 top-12 w-56 rounded-2xl border border-white/60 bg-white/95 p-2 shadow-xl shadow-slate-900/20 backdrop-blur">
                      <div className="space-y-1">
                        {accountMenuItems.map((item) => (
                          <button
                            key={item.label}
                            type="button"
                            onClick={item.onClick}
                            className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left text-sm text-slate-600 transition hover:bg-indigo-50 hover:text-indigo-600"
                          >
                            {item.icon}
                            <span>{item.label}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {isAuthModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4">
          <div className="w-full max-w-lg rounded-3xl bg-white/95 p-8 shadow-2xl shadow-slate-900/40 backdrop-blur">
            <div className="mb-6 text-center">
              <p className="text-sm uppercase tracking-[0.35em] text-indigo-400">Aurora Access</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-900">
                {authModalMode === 'sign-up'
                  ? 'Sign up to deepen the journey'
                  : 'Sign in to continue the journey'}
              </h2>
              <p className="mt-2 text-sm text-slate-600">
                {authModalMode === 'sign-up'
                  ? 'Create your profile so Aurora can remember your rhythms and craft more attuned insights.'
                  : 'Enter your credentials to sync your data and personalize the experience.'}
              </p>
            </div>

            <form className="space-y-5" onSubmit={handleSubmit}>
              {authModalMode === 'sign-in' ? (
                <>
                  <div>
                    <label htmlFor="signin-email" className="block text-sm font-medium text-slate-700">
                      Email
                    </label>
                    <input
                      id="signin-email"
                      name="email"
                      type="email"
                      value={signInForm.email}
                      onChange={handleSignInFieldChange}
                      required
                      className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                      placeholder="you@example.com"
                    />
                  </div>

                  <div>
                    <label htmlFor="signin-password" className="block text-sm font-medium text-slate-700">
                      Password
                    </label>
                    <input
                      id="signin-password"
                      name="password"
                      type="password"
                      value={signInForm.password}
                      onChange={handleSignInFieldChange}
                      required
                      className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                      placeholder="Enter your password"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="md:col-span-2">
                      <label htmlFor="signup-email" className="block text-sm font-medium text-slate-700">
                        Email
                      </label>
                      <input
                        id="signup-email"
                        type="email"
                        value={signUpForm.email}
                        onChange={(event) => handleSignUpFieldChange('email', event.target.value)}
                        required
                        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                        placeholder="you@example.com"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label htmlFor="signup-password" className="block text-sm font-medium text-slate-700">
                        Password
                      </label>
                      <input
                        id="signup-password"
                        type="password"
                        value={signUpForm.password}
                        onChange={(event) => handleSignUpFieldChange('password', event.target.value)}
                        required
                        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                        placeholder="Choose a secure password"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label htmlFor="signup-nickname" className="block text-sm font-medium text-slate-700">
                        Nickname
                      </label>
                      <input
                        id="signup-nickname"
                        type="text"
                        value={signUpForm.nickname}
                        onChange={(event) => handleSignUpFieldChange('nickname', event.target.value)}
                        required
                        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                        placeholder="How should Aurora call you?"
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex items-baseline justify-between">
                      <label className="block text-sm font-medium text-slate-700">Gender</label>
                      <span className="text-xs text-slate-500">(supports Mirror accuracy)</span>
                    </div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {genderOptions.map((option) => {
                        const selected = signUpForm.gender === option.value
                        return (
                          <label
                            key={option.value}
                            className={`inline-flex cursor-pointer items-center rounded-full border px-4 py-2 text-sm transition ${
                              selected
                                ? 'border-indigo-500 bg-indigo-500 text-white'
                                : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-200'
                            }`}
                          >
                            <input
                              type="radio"
                              name="gender"
                              value={option.value}
                              checked={selected}
                              onChange={() => handleSignUpFieldChange('gender', option.value)}
                              className="sr-only"
                            />
                            {option.label}
                          </label>
                        )
                      })}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700">
                      Topics you want Aurora to track
                    </label>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {topicOptions.map((topic) => {
                        const selected = signUpForm.topics.includes(topic.value)
                        return (
                          <label
                            key={topic.value}
                            className={`inline-flex cursor-pointer items-center rounded-full border px-4 py-2 text-sm transition ${
                              selected
                                ? 'border-indigo-500 bg-indigo-500 text-white'
                                : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-200'
                            }`}
                          >
                            <input
                              type="checkbox"
                              value={topic.value}
                              checked={selected}
                              onChange={() => toggleTopic(topic.value)}
                              className="sr-only"
                            />
                            {topic.label}
                          </label>
                        )
                      })}
                    </div>
                    {signUpForm.topics.includes('other') && (
                      <input
                        type="text"
                        value={signUpForm.otherTopic}
                        onChange={(event) => handleSignUpFieldChange('otherTopic', event.target.value)}
                        className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 shadow-inner focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                        placeholder="Tell me the other focus you care about"
                      />
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700">
                      Initial wearable pairing
                    </label>
                    <p className="mt-1 text-xs text-slate-500">
                      Choose what you would like to connect first. You can update this anytime.
                    </p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {wearableOptions.map((option) => {
                        const selected = signUpForm.wearablePreference === option.value
                        return (
                          <label
                            key={option.value}
                            className={`inline-flex cursor-pointer items-center rounded-full border px-4 py-2 text-sm transition ${
                              selected
                                ? 'border-indigo-500 bg-indigo-500 text-white'
                                : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-200'
                            }`}
                          >
                            <input
                              type="radio"
                              name="wearable"
                              value={option.value}
                              checked={selected}
                              onChange={() => handleSignUpFieldChange('wearablePreference', option.value)}
                              className="sr-only"
                            />
                            {option.label}
                          </label>
                        )
                      })}
                    </div>
                  </div>
                </>
              )}

              {formError && (
                <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {formError}
                </div>
              )}

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => closeAuthModal()}
                  className="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={formLoading}
                  className="flex flex-1 items-center justify-center rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:from-indigo-600 hover:to-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {formLoading ? (
                    <span className="flex items-center gap-2">
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"></span>
                      Processing...
                    </span>
                  ) : (
                    (authModalMode === 'sign-up' ? 'Sign Up' : 'Sign In')
                  )}
                </button>
              </div>
            </form>

            <div className="mt-6 space-y-2 text-center text-sm text-slate-500">
              {authModalMode === 'sign-in' && (
                <button
                  type="button"
                  className="inline-flex items-center justify-center gap-2 text-sm font-semibold text-indigo-600 transition hover:text-indigo-500"
                  onClick={handleResetPassword}
                >
                  <svg
                    viewBox="0 0 24 24"
                    className="h-4 w-4"
                    aria-hidden="true"
                  >
                    <path
                      fill="currentColor"
                      d="M12 5a7 7 0 016.93 6.1l1.57-.27-2.5 4.33-4.33-2.5 1.36-.24A4.5 4.5 0 107.5 12H5a7 7 0 017-7zm0 14a7 7 0 01-6.93-6.1l-1.57.27 2.5-4.33 4.33 2.5-1.36.24a4.5 4.5 0 104.53 5.42H19a7 7 0 01-7 7z"
                    />
                  </svg>
                  Reset your password
                </button>
              )}

              {authModalMode === 'sign-up' ? (
                <>
                  Already have an account?{' '}
                  <button
                    type="button"
                    className="font-semibold text-indigo-600 transition hover:text-indigo-500"
                    onClick={() => setAuthModalMode('sign-in')}
                  >
                    Switch to sign in
                  </button>
                </>
              ) : (
                <>
                  New to Aurora?{' '}
                  <button
                    type="button"
                    className="font-semibold text-indigo-600 transition hover:text-indigo-500"
                    onClick={() => setAuthModalMode('sign-up')}
                  >
                    Create an account
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default TopNav
