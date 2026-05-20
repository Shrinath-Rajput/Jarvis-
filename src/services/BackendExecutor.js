/**
 * FINAL REAL AUTONOMOUS BACKEND EXECUTOR
 */

const BACKEND_URL = "http://127.0.0.1:5000";

class BackendExecutor {

    constructor() {

        this.isConnected = false;

        this.executionHistory = [];
    }

    // ====================================================
    // HEALTH
    // ====================================================

    async checkHealth() {

        try {

            const response = await fetch(

                `${BACKEND_URL}/health`
            );

            const data =
                await response.json();

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

    // ====================================================
    // EXECUTE TASK
    // ====================================================

    async executeTask(command) {

        console.log(
            "[BackendExecutor] Executing:",
            command
        );

        try {

            // ============================================
            // HEALTH
            // ============================================

            const health =
                await this.checkHealth();

            if (!health.success) {

                throw new Error(
                    "Backend offline"
                );
            }

            // ============================================
            // REQUEST
            // ============================================

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

            // ============================================
            // HTTP ERROR
            // ============================================

            if (!response.ok) {

                throw new Error(

                    `HTTP ${response.status}`
                );
            }

            // ============================================
            // JSON
            // ============================================

            const data =
                await response.json();

            console.log(
                "[BackendExecutor] Result:",
                data
            );

            // ============================================
            // HISTORY
            // ============================================

            this.executionHistory.push({

                command,

                timestamp:
                    new Date().toISOString(),

                result: data
            });

            // ============================================
            // FORCE SUCCESS DETECTION
            // ============================================

            const isSuccess =

                data?.success === true ||

                data?.status === "completed" ||

                data?.status === "success" ||

                data?.response ===
                    "Task completed successfully";

            // ============================================
            // FAILED
            // ============================================

            if (!isSuccess) {

                console.error(
                    "[BackendExecutor] Task failed"
                );

                return {

                    success: false,

                    status: "failed",

                    response:

                        data?.response ||

                        data?.error ||

                        data?.message ||

                        "Task failed",

                    result: data,

                    executionTime:
                        data?.execution_time || 0
                };
            }

            // ============================================
            // SUCCESS
            // ============================================

            console.log(
                "[BackendExecutor] Task success"
            );

            return {

                success: true,

                status: "completed",

                response:

                    data?.response ||

                    data?.message ||

                    "Task completed successfully",

                result: data,

                executionTime:
                    data?.execution_time || 0
            };

        } catch (error) {

            console.error(
                "[BackendExecutor] Failed:",
                error
            );

            return {

                success: false,

                status: "failed",

                response:
                    "Execution failed",

                error: error.message
            };
        }
    }

    // ====================================================
    // HISTORY
    // ====================================================

    getHistory() {

        return this.executionHistory;
    }

    // ====================================================
    // CLEAR
    // ====================================================

    clearHistory() {

        this.executionHistory = [];
    }
}

const backendExecutor =
    new BackendExecutor();

export default backendExecutor;

export const getBackendExecutor = () => {

    return backendExecutor;
};