// src/components/JarvisHUD.jsx

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

import {
  Mic,
  Send,
  Volume2,
  Zap
} from "lucide-react";

import backendExecutor from "../services/BackendExecutor";
import { voiceEngine } from "../services/VoiceEngine";
import { getGeminiResponse } from "../services/GeminiBrain";

export default function JarvisHUD() {

  // =====================================================
  // STATES
  // =====================================================

  const [input, setInput] = useState("");

  const [response, setResponse] = useState("");

  const [logs, setLogs] = useState([]);

  const [status, setStatus] = useState("IDLE");

  const [time, setTime] = useState("");

  const [listening, setListening] = useState(false);

  // =====================================================
  // CLOCK
  // =====================================================

  useEffect(() => {

    const updateClock = () => {

      const now = new Date();

      setTime(
        now.toLocaleTimeString()
      );
    };

    updateClock();

    const interval =
      setInterval(updateClock, 1000);

    return () =>
      clearInterval(interval);

  }, []);

  // =====================================================
  // LOGS
  // =====================================================

  const addLog = (
    title,
    detail,
    type = "info"
  ) => {

    setLogs(prev => [

      {

        title,

        detail:

          typeof detail === "object"

            ? JSON.stringify(detail, null, 2)

            : String(detail),

        type,

        time:
          new Date().toLocaleTimeString(),

      },

      ...prev,
    ]);
  };

  // =====================================================
  // VOICE
  // =====================================================

  const startVoice = async () => {

    try {

      setListening(true);

      setStatus("LISTENING");

      const transcript =
        await voiceEngine.startListening();

      if (transcript) {

        setInput(transcript);

        handleSubmit(
          null,
          transcript
        );
      }

    } catch (err) {

      console.error(err);

      addLog(
        "VOICE ERROR",
        err.message,
        "error"
      );

    } finally {

      setListening(false);

      setStatus("IDLE");
    }
  };

  // =====================================================
  // SUBMIT
  // =====================================================

  const handleSubmit = async (
    e,
    voiceText = ""
  ) => {

    if (e) e.preventDefault();

    const query =
      voiceText || input;

    if (!query.trim()) return;

    try {

      // ===============================================
      // THINKING
      // ===============================================

      setStatus("THINKING");

      addLog(
        "QUERY",
        query,
        "running"
      );

      // ===============================================
      // GEMINI RESPONSE
      // ===============================================

      const aiResponse =
        await getGeminiResponse(query);

      setResponse(

        typeof aiResponse === "object"

          ? JSON.stringify(aiResponse, null, 2)

          : String(aiResponse)
      );

      // ===============================================
      // SPEAKING
      // ===============================================

      setStatus("SPEAKING");

      try {

        await voiceEngine.speak(
          typeof aiResponse === "string"

            ? aiResponse

            : "Task processing"
        );

      } catch {

        console.log(
          "Speech skipped"
        );
      }

      // ===============================================
      // EXECUTION
      // ===============================================

      setStatus("EXECUTING");

      const result =
        await backendExecutor.executeTask(query);

      console.log(
        "[REAL RESULT]",
        result
      );

      // ===============================================
      // FAILED
      // ===============================================

      if (!result.success) {

        setStatus("FAILED");

        addLog(
          "TASK FAILED",

          result,

          "error"
        );

        setResponse(

          typeof result === "object"

            ? JSON.stringify(result, null, 2)

            : String(result)
        );

        return;
      }

      // ===============================================
      // SUCCESS
      // ===============================================

      setStatus("SUCCESS");

      addLog(
        "TASK COMPLETED",

        result,

        "success"
      );

      setResponse(

        typeof result === "object"

          ? JSON.stringify(result, null, 2)

          : String(result)
      );

    } catch (err) {

      console.error(err);

      setStatus("ERROR");

      addLog(
        "SYSTEM ERROR",

        err.message,

        "error"
      );

      setResponse(

        typeof err === "object"

          ? JSON.stringify(err, null, 2)

          : String(err)
      );

    } finally {

      setInput("");

      setTimeout(() => {

        setStatus("IDLE");

      }, 3000);
    }
  };

  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="min-h-screen bg-[#050816] text-white overflow-hidden">

      {/* GRID */}

      <div className="absolute inset-0 opacity-20">

        <div
          className="w-full h-full"
          style={{
            backgroundImage:
              "linear-gradient(rgba(0,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,255,0.08) 1px, transparent 1px)",
            backgroundSize:
              "40px 40px",
          }}
        />
      </div>

      {/* MAIN */}

      <div className="relative z-10 flex h-screen">

        {/* SIDEBAR */}

        <div className="w-64 bg-black/30 border-r border-cyan-500/20 p-5 backdrop-blur-xl">

          <h1 className="text-3xl font-bold text-cyan-400 mb-2">

            JARVIS

          </h1>

          <p className="text-cyan-300/60 text-sm">

            Autonomous AI Assistant

          </p>

          <div className="mt-10">

            <div className="text-cyan-400 mb-3">
              STATUS
            </div>

            <div className="bg-cyan-500/10 border border-cyan-500/20 rounded-xl p-4">

              <div className="text-2xl font-bold">

                {status}

              </div>

            </div>

          </div>

          <div className="mt-10">

            <div className="text-cyan-400 mb-3">
              CLOCK
            </div>

            <div className="bg-cyan-500/10 border border-cyan-500/20 rounded-xl p-4">

              <div className="text-3xl font-mono text-cyan-300">

                {time}

              </div>

            </div>

          </div>

        </div>

        {/* CENTER */}

        <div className="flex-1 flex flex-col items-center justify-center px-10">

          {/* TITLE */}

          <motion.h1

            initial={{
              opacity: 0,
              y: -30
            }}

            animate={{
              opacity: 1,
              y: 0
            }}

            className="text-6xl font-black bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-4"
          >

            JARVIS AI SYSTEM

          </motion.h1>

          <p className="text-cyan-300/60 mb-16">

            Autonomous Intelligence Core

          </p>

          {/* ORB */}

          <motion.div

            animate={{

              scale:
                listening
                  ? [1, 1.1, 1]
                  : 1,

              boxShadow:
                listening
                  ? [
                      "0 0 40px cyan",
                      "0 0 80px cyan",
                      "0 0 40px cyan"
                    ]
                  : "0 0 40px rgba(0,255,255,0.4)"
            }}

            transition={{
              repeat: Infinity,
              duration: 1.5
            }}

            className="w-64 h-64 rounded-full bg-cyan-500/10 border border-cyan-400/40 flex items-center justify-center mb-14 backdrop-blur-xl"
          >

            <Mic className="w-20 h-20 text-cyan-300" />

          </motion.div>

          {/* BUTTONS */}

          <div className="flex gap-5 mb-10">

            <button

              onClick={startVoice}

              className="w-16 h-16 rounded-full bg-cyan-500 hover:scale-110 transition flex items-center justify-center"
            >

              <Mic />

            </button>

            <button

              className="w-16 h-16 rounded-full bg-pink-500 hover:scale-110 transition flex items-center justify-center"
            >

              <Volume2 />

            </button>

            <button

              className="w-16 h-16 rounded-full bg-green-500 hover:scale-110 transition flex items-center justify-center"
            >

              <Zap />

            </button>

          </div>

          {/* INPUT */}

          <form

            onSubmit={handleSubmit}

            className="w-full max-w-5xl flex gap-4"
          >

            <input

              type="text"

              value={input}

              onChange={(e) =>
                setInput(e.target.value)
              }

              placeholder="Enter command..."

              className="flex-1 bg-black/40 border border-cyan-500/20 rounded-2xl px-6 py-5 text-lg outline-none"
            />

            <button

              type="submit"

              className="px-8 rounded-2xl bg-cyan-500 hover:bg-cyan-400 transition font-bold"
            >

              <Send />

            </button>

          </form>

          {/* RESPONSE */}

          {response && (

            <div className="mt-8 w-full max-w-5xl bg-purple-500/10 border border-purple-500/20 rounded-2xl p-5 overflow-auto max-h-72">

              <div className="text-purple-300 text-sm mb-2">

                RESPONSE

              </div>

              <pre className="whitespace-pre-wrap text-white text-sm">

                {response}

              </pre>

            </div>
          )}

        </div>

        {/* RIGHT PANEL */}

        <div className="w-96 bg-black/30 border-l border-cyan-500/20 p-5 overflow-y-auto backdrop-blur-xl">

          <div className="text-cyan-400 text-xl mb-5">

            EXECUTION LOGS

          </div>

          <div className="space-y-4">

            {logs.map((log, index) => (

              <div

                key={index}

                className={`p-4 rounded-xl border ${
                  log.type === "error"
                    ? "bg-red-500/10 border-red-500/20"
                    : log.type === "success"
                    ? "bg-green-500/10 border-green-500/20"
                    : "bg-cyan-500/10 border-cyan-500/20"
                }`}
              >

                <div className="font-bold">

                  {log.title}

                </div>

                <pre className="text-xs opacity-80 mt-2 whitespace-pre-wrap">

                  {log.detail}

                </pre>

                <div className="text-xs opacity-50 mt-2">

                  {log.time}

                </div>

              </div>
            ))}

          </div>

        </div>

      </div>

    </div>
  );
}