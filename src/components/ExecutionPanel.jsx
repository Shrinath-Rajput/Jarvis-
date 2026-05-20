import { motion } from 'framer-motion';
import { Play, Pause, Square, CheckCircle, AlertTriangle, Clock, Zap } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';

export default function ExecutionPanel() {
  const currentTask = useJarvisStore(state => state.currentTask);
  const executionLogs = useJarvisStore(state => state.executionLogs);
  const currentToolExecuting = useJarvisStore(state => state.currentToolExecuting);
  const toolLogs = useJarvisStore(state => state.toolLogs);

  const recentLogs = executionLogs.slice(0, 5);
  const recentTools = toolLogs.slice(0, 4);

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.08 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -15 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.4 } },
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-400" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'running':
        return <Zap className="w-4 h-4 text-cyan-400" />;
      default:
        return <Square className="w-4 h-4 text-slate-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'from-green-500/20 to-emerald-500/20 border-green-500/30';
      case 'error':
        return 'from-red-500/20 to-orange-500/20 border-red-500/30';
      case 'pending':
        return 'from-yellow-500/20 to-amber-500/20 border-yellow-500/30';
      case 'running':
        return 'from-cyan-500/20 to-blue-500/20 border-cyan-500/30';
      default:
        return 'from-slate-500/10 to-slate-600/10 border-slate-500/20';
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-4"
    >
      {/* Current Task */}
      <motion.div
        variants={itemVariants}
        className="relative p-4 bg-gradient-to-br from-blue-900/40 to-cyan-900/40 backdrop-blur-lg rounded-xl border border-blue-500/30 overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-cyan-500/5"></div>

        <div className="relative z-10 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-blue-400/70 uppercase tracking-widest">◈ Current Task</span>
            {currentTask && (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
              >
                <Zap className="w-4 h-4 text-blue-400" />
              </motion.div>
            )}
          </div>

          {currentTask ? (
            <div className="space-y-2">
              <div className="text-sm font-bold text-blue-200">{currentTask.name}</div>
              <div className="text-xs text-blue-300/60 font-mono">{currentTask.description}</div>
              <div className="flex items-center gap-2 mt-2">
                <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                    animate={{ width: ['0%', '75%'] }}
                    transition={{ duration: 3, repeat: Infinity }}
                  />
                </div>
                <span className="text-xs text-blue-300/50 font-mono">In Progress</span>
              </div>
            </div>
          ) : (
            <div className="text-sm text-slate-400 font-mono text-center py-2">
              Awaiting task execution...
            </div>
          )}
        </div>
      </motion.div>

      {/* Tool Execution Status */}
      {currentToolExecuting && (
        <motion.div
          variants={itemVariants}
          className="relative p-4 bg-gradient-to-br from-purple-900/40 to-pink-900/40 backdrop-blur-lg rounded-xl border border-purple-500/30 overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-pink-500/5"></div>

          <div className="relative z-10 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-purple-400/70 uppercase tracking-widest">◈ Active Tool</span>
              <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ duration: 0.8, repeat: Infinity }}>
                <Play className="w-4 h-4 text-purple-400" />
              </motion.div>
            </div>

            <div className="space-y-1">
              <div className="text-sm font-bold text-purple-200">{currentToolExecuting.name}</div>
              <div className="text-xs text-purple-300/60">{currentToolExecuting.status}</div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Execution Logs */}
      <motion.div
        variants={itemVariants}
        className="space-y-2"
      >
        <div className="text-xs font-mono text-cyan-400/60 uppercase tracking-widest px-1">◈ Recent Executions</div>
        {recentLogs.length > 0 ? (
          <div className="space-y-2 max-h-48 overflow-y-auto custom-scrollbar">
            {recentLogs.map((log, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
                className={`relative p-3 bg-gradient-to-br ${getStatusColor(log.status)} backdrop-blur-lg rounded-lg border overflow-hidden group hover:border-white/20 transition-colors`}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/3 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                <div className="relative z-10 flex items-start gap-2">
                  {getStatusIcon(log.status)}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-mono text-slate-300 truncate">{log.action}</span>
                      <span className="text-xs text-slate-400 font-mono whitespace-nowrap">{log.timestamp}</span>
                    </div>
                    {log.details && (
                      <div className="text-xs text-slate-400/70 font-mono mt-1 truncate">{log.details}</div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="p-3 bg-slate-800/40 backdrop-blur-lg rounded-lg border border-slate-600/20 text-center">
            <div className="text-xs text-slate-500 font-mono">No executions yet</div>
          </div>
        )}
      </motion.div>

      {/* Tool Activity */}
      {recentTools.length > 0 && (
        <motion.div
          variants={itemVariants}
          className="space-y-2"
        >
          <div className="text-xs font-mono text-purple-400/60 uppercase tracking-widest px-1">◈ Tool Activity</div>
          <div className="grid grid-cols-2 gap-2">
            {recentTools.map((tool, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.08 }}
                className="relative p-3 bg-gradient-to-br from-slate-800/60 to-slate-900/60 backdrop-blur-lg rounded-lg border border-slate-600/30 overflow-hidden group hover:border-purple-500/30 transition-colors"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                <div className="relative z-10 space-y-1">
                  <div className="flex items-center gap-1.5">
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1.5, repeat: Infinity, delay: idx * 0.1 }}
                      className={`w-1.5 h-1.5 rounded-full ${
                        tool.status === 'running' ? 'bg-green-400' : 'bg-slate-500'
                      }`}
                    />
                    <span className="text-xs font-mono text-slate-300 truncate">{tool.name}</span>
                  </div>
                  <div className="text-xs text-slate-500 font-mono">{tool.status}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
