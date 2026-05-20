import { motion } from 'framer-motion';
import { Mic, MicOff, Brain, Zap } from 'lucide-react';
import { useJarvisStore } from '../stores/jarvisStore';

export default function VoiceOrb() {
  const isListening = useJarvisStore(state => state.isListening);
  const isSpeaking = useJarvisStore(state => state.isSpeaking);
  const aiStatus = useJarvisStore(state => state.aiStatus);
  const voiceLevel = useJarvisStore(state => state.voiceLevel);

  const getStatusColor = () => {
    if (isSpeaking) return 'from-orange-500 via-amber-500 to-yellow-500';
    if (isListening) return 'from-cyan-500 via-blue-500 to-indigo-500';
    if (aiStatus === 'thinking') return 'from-purple-500 via-pink-500 to-purple-600';
    if (aiStatus === 'executing') return 'from-green-500 via-emerald-500 to-teal-500';
    return 'from-slate-600 via-slate-700 to-slate-800';
  };

  const getGlowColor = () => {
    if (isSpeaking) return 'shadow-[0_0_40px_rgba(249,115,22,0.6)]';
    if (isListening) return 'shadow-[0_0_40px_rgba(6,182,212,0.6)]';
    if (aiStatus === 'thinking') return 'shadow-[0_0_40px_rgba(168,85,247,0.6)]';
    if (aiStatus === 'executing') return 'shadow-[0_0_40px_rgba(34,197,94,0.6)]';
    return 'shadow-[0_0_20px_rgba(100,116,139,0.3)]';
  };

  const getBorderColor = () => {
    if (isSpeaking) return 'from-orange-400 to-amber-400';
    if (isListening) return 'from-cyan-400 to-blue-400';
    if (aiStatus === 'thinking') return 'from-purple-400 to-pink-400';
    if (aiStatus === 'executing') return 'from-green-400 to-emerald-400';
    return 'from-slate-500 to-slate-600';
  };

  return (
    <div className="relative w-64 h-64 flex items-center justify-center">
      {/* Outer Rotating Ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 12, repeat: Infinity, ease: 'linear' }}
        className={`absolute inset-0 rounded-full border border-transparent bg-gradient-to-r ${getBorderColor()} opacity-30`}
      />

      {/* Animated Particle Ring */}
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        className="absolute inset-3 rounded-full"
        style={{
          background: `conic-gradient(from 0deg, transparent, rgba(6,182,212,0.4), transparent 50%)`,
          opacity: isListening || isSpeaking ? 1 : 0.3,
        }}
      />

      {/* Pulsing Energy Ring */}
      {(isListening || isSpeaking || aiStatus === 'thinking') && (
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.8, 0.2, 0.8] }}
          transition={{ duration: 2.5, repeat: Infinity }}
          className={`absolute inset-6 rounded-full border-2 border-transparent bg-gradient-to-r ${getBorderColor()}`}
        />
      )}

      {/* Inner Thinking Ring */}
      {aiStatus === 'thinking' && (
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
          className="absolute inset-14 rounded-full border border-purple-400/40"
        />
      )}

      {/* Main Orb Glass Effect */}
      <motion.div
        animate={{
          scale: isListening || isSpeaking || aiStatus === 'thinking' ? [1, 1.08, 1] : 1,
        }}
        transition={{ duration: 0.6, repeat: isListening || isSpeaking || aiStatus === 'thinking' ? Infinity : false }}
        className={`relative z-10 w-32 h-32 rounded-full bg-gradient-to-br ${getStatusColor()} ${getGlowColor()} flex items-center justify-center overflow-hidden backdrop-blur-md border-2 border-white/10`}
      >
        {/* Premium Glass Inner Glow */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-tl from-white/30 to-transparent opacity-40" />
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-transparent to-black/20 opacity-30" />

        {/* Holographic Core Effect */}
        <div className="absolute top-2 left-2 w-8 h-8 bg-white/20 rounded-full blur-xl" />

        {/* Icon Container */}
        <motion.div
          animate={{
            scale: isListening || isSpeaking ? [1, 0.9, 1] : 1,
          }}
          transition={{ duration: 0.4, repeat: isListening || isSpeaking ? Infinity : false }}
          className="relative z-20"
        >
          {isSpeaking ? (
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            >
              <Mic className="w-14 h-14 text-white drop-shadow-lg" />
            </motion.div>
          ) : isListening ? (
            <motion.div
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <Mic className="w-14 h-14 text-white drop-shadow-lg" />
            </motion.div>
          ) : aiStatus === 'thinking' ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            >
              <Brain className="w-14 h-14 text-white drop-shadow-lg" />
            </motion.div>
          ) : aiStatus === 'executing' ? (
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 0.6, repeat: Infinity }}
            >
              <Zap className="w-14 h-14 text-white drop-shadow-lg" />
            </motion.div>
          ) : (
            <Mic className="w-14 h-14 text-white/60 drop-shadow-lg" />
          )}
        </motion.div>

        {/* Waveform Visualization */}
        {(isListening || isSpeaking || aiStatus === 'thinking') && (
          <svg className="absolute inset-0 w-full h-full" viewBox="0 0 128 128" preserveAspectRatio="xMidYMid meet">
            {[0, 1, 2, 3, 4, 5, 6].map((i) => (
              <motion.g
                key={i}
                animate={{
                  scaleY: [1, 0.6, 1, 0.7, 1][i % 5],
                  opacity: [0.8, 1, 0.8],
                }}
                transition={{
                  duration: 0.5,
                  repeat: Infinity,
                  delay: i * 0.08,
                }}
                style={{ transformOrigin: `${20 + i * 16}px 64px` }}
              >
                <line
                  x1={20 + i * 16}
                  y1="50"
                  x2={20 + i * 16}
                  y2="78"
                  stroke={isSpeaking ? '#fbbf24' : isListening ? '#06b6d4' : '#a855f7'}
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </motion.g>
            ))}
          </svg>
        )}
      </motion.div>

      {/* Rotating Voice Level Ring */}
      {(isListening || isSpeaking) && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
          className="absolute inset-0 rounded-full border border-dashed border-cyan-400/40"
          style={{
            opacity: 0.4 + voiceLevel * 0.6,
          }}
        />
      )}

      {/* Status Indicator Badge */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="absolute -bottom-16 text-center space-y-1"
      >
        <div className="text-sm font-bold text-cyan-300 uppercase tracking-widest">
          {isSpeaking && (
            <motion.span animate={{ opacity: [0.5, 1] }} transition={{ duration: 0.6, repeat: Infinity }}>
              ◆ SPEAKING
            </motion.span>
          )}
          {isListening && (
            <motion.span animate={{ opacity: [0.5, 1] }} transition={{ duration: 0.6, repeat: Infinity }}>
              ◆ LISTENING
            </motion.span>
          )}
          {aiStatus === 'thinking' && (
            <motion.span animate={{ opacity: [0.5, 1] }} transition={{ duration: 0.6, repeat: Infinity }}>
              ◆ THINKING
            </motion.span>
          )}
          {aiStatus === 'executing' && (
            <motion.span animate={{ opacity: [0.5, 1] }} transition={{ duration: 0.6, repeat: Infinity }}>
              ◆ EXECUTING
            </motion.span>
          )}
          {aiStatus === 'idle' && !isListening && !isSpeaking && (
            <span className="text-slate-400">◆ STANDBY</span>
          )}
        </div>
        <div className="text-xs text-cyan-500/60 font-mono">JARVIS CORE</div>
      </motion.div>
    </div>
  );
}
