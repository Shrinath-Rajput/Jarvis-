/**
 * BackendExecutor Service
 * ═══════════════════════════════════════════════════════════════
 * 
 * Connects the frontend to the REAL autonomous agent backend.
 * This is the single source of truth for all task execution.
 * 
 * Flow:
 * 1. User voice command → BackendExecutor.executeTask()
 * 2. Backend autonomous agent decides which tools to use
 * 3. Tools execute on the actual system
 * 4. OCR verifies results
 * 5. Agent loops until task complete
 * 6. Result returned to frontend
 * 
 * This replaces ALL fake action parsing in the frontend.
 */

const BACKEND_URL = 'http://localhost:5000'; // Flask backend address

class BackendExecutor {
  constructor() {
    this.isConnected = false;
    this.lastTaskId = null;
    this.executionHistory = [];
  }

  /**
   * Check backend health
   */
  async checkHealth() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/health`);
      const data = await response.json();
      this.isConnected = data.success;
      return data;
    } catch (error) {
      console.error('Backend health check failed:', error);
      this.isConnected = false;
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute a task using the real autonomous agent
   * 
   * This sends the task to the backend and waits for real execution
   * NOT simulated execution.
   */
  async executeTask(userCommand, options = {}) {
    const {
      maxSteps = 150,
      taskId = this._generateTaskId(),
      onProgress = null,
      pollInterval = 2000,
      timeout = 300000 // 5 minutes
    } = options;

    console.log(`[BackendExecutor] Executing: ${userCommand}`);
    
    try {
      // 1. Send task to backend
      const response = await fetch(`${BACKEND_URL}/api/autonomous/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          task: userCommand,
          max_steps: maxSteps,
          task_id: taskId
        })
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // 2. Store in history
      this.lastTaskId = taskId;
      this.executionHistory.push({
        taskId,
        command: userCommand,
        timestamp: new Date().toISOString(),
        result
      });

      console.log(`[BackendExecutor] Task completed:`, result);
      
      // 3. Return parsed result
      return this._parseBackendResult(result);

    } catch (error) {
      console.error('[BackendExecutor] Execution failed:', error);
      return {
        success: false,
        error: error.message,
        output: null,
        actionsTaken: [],
        finalScreenshot: null
      };
    }
  }

  /**
   * Get list of available tools from backend
   */
  async getAvailableTools() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/tools/list`);
      const data = await response.json();
      return data.result || [];
    } catch (error) {
      console.error('Failed to fetch tools:', error);
      return [];
    }
  }

  /**
   * Get tools by category
   */
  async getToolsByCategory() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/tools/categories`);
      const data = await response.json();
      return data.result || {};
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return {};
    }
  }

  /**
   * Search for specific tools
   */
  async searchTools(query) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/tools/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await response.json();
      return data.result || [];
    } catch (error) {
      console.error('Failed to search tools:', error);
      return [];
    }
  }

  /**
   * Get execution statistics
   */
  async getStatistics() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/stats`);
      const data = await response.json();
      return data.result || {};
    } catch (error) {
      console.error('Failed to fetch statistics:', error);
      return {};
    }
  }

  /**
   * Get action history from backend
   */
  async getActionHistory(limit = 20) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/history?limit=${limit}`);
      const data = await response.json();
      return data.result || [];
    } catch (error) {
      console.error('Failed to fetch history:', error);
      return [];
    }
  }

  /**
   * Get decision history from backend
   */
  async getDecisionHistory(limit = 20) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/decision-history?limit=${limit}`);
      const data = await response.json();
      return data.result || [];
    } catch (error) {
      console.error('Failed to fetch decision history:', error);
      return [];
    }
  }

  /**
   * Get system configuration
   */
  async getConfig() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/autonomous/config`);
      const data = await response.json();
      return data.result || {};
    } catch (error) {
      console.error('Failed to fetch config:', error);
      return {};
    }
  }

  /**
   * Parse backend result into frontend-friendly format
   */
  _parseBackendResult(result) {
    return {
      success: result.success,
      output: result.result?.summary || result.error || 'Task execution completed',
      actionsTaken: result.result?.action_history || [],
      decisions: result.result?.decision_history || [],
      finalScreenshot: result.result?.final_screenshot || null,
      statistics: result.result?.statistics || {},
      errors: result.result?.errors || [],
      completedSteps: result.result?.steps_taken || 0,
      maxSteps: result.result?.max_steps || 150,
      taskId: result.result?.task_id
    };
  }

  /**
   * Generate unique task ID
   */
  _generateTaskId() {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Format backend result for display in UI
   */
  formatForDisplay(result) {
    if (!result.success) {
      return `System error: ${result.error}`;
    }
    return result.output;
  }

  /**
   * Get execution history
   */
  getHistory() {
    return this.executionHistory;
  }

  /**
   * Clear execution history
   */
  clearHistory() {
    this.executionHistory = [];
  }
}

// Singleton instance
let executorInstance = null;

export const getBackendExecutor = () => {
  if (!executorInstance) {
    executorInstance = new BackendExecutor();
  }
  return executorInstance;
};

export default BackendExecutor;
