/**
 * FINAL STABLE BACKEND EXECUTOR
 */

const BACKEND_URL = "http://127.0.0.1:5000";

class BackendExecutor {

    constructor() {

        this.isConnected = false;
        this.executionHistory = [];
        this.lastTaskId = null;
    }

    // =========================
    // HEALTH CHECK
    // =========================

    async checkHealth() {

        try {

            const response = await fetch(

                `${BACKEND_URL}/health`

            );

            const data = await response.json();

            this.isConnected = true;

            console.log(
                "[BackendExecutor] Backend healthy"
            );

            return {

                success: true,

                data
            };

        } catch (error) {

            console.error(
                "[BackendExecutor] Health failed:",
                error
            );

            this.isConnected = false;

            return {

                success: false,

                error: error.message
            };
        }
    }

    // =========================
    // EXECUTE TASK
    // =========================

    async executeTask(command) {

        console.log(
            "[BackendExecutor] Executing:",
            command
        );

        try {

            // ---------------------
            // HEALTH CHECK
            // ---------------------

            const health =
                await this.checkHealth();

            if (!health.success) {

                throw new Error(
                    "Backend offline"
                );
            }

            // ---------------------
            // SEND REQUEST
            // ---------------------

            const response = await fetch(

                `${BACKEND_URL}/api/autonomous/execute`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        task: command,

                        max_steps: 50
                    })
                }
            );

            // ---------------------
            // RESPONSE ERROR
            // ---------------------

            if (!response.ok) {

                throw new Error(

                    `HTTP ${response.status}`
                );
            }

            // ---------------------
            // JSON
            // ---------------------

            const data =
                await response.json();

            console.log(
                "[BackendExecutor] Result:",
                data
            );

            // ---------------------
            // HISTORY
            // ---------------------

            this.executionHistory.push({

                command,

                timestamp:
                    new Date().toISOString(),

                result: data
            });

            // ---------------------
            // RETURN
            // ---------------------

            return {

                success:
                    data.success || false,

                response:
                    data.response ||

                    data.result ||

                    "Task executed",

                result: data,

                executionTime:
                    data.execution_time || 0
            };

        } catch (error) {

            console.error(
                "[BackendExecutor] Failed:",
                error
            );

            return {

                success: false,

                response:
                    "Execution failed",

                error: error.message
            };
        }
    }

    // =========================
    // HISTORY
    // =========================

    getHistory() {

        return this.executionHistory;
    }

    clearHistory() {

        this.executionHistory = [];
    }
}

// =========================
// SINGLETON
// =========================

const backendExecutor =
    new BackendExecutor();

export default backendExecutor;

export const getBackendExecutor = () => {
    return backendExecutor;
};