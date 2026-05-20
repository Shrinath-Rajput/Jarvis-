import { useState, useEffect } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import LoginPage from './components/LoginPage'
import SignupPage from './components/SignupPage'
import JarvisHUD from './components/JarvisHUD'
import { useJarvisStore } from './stores/jarvisStore'
import { initializeAuth } from './services/authService'

function App() {
  const [authMode, setAuthMode] = useState('login') // 'login' | 'signup'
  const isAuthenticated = useJarvisStore(state => state.isAuthenticated)
  const currentUser = useJarvisStore(state => state.currentUser)
  const setCurrentUser = useJarvisStore(state => state.setCurrentUser)
  const [isInitialized, setIsInitialized] = useState(false)

  // Initialize auth on app load (check for existing session)
  useEffect(() => {
    console.log('🚀 Initializing Jarvis App...')
    const user = initializeAuth()
    if (user) {
      console.log('✅ Auto-login successful:', user.email)
      setCurrentUser(user)
    } else {
      console.log('ℹ️ No auto-login session found')
    }
    setIsInitialized(true)
  }, [setCurrentUser])

  const handleLoginSuccess = () => {
    console.log('🎉 Login successful, redirecting to HUD...')
    // Store will already be updated by LoginPage
  }

  const handleSignupSuccess = () => {
    console.log('🎉 Signup successful, redirecting to HUD...')
    // Store will already be updated by SignupPage
  }

  // Don't render until initialization is complete
  if (!isInitialized) {
    return <div className="min-h-screen bg-slate-950" />
  }

  return (
    <AnimatePresence mode="wait">
      {!isAuthenticated || !currentUser ? (
        <motion.div
          key="auth"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{ duration: 0.8 }}
        >
          {authMode === 'login' ? (
            <LoginPage 
              onSuccess={handleLoginSuccess}
              onSwitchToSignup={() => setAuthMode('signup')}
            />
          ) : (
            <SignupPage 
              onSuccess={handleSignupSuccess}
              onSwitchToLogin={() => setAuthMode('login')}
            />
          )}
        </motion.div>
      ) : (
        <motion.div
          key="hud"
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, ease: 'easeOut' }}
        >
          <JarvisHUD />
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default App
