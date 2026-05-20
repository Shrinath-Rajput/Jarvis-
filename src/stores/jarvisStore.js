import { create } from 'zustand';
import { getCurrentUser, getAllUsers } from '../services/authService';

export const useJarvisStore = create((set) => ({
  // Auth State
  currentUser: getCurrentUser(), // Auto-load from localStorage
  isAuthenticated: getCurrentUser() !== null,
  users: getAllUsers(), // Load users from localStorage

  // Voice State
  isListening: false,
  isSpeaking: false,
  voiceLevel: 0,

  // Task State
  currentTask: null,
  executionLogs: [],
  taskHistory: [],

  // AI State
  aiStatus: 'idle', // idle, listening, thinking, executing, speaking
  aiResponse: '',
  isProcessing: false,

  // Backend State
  backendStatus: 'connecting', // connecting, connected, disconnected
  systemStatus: {
    ai: 'ready',
    browser: 'ready',
    executor: 'ready',
  },
  
  // Tool Activity
  toolLogs: [],
  currentToolExecuting: null,

  // Admin Panel State
  totalUsers: 0,
  activeUsers: 0,
  recentLogins: [],

  // Auth Actions
  setCurrentUser: (user) => set({
    currentUser: user,
    isAuthenticated: !!user,
  }),

  logout: () => set({
    currentUser: null,
    isAuthenticated: false,
  }),

  // Voice Actions
  setIsListening: (listening) => set({ isListening: listening }),
  setIsSpeaking: (speaking) => set({ isSpeaking: speaking }),
  setVoiceLevel: (level) => set({ voiceLevel: level }),

  // Task Actions
  setCurrentTask: (task) => set({ currentTask: task }),
  addExecutionLog: (log) => set((state) => ({
    executionLogs: [log, ...state.executionLogs].slice(0, 100),
  })),
  clearExecutionLogs: () => set({ executionLogs: [] }),
  addTaskToHistory: (task) => set((state) => ({
    taskHistory: [task, ...state.taskHistory].slice(0, 50),
  })),

  // AI Actions
  setAiStatus: (status) => set({ aiStatus: status }),
  setAiResponse: (response) => set({ aiResponse: response }),
  setIsProcessing: (processing) => set({ isProcessing: processing }),

  // Backend Actions
  setBackendStatus: (status) => set({ backendStatus: status }),
  setSystemStatus: (status) => set({ systemStatus: status }),

  // Tool Actions
  setCurrentToolExecuting: (tool) => set({ currentToolExecuting: tool }),
  addToolLog: (log) => set((state) => ({
    toolLogs: [log, ...state.toolLogs].slice(0, 100),
  })),

  // Admin Actions
  updateAdminStats: () => set((state) => {
    const users = state.users;
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
    const recentLogins = users
      .filter(u => new Date(u.lastActive) > oneHourAgo)
      .map(u => ({
        name: u.name,
        email: u.email,
        time: u.lastActive,
      }))
      .slice(0, 10);

    return {
      totalUsers: users.length,
      activeUsers: recentLogins.length,
      recentLogins,
    };
  }),

  // Reset on logout
  reset: () => set({
    currentTask: null,
    executionLogs: [],
    aiStatus: 'idle',
    aiResponse: '',
    isListening: false,
    isSpeaking: false,
  }),
}));
