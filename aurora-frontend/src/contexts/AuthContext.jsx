import { createContext, useCallback, useContext, useMemo, useState } from 'react'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

const DEFAULT_MODAL_STATE = {
  isOpen: false,
  mode: 'sign-in',
}

export const AuthProvider = ({ children }) => {
  const [userProfile, setUserProfile] = useState(null)
  const [modalState, setModalState] = useState(DEFAULT_MODAL_STATE)
  const isRegistered = Boolean(userProfile?.is_registered)

  const openAuthModal = useCallback((mode = 'sign-up') => {
    setModalState({
      isOpen: true,
      mode,
    })
  }, [])

  const closeAuthModal = useCallback(() => {
    setModalState((prev) => ({
      ...prev,
      isOpen: false,
    }))
  }, [])

  const markRegistered = useCallback((profile) => {
    const normalizedProfile = profile
      ? {
          ...profile,
          is_registered:
            typeof profile.is_registered === 'boolean' ? profile.is_registered : true,
        }
      : profile

    setUserProfile(normalizedProfile)
    setModalState((prev) => ({
      ...prev,
      isOpen: false,
    }))
  }, [])

  const markSignedOut = useCallback(() => {
    setUserProfile(null)
  }, [])

  const setAuthModalMode = useCallback((mode) => {
    setModalState({
      isOpen: true,
      mode,
    })
  }, [])

  const value = useMemo(
    () => ({
      isRegistered,
      userProfile,
      markRegistered,
      markSignedOut,
      isAuthModalOpen: modalState.isOpen,
      authModalMode: modalState.mode,
      openAuthModal,
      closeAuthModal,
      setAuthModalMode,
    }),
    [isRegistered, userProfile, modalState, markRegistered, markSignedOut, openAuthModal, closeAuthModal, setAuthModalMode]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}


