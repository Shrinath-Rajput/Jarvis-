import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Lock, Mail, User, ArrowRight, Zap } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';
import { signup } from '../services/authService';
import ParticleSystem from './ParticleSystem';
import CursorGlow from './CursorGlow';

export default function SignupPage({ onSuccess, onSwitchToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [textIndex, setTextIndex] = useState(0);
  const setCurrentUser = useJarvisStore(state => state.setCurrentUser);

  const subtitleText = "JOIN THE JARVIS AI SYSTEM";

  useEffect(() => {
    if (textIndex < subtitleText.length) {
      const timeout = setTimeout(() => {
        setTextIndex((prev) => prev + 1);
      }, 30);
      return () => clearTimeout(timeout);
    }
  }, [textIndex]);

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 800));

      // Validate passwords match
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        setIsLoading(false);
        return;
      }

      // Use auth service to signup
      const result = signup(name, email, password);

      if (!result.success) {
        setError(result.error);
        setIsLoading(false);
        return;
      }

      // Update store with logged-in user
      setCurrentUser(result.user);

      // Save to localStorage for persistence
      localStorage.setItem('jarvis_current_user', JSON.stringify(result.user));

      console.log('✅ Signup successful:', result.user);

      // Call success callback
      if (onSuccess) onSuccess();

    } catch (err) {
      console.error('Signup error:', err);
      setError('Signup failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.08, delayChildren: 0.2 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center p-4 overflow-hidden bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(168,85,247,0.3),rgba(255,255,255,0))] opacity-40"></div>
      <div className="fixed inset-0 bg-grid opacity-5"></div>
      <ParticleSystem />
      <CursorGlow />

      {/* Animated scanline */}
      <div className="fixed top-0 left-0 w-full h-1/3 bg-gradient-to-b from-blue-400/10 via-transparent to-transparent pointer-events-none z-30 animate-pulse"></div>

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
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl blur"></div>

          {/* Card Content */}
          <div className="relative bg-slate-900/80 backdrop-blur-xl rounded-3xl p-8 border border-blue-500/20">
            {/* Decorative glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/5 rounded-full blur-3xl -z-10"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl -z-10"></div>

            <motion.div
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="space-y-5"
            >
              {/* Header */}
              <motion.div variants={itemVariants} className="space-y-3">
                <div className="flex items-center gap-3 justify-center">
                  <Zap className="w-8 h-8 text-blue-400 animate-pulse" />
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                    REGISTER
                  </h1>
                  <Zap className="w-8 h-8 text-blue-400 animate-pulse" />
                </div>
                <div className="h-1 w-16 mx-auto bg-gradient-to-r from-blue-400 to-purple-500 rounded-full"></div>
              </motion.div>

              {/* Subtitle */}
              <motion.p
                variants={itemVariants}
                className="text-xs text-blue-200/60 font-mono tracking-widest text-center"
              >
                {subtitleText.substring(0, textIndex)}
                {textIndex < subtitleText.length && (
                  <span className="animate-pulse ml-1">▌</span>
                )}
              </motion.p>

              {/* Form */}
              <motion.form
                variants={itemVariants}
                onSubmit={handleSignup}
                className="space-y-4"
              >
                {/* Name Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-blue-400/60 uppercase tracking-wider block mb-2">
                    Full Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 w-5 h-5 text-blue-400/40" />
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Your Name"
                      className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-blue-500/20 rounded-lg text-blue-100 placeholder-blue-600/30 focus:outline-none focus:border-blue-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                  </div>
                </div>

                {/* Email Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-blue-400/60 uppercase tracking-wider block mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 w-5 h-5 text-blue-400/40" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="agent@jarvis.ai"
                      className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-blue-500/20 rounded-lg text-blue-100 placeholder-blue-600/30 focus:outline-none focus:border-blue-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                  </div>
                </div>

                {/* Password Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-blue-400/60 uppercase tracking-wider block mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 w-5 h-5 text-blue-400/40" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full pl-10 pr-10 py-3 bg-slate-800/50 border border-blue-500/20 rounded-lg text-blue-100 placeholder-blue-600/30 focus:outline-none focus:border-blue-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-blue-400/40 hover:text-blue-400/80 transition-colors"
                    >
                      {showPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Confirm Password Input */}
                <div className="relative group">
                  <label className="text-xs font-mono text-blue-400/60 uppercase tracking-wider block mb-2">
                    Confirm Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 w-5 h-5 text-blue-400/40" />
                    <input
                      type={showConfirm ? 'text' : 'password'}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full pl-10 pr-10 py-3 bg-slate-800/50 border border-blue-500/20 rounded-lg text-blue-100 placeholder-blue-600/30 focus:outline-none focus:border-blue-400/50 focus:bg-slate-800/70 transition-all duration-300 font-mono text-sm"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirm(!showConfirm)}
                      className="absolute right-3 top-3 text-blue-400/40 hover:text-blue-400/80 transition-colors"
                    >
                      {showConfirm ? (
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

                {/* Signup Button */}
                <motion.button
                  type="submit"
                  disabled={isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full mt-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-400 hover:to-purple-500 text-white font-bold rounded-lg transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span>
                    {isLoading ? 'CREATING ACCOUNT...' : 'CREATE ACCOUNT'}
                  </span>
                  {!isLoading && <ArrowRight className="w-4 h-4" />}
                </motion.button>
              </motion.form>

              {/* Divider */}
              <motion.div
                variants={itemVariants}
                className="flex items-center gap-3"
              >
                <div className="flex-1 h-px bg-gradient-to-r from-transparent to-blue-500/20"></div>
                <span className="text-xs text-blue-400/40 font-mono">OR</span>
                <div className="flex-1 h-px bg-gradient-to-l from-transparent to-blue-500/20"></div>
              </motion.div>

              {/* Login Link */}
              <motion.button
                variants={itemVariants}
                onClick={onSwitchToLogin}
                className="w-full py-3 border border-blue-500/30 hover:border-blue-400/50 text-blue-300 hover:text-blue-200 rounded-lg font-mono text-sm transition-all duration-300 bg-slate-800/30 hover:bg-slate-800/50"
              >
                BACK TO LOGIN
              </motion.button>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
