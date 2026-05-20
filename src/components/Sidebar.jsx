import { motion } from 'framer-motion';
import { Home, Settings, LogOut, Menu, X, BarChart3, Users, Shield } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';
import { useState } from 'react';

export default function Sidebar({ onLogout }) {
  const [isOpen, setIsOpen] = useState(true);
  const currentUser = useJarvisStore(state => state.currentUser);
  const users = useJarvisStore(state => state.users);

  const menuItems = [
    { icon: Home, label: 'Dashboard', active: true },
    { icon: BarChart3, label: 'Analytics' },
    { icon: Shield, label: 'Security' },
    { icon: Users, label: 'Team' },
    { icon: Settings, label: 'Settings' },
  ];

  const sidebarVariants = {
    open: { x: 0, opacity: 1 },
    closed: { x: '-100%', opacity: 0 },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: (i) => ({
      opacity: 1,
      x: 0,
      transition: { delay: i * 0.08, duration: 0.4 },
    }),
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="md:hidden fixed bottom-6 left-6 z-50 p-3 bg-gradient-to-br from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-full shadow-lg hover:shadow-xl transition-all"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </motion.button>

      {/* Sidebar */}
      <motion.div
        variants={sidebarVariants}
        initial={false}
        animate={isOpen ? 'open' : 'closed'}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="fixed md:relative left-0 top-0 h-screen w-64 bg-gradient-to-b from-slate-900/95 to-slate-950/95 backdrop-blur-xl border-r border-cyan-500/20 z-40 md:z-10 overflow-y-auto"
      >
        {/* Sidebar Content */}
        <div className="h-full flex flex-col p-6 space-y-8">
          {/* Logo Section */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-2"
          >
            <div className="flex items-center gap-2">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center"
              >
                <div className="w-4 h-4 bg-cyan-300 rounded-full opacity-60"></div>
              </motion.div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">JARVIS</h1>
                <div className="text-xs font-mono text-cyan-400/60">AI SYSTEM</div>
              </div>
            </div>
          </motion.div>

          {/* User Profile */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="p-4 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur-lg rounded-lg border border-cyan-500/20 space-y-2"
          >
            <div className="flex items-center gap-3">
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold"
              >
                {currentUser?.name?.charAt(0) || 'A'}
              </motion.div>
              <div>
                <div className="text-sm font-semibold text-cyan-200">{currentUser?.name}</div>
                <div className="text-xs text-cyan-400/60 font-mono">{currentUser?.email}</div>
              </div>
            </div>
          </motion.div>

          {/* Navigation Menu */}
          <nav className="flex-1 space-y-2">
            <div className="text-xs font-mono text-cyan-400/40 uppercase tracking-widest px-2 mb-3">
              ◈ Navigation
            </div>
            {menuItems.map((item, i) => {
              const Icon = item.icon;
              return (
                <motion.button
                  key={i}
                  custom={i}
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  whileHover={{ x: 8, backgroundColor: 'rgba(6, 182, 212, 0.1)' }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    item.active
                      ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 text-cyan-300'
                      : 'text-slate-400 hover:text-cyan-300 border border-transparent'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-sm font-medium">{item.label}</span>
                  {item.active && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="ml-auto w-2 h-2 rounded-full bg-cyan-400"
                    />
                  )}
                </motion.button>
              );
            })}
          </nav>

          {/* Stats Section */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="space-y-2 py-4 border-y border-slate-700/50"
          >
            <div className="text-xs font-mono text-cyan-400/40 uppercase tracking-widest px-2 mb-3">
              ◈ Activity
            </div>
            <div className="flex items-center justify-between px-2 py-1">
              <span className="text-xs text-slate-400">Total Users</span>
              <span className="text-sm font-bold text-cyan-300">{users.length}</span>
            </div>
            <div className="flex items-center justify-between px-2 py-1">
              <span className="text-xs text-slate-400">Active Now</span>
              <motion.span
                animate={{ opacity: [0.5, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="text-sm font-bold text-green-400"
              >
                1
              </motion.span>
            </div>
          </motion.div>

          {/* Logout Button */}
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            whileHover={{ scale: 1.02, x: 4 }}
            whileTap={{ scale: 0.98 }}
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-red-500/20 to-orange-500/20 hover:from-red-500/30 hover:to-orange-500/30 border border-red-500/30 hover:border-red-500/50 text-red-300 rounded-lg transition-all font-medium"
          >
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Mobile Overlay */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 bg-black/40 backdrop-blur-sm md:hidden z-30"
        />
      )}
    </>
  );
}
