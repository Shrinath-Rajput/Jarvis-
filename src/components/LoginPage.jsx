import { useState } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Lock, Mail, LogIn } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';
import ParticleSystem from './ParticleSystem';

export default function LoginPage({ onSuccess, onSwitchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const setCurrentUser = useJarvisStore(state => state.setCurrentUser);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 800));

      if (!email || !password) {
        setError('Please fill in all fields');
        setIsLoading(false);
        return;
      }

      if (!email.includes('@')) {
        setError('Please enter a valid email');
        setIsLoading(false);
        return;
      }

      // Check if user exists
      const users = JSON.parse(localStorage.getItem('jarvis_users') || '[]');
      const user = users.find(u => u.email === email);

      if (!user) {
        setError('User not found. Please sign up first.');
        setIsLoading(false);
        return;
      }

      if (user.password !== password) {
        setError('Invalid password');
        setIsLoading(false);
        return;
      }

      // Update last active
      const updatedUsers = users.map(u =>
        u.email === email ? { ...u, lastActive: new Date().toISOString() } : u
      );
      localStorage.setItem('jarvis_users', JSON.stringify(updatedUsers));

      const userData = {
        name: user.name,
        email: user.email,
        loginTime: new Date().toISOString(),
      };

      if (rememberMe) {
        localStorage.setItem('jarvis_remembered_user', JSON.stringify(userData));
      }

      setCurrentUser(userData);
      onSuccess();
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      <ParticleSystem />

      {/* Gradient Background */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl opacity-20" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl opacity-20" />
      </div>

      {/* Content */}
      <div className="relative h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="w-full max-w-md"
        >
          {/* Glass Card */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl">
            {/* Header */}
            <div className="text-center mb-8">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                className="inline-block mb-4"
              >
                <div className="w-16 h-16 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-400/50">
                  <Lock className="w-8 h-8" />
                </div>
              </motion.div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                JARVIS
              </h1>
              <p className="text-gray-300 mt-2">AI Assistant Login</p>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-3 bg-red-500/20 border border-red-500/50 rounded-xl text-red-300 text-sm"
              >
                {error}
              </motion.div>
            )}

            {/* Form */}
            <form onSubmit={handleLogin} className="space-y-4">
              {/* Email Input */}
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-400">
                  <Mail className="w-5 h-5" />
                </div>
                <input
                  type="email"
                  placeholder="Email Address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-white/5 border border-white/20 rounded-xl pl-12 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400/50 focus:bg-white/10 transition-all"
                />
              </div>

              {/* Password Input */}
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-400">
                  <Lock className="w-5 h-5" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-white/5 border border-white/20 rounded-xl pl-12 pr-12 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-400/50 focus:bg-white/10 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-cyan-400 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>

              {/* Remember & Forgot */}
              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-cyan-400 transition-colors">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 rounded bg-white/10 border border-white/20"
                  />
                  Remember Me
                </label>
                <button type="button" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                  Forgot Password?
                </button>
              </div>

              {/* Login Button */}
              <motion.button
                type="submit"
                disabled={isLoading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-all disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <LogIn className="w-5 h-5" />
                    Enter JARVIS
                  </>
                )}
              </motion.button>
            </form>

            {/* Signup Link */}
            <div className="mt-6 text-center text-gray-400">
              Don't have an account?{' '}
              <button
                onClick={onSwitchToSignup}
                className="text-cyan-400 hover:text-cyan-300 font-semibold transition-colors"
              >
                Sign Up
              </button>
            </div>
          </div>

          {/* Demo Notice */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="mt-6 text-center text-xs text-gray-400"
          >
            <p>Demo Account: demo@jarvis.ai / password</p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
