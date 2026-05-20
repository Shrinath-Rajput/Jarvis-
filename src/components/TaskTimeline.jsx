import { motion } from 'framer-motion';
import { CheckCircle2, Clock, AlertCircle, Play } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';

export default function TaskTimeline() {
  const taskHistory = useJarvisStore(state => state.taskHistory);

  const recentTasks = taskHistory.slice(0, 8);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.05 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.3 } },
  };

  const getTaskIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-green-400" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      case 'running':
        return <Play className="w-4 h-4 text-cyan-400" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-400" />;
      default:
        return <Clock className="w-4 h-4 text-slate-500" />;
    }
  };

  const getTimelineColor = (status) => {
    switch (status) {
      case 'completed':
        return 'from-green-500 to-emerald-500';
      case 'failed':
        return 'from-red-500 to-orange-500';
      case 'running':
        return 'from-cyan-500 to-blue-500';
      case 'pending':
        return 'from-yellow-500 to-amber-500';
      default:
        return 'from-slate-600 to-slate-700';
    }
  };

  const getCardGradient = (status) => {
    switch (status) {
      case 'completed':
        return 'from-green-900/20 to-emerald-900/20 border-green-500/20';
      case 'failed':
        return 'from-red-900/20 to-orange-900/20 border-red-500/20';
      case 'running':
        return 'from-cyan-900/20 to-blue-900/20 border-cyan-500/20';
      case 'pending':
        return 'from-yellow-900/20 to-amber-900/20 border-yellow-500/20';
      default:
        return 'from-slate-800/20 to-slate-900/20 border-slate-500/10';
    }
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <div className="space-y-4">
      <div className="text-xs font-mono text-cyan-400/60 uppercase tracking-widest">◈ Task Timeline</div>

      {recentTasks.length > 0 ? (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar"
        >
          {recentTasks.map((task, idx) => (
            <motion.div
              key={idx}
              variants={itemVariants}
              className="relative group"
            >
              {/* Timeline Connector Line */}
              {idx < recentTasks.length - 1 && (
                <div className="absolute left-2 top-8 bottom-0 w-0.5 bg-gradient-to-b from-slate-600/50 to-transparent"></div>
              )}

              {/* Timeline Item */}
              <div className="flex gap-3">
                {/* Timeline Dot */}
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity, delay: idx * 0.1 }}
                  className={`relative mt-1 w-5 h-5 rounded-full bg-gradient-to-br ${getTimelineColor(task.status)} flex items-center justify-center flex-shrink-0 ring-2 ring-slate-900 shadow-lg`}
                >
                  <div className="absolute inset-0 rounded-full bg-white/20"></div>
                </motion.div>

                {/* Content */}
                <motion.div
                  className={`relative flex-1 p-3 bg-gradient-to-br ${getCardGradient(task.status)} backdrop-blur-lg rounded-lg border overflow-hidden hover:border-white/30 transition-all duration-300 group`}
                  whileHover={{ scale: 1.02, y: -2 }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                  <div className="relative z-10 space-y-1">
                    {/* Header */}
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2 flex-1 min-w-0">
                        {getTaskIcon(task.status)}
                        <div className="min-w-0 flex-1">
                          <div className="text-sm font-semibold text-slate-200 truncate">{task.name}</div>
                          <div className="text-xs text-slate-400/70 font-mono truncate">{task.description}</div>
                        </div>
                      </div>
                      <span className="text-xs font-mono text-slate-400 whitespace-nowrap flex-shrink-0">{formatTime(task.timestamp)}</span>
                    </div>

                    {/* Status Badge */}
                    <div className="flex items-center justify-between">
                      <motion.div
                        className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-slate-800/50 border border-slate-600/30`}
                      >
                        <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${getTimelineColor(task.status)}`}></div>
                        <span className="text-xs font-mono uppercase tracking-wider text-slate-300">{task.status}</span>
                      </motion.div>
                      {task.duration && (
                        <span className="text-xs text-slate-500 font-mono">{task.duration}</span>
                      )}
                    </div>

                    {/* Result/Error */}
                    {task.result && (
                      <div className="text-xs text-slate-400 font-mono mt-2 p-2 bg-slate-900/50 rounded border border-slate-700/30 truncate">
                        {task.result}
                      </div>
                    )}
                  </div>
                </motion.div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-8 bg-gradient-to-br from-slate-800/40 to-slate-900/40 backdrop-blur-lg rounded-lg border border-slate-600/20 text-center"
        >
          <Clock className="w-8 h-8 text-slate-500/50 mx-auto mb-2" />
          <div className="text-sm text-slate-500 font-mono">No tasks executed yet</div>
          <div className="text-xs text-slate-600 font-mono mt-1">Start a task to see timeline</div>
        </motion.div>
      )}
    </div>
  );
}
