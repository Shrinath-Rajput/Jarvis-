import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Lock, Mail, ArrowRight, Zap } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';
import { login } from '../services/authService';
import ParticleSystem from './ParticleSystem';
import CursorGlow from './CursorGlow';

export default function LoginPage({ onSuccess, onSwitchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [textIndex, setTextIndex] = useState(0);
  const setCurrentUser = useJarvisStore(state => state.setCurrentUser);
  
  const subtitleText = "AUTHENTICATE TO ACCESS JARVIS AI SYSTEM";

  useEffect(() => {
    if (textIndex < subtitleText.length) {
      const timeout = setTimeout(() => {
        setTextIndex((prev) => prev + 1);
      }, 30);
      return () => clearTimeout(timeout);
    }
  }, [textIndex]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 800));

      // Use auth service to login
      const result = login(email, password);

      if (!result.success) {
        setError(result.error);
        setIsLoading(false);
        return;
      }

      // Update store with logged-in user
      setCurrentUser(result.user);

      // Save to localStorage for persistence
      localStorage.setItem('jarvis_current_user', JSON.stringify(result.user));

      console.log('✅ Login successful:', result.user);

      // Call success callback
      if (onSuccess) onSuccess();

    } catch (err) {
      console.error('Login error:', err);
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.1, delayChildren: 0.3 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center p-4 overflow-hidden bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))] opacity-40"></div>
      <div className="fixed inset-0 bg-grid opacity-5"></div>
      <ParticleSystem />
      <CursorGlow />

      {/* Animated scanline */}
      <div className="fixed top-0 left-0 w-full h-1/3 bg-gradient-to-b from-cyan-400/10 via-transparent to-transparent pointer-events-none z-30 animate-pulse"></div>

      {/* Main Container */}
      <motion.div
        className="relative z-20 w-full max-w-md"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        {/* Glassmorphism Card */}
        <div className="relative p-[1px] rounded-3xl overflow-hidden group">
          {/* Gradient Border */}
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl blur"></div>

          {/* Card Content */}
          <div className="relative bg-slate-900/80 backdrop-blur-xl rounded-3xl p-8 border border-cyan-500/20">
            {/* Decorative glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl -z-10"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/5 rounded-full blur-3xl -z-10"></div>

            <motion.div
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="space-y-6"
            >
              {/* Header */}
              <motion.div variants={itemVariants} className="space-y-3">
                <div className="flex items-center gap-3 justify-center">
                  <Zap className="w-8 h-8 text-cyan-400 animate-pulse" />
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                    JARVIS
                  </h1>
                  <Zap className="w-8 h-8 text-cyan-400 animate-pulse" />
                </div>
                <div className="h-1 w-16 mx-auto bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full"></div>
              </motion.div>

              {/* Subtitle */}
              <motion.p
                variants={itemVariants}
                className="text-xs text-cyan-200/60 font-mono tracking-widest text-center"
              >
                {subtitleText.substring(0, textIndex)}
                {textIndex < subtitleText.length && (
                  <span className="animate-pulse ml-1">▌</span>
                )}
              </motion.p>

              {/* Form */}
              <motion.form
                variants={itemVariants}
                onSubmit={handleLogin}
                className="space-y-4"
              >
                {/* Email Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-cyan-400/60 uppercase tracking-wider block mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 w-5 h-5 text-cyan-400/40" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="agent@jarvis.ai"
                      className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-cyan-500/20 rounded-lg text-cyan-100 placeholder-cyan-600/30 focus:outline-none focus:border-cyan-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-cyan-400/60 uppercase tracking-wider block mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 w-5 h-5 text-cyan-400/40" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full pl-10 pr-10 py-3 bg-slate-800/50 border border-cyan-500/20 rounded-lg text-cyan-100 placeholder-cyan-600/30 focus:outline-none focus:border-cyan-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-cyan-400/40 hover:text-cyan-400/80 transition-colors"
                    >
                      {showPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Error Message */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm font-mono"
                  >
                    {error}
                  </motion.div>
                )}

                {/* Remember & Forgot */}
                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded bg-slate-800 border border-cyan-500/20 cursor-pointer accent-cyan-400"
                    />
                    <span className="text-xs text-cyan-300/70 group-hover:text-cyan-300 transition-colors">
                      Remember me
                    </span>
                  </label>
                  <a
                    href="#"
                    className="text-xs text-cyan-400/60 hover:text-cyan-400 transition-colors"
                  >
                    Forgot Password?
                  </a>
                </div>

                {/* Login Button */}
                <motion.button
                  type="submit"
                  disabled={isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full mt-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-lg transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
                >
                  <span className="relative z-10">
                    {isLoading ? 'AUTHENTICATING...' : 'LOGIN'}
                  </span>
                  {!isLoading && <ArrowRight className="w-4 h-4 relative z-10" />}
                </motion.button>
              </motion.form>

              {/* Divider */}
              <motion.div
                variants={itemVariants}
                className="flex items-center gap-3"
              >
                <div className="flex-1 h-px bg-gradient-to-r from-transparent to-cyan-500/20"></div>
                <span className="text-xs text-cyan-400/40 font-mono">OR</span>
                <div className="flex-1 h-px bg-gradient-to-l from-transparent to-cyan-500/20"></div>
              </motion.div>

              {/* Signup Link */}
              <motion.button
                variants={itemVariants}
                onClick={onSwitchToSignup}
                className="w-full py-3 border border-cyan-500/30 hover:border-cyan-400/50 text-cyan-300 hover:text-cyan-200 rounded-lg font-mono text-sm transition-all duration-300 bg-slate-800/30 hover:bg-slate-800/50"
              >
                CREATE NEW ACCOUNT
              </motion.button>
            </motion.div>
          </div>
        </div>

        {/* Demo Credentials */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 20 }}
          transition={{ delay: 1 }}
          className="mt-6 p-4 bg-slate-900/50 backdrop-blur-sm border border-cyan-500/10 rounded-lg"
        >
          <p className="text-xs text-cyan-300/50 font-mono mb-2">DEMO CREDENTIALS:</p>
          <p className="text-xs text-cyan-300/70 font-mono">Email: demo@jarvis.ai</p>
          <p className="text-xs text-cyan-300/70 font-mono">Pass: password</p>
        </motion.div>
      </motion.div>
    </div>
  );
}
