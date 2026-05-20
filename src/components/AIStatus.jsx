import { motion } from 'framer-motion';
import { Activity, Zap, Radio, Cpu, Network, AlertCircle } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';

export default function AIStatus() {
  const aiStatus = useJarvisStore(state => state.aiStatus);
  const systemStatus = useJarvisStore(state => state.systemStatus);
  const backendStatus = useJarvisStore(state => state.backendStatus);

  const getStatusIndicator = (status) => {
    switch (status) {
      case 'ready':
        return { color: 'from-green-500 to-emerald-500', text: 'OPERATIONAL', glow: 'shadow-green-500/50' };
      case 'idle':
        return { color: 'from-slate-500 to-slate-600', text: 'IDLE', glow: 'shadow-slate-500/30' };
      case 'connected':
        return { color: 'from-cyan-500 to-blue-500', text: 'CONNECTED', glow: 'shadow-cyan-500/50' };
      case 'connecting':
        return { color: 'from-yellow-500 to-amber-500', text: 'CONNECTING...', glow: 'shadow-yellow-500/50' };
      case 'disconnected':
        return { color: 'from-red-500 to-orange-500', text: 'OFFLINE', glow: 'shadow-red-500/50' };
      default:
        return { color: 'from-slate-600 to-slate-700', text: 'UNKNOWN', glow: 'shadow-slate-600/30' };
    }
  };

  const aiIndicator = getStatusIndicator(aiStatus);
  const backendIndicator = getStatusIndicator(backendStatus);
  const systemIndicators = [
    { label: 'AI Engine', value: systemStatus.ai, icon: Cpu },
    { label: 'Browser', value: systemStatus.browser, icon: Radio },
    { label: 'Executor', value: systemStatus.executor, icon: Zap },
  ];

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -10 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.4 } },
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-4"
    >
      {/* Main AI Status */}
      <motion.div
        variants={itemVariants}
        className="relative p-4 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-lg rounded-xl border border-cyan-500/20 overflow-hidden group"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

        <div className="relative z-10 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-cyan-400/70 uppercase tracking-widest">◈ AI Status</span>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
              className="w-2 h-2 rounded-full bg-cyan-400"
            />
          </div>

          <div className="flex items-center gap-3">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className={`w-3 h-3 rounded-full bg-gradient-to-r ${aiIndicator.color} shadow-lg ${aiIndicator.glow}`}
            />
            <div>
              <div className="text-sm font-bold text-cyan-200">{aiIndicator.text}</div>
              <div className="text-xs text-cyan-300/50 font-mono">Core Processor</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Backend Status */}
      <motion.div
        variants={itemVariants}
        className="relative p-4 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-lg rounded-xl border border-blue-500/20 overflow-hidden group"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

        <div className="relative z-10 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-blue-400/70 uppercase tracking-widest">◈ Backend</span>
            <motion.div
              animate={{ scale: [1, 1.5, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <Network className="w-3.5 h-3.5 text-blue-400" />
            </motion.div>
          </div>

          <div className="flex items-center gap-3">
            <motion.div
              animate={{ opacity: [0.5, 1] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className={`w-3 h-3 rounded-full bg-gradient-to-r ${backendIndicator.color} shadow-lg ${backendIndicator.glow}`}
            />
            <div>
              <div className="text-sm font-bold text-blue-200">{backendIndicator.text}</div>
              <div className="text-xs text-blue-300/50 font-mono">Server Connection</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* System Modules */}
      <div className="space-y-2">
        <div className="text-xs font-mono text-cyan-400/60 uppercase tracking-widest px-1">◈ System Modules</div>
        {systemIndicators.map((module, idx) => {
          const indicator = getStatusIndicator(module.value);
          const Icon = module.icon;

          return (
            <motion.div
              key={idx}
              variants={itemVariants}
              className="relative p-3 bg-gradient-to-br from-slate-800/40 to-slate-900/40 backdrop-blur-lg rounded-lg border border-slate-600/20 overflow-hidden group hover:border-purple-500/30 transition-colors"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/3 to-cyan-500/3 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <div className="relative z-10 flex items-center gap-2">
                <motion.div
                  animate={{ scale: [1, 1.1, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: idx * 0.1 }}
                  className={`w-2 h-2 rounded-full bg-gradient-to-r ${indicator.color}`}
                />

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Icon className="w-3 h-3 text-purple-400/60" />
                      <span className="text-xs font-mono text-slate-300">{module.label}</span>
                    </div>
                    <span className="text-xs font-bold text-green-400 uppercase">{indicator.text}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Performance Metrics */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-2 gap-2"
      >
        {[
          { label: 'Response Time', value: '240ms', color: 'from-cyan-500 to-blue-500' },
          { label: 'Memory Usage', value: '64%', color: 'from-purple-500 to-pink-500' },
          { label: 'CPU Load', value: '42%', color: 'from-green-500 to-emerald-500' },
          { label: 'Uptime', value: '99.9%', color: 'from-yellow-500 to-orange-500' },
        ].map((metric, idx) => (
          <motion.div
            key={idx}
            animate={{ y: [0, -2, 0] }}
            transition={{ duration: 2, repeat: Infinity, delay: idx * 0.1 }}
            className="p-3 bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-lg rounded-lg border border-slate-600/30"
          >
            <div className="text-xs font-mono text-slate-400 mb-1">{metric.label}</div>
            <div className={`text-sm font-bold bg-gradient-to-r ${metric.color} bg-clip-text text-transparent`}>
              {metric.value}
            </div>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}
