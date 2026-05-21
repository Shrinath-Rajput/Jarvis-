import { getBackendExecutor } from './BackendExecutor.js';

export class VoiceEngine {

  constructor() {

    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    this.recognition = SpeechRecognition
      ? new SpeechRecognition()
      : null;

    this.wakeRecognition = SpeechRecognition
      ? new SpeechRecognition()
      : null;

    // ✅ ROBUST STATE TRACKING
    this.isWakeWordActive = false;
    this.isListeningWake = false;
    this.isListening = false;
    this.recognitionStarting = false;
    this.wakeRecognitionStarting = false;

    if (this.recognition) {
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = "en-US";
      
      // ✅ PREVENT DOUBLE-START ON BOOT
      this.recognition.onstart = () => {
        console.log("🎤 Main recognition started");
        this.recognitionStarting = false;
      };
    }

    if (this.wakeRecognition) {
      this.wakeRecognition.continuous = true;
      this.wakeRecognition.interimResults = true;
      this.wakeRecognition.lang = "en-US";
      
      // ✅ PREVENT DOUBLE-START ON BOOT
      this.wakeRecognition.onstart = () => {
        console.log("👂 Wake recognition started");
        this.wakeRecognitionStarting = false;
      };
    }
  }

  startWakeWord(onWakeDetected, onMicLevel) {

    if (!this.wakeRecognition) return;

    this.isWakeWordActive = true;

    this.wakeRecognition.onresult = (event) => {

      let combined = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        ++i
      ) {
        combined +=
          event.results[i][0].transcript.toLowerCase();
      }

      if (
        onMicLevel &&
        combined.trim().length > 0
      ) {
        onMicLevel(
          Math.random() * 0.5 + 0.5
        );
      }

      if (
        combined.includes("jarvis") ||
        combined.includes("premex") ||
        combined.includes("boss") ||
        combined.includes("hey jarvis")
      ) {

        console.log("🎯 WAKE WORD DETECTED");

        this.stopWakeWord();

        onWakeDetected();
      }
    };

    this.wakeRecognition.onerror = (event) => {

      console.error(
        "👂 Wake Error:",
        event.error
      );

      // ✅ RESET STATE ON ERROR
      this.wakeRecognitionStarting = false;

      if (event.error === 'not-allowed') {
        console.warn("Microphone access denied");
        this.stopWakeWord();
      }
      
      // ✅ AUTO-RESTART ON NETWORK ERROR
      if (event.error === 'network' && this.isWakeWordActive) {
        console.log("Retrying wake detection in 2s...");
        setTimeout(() => this.startWakeWord(onWakeDetected, onMicLevel), 2000);
      }
    };

    this.wakeRecognition.onend = () => {

      this.isListeningWake = false;

      if (this.isWakeWordActive) {

        setTimeout(() => {

          try {

            // ✅ CHECK BOTH FLAGS BEFORE STARTING
            if (!this.isListeningWake && !this.wakeRecognitionStarting) {

              this.wakeRecognitionStarting = true;
              this.wakeRecognition.start();
              this.isListeningWake = true;
            }

          } catch (e) {
            console.error("Failed to restart wake detection:", e.message);
            this.wakeRecognitionStarting = false;
          }

        }, 1000);
      }
    };

    try {

      // ✅ CHECK BOTH FLAGS TO PREVENT DOUBLE-START
      if (!this.isListeningWake && !this.wakeRecognitionStarting) {

        this.wakeRecognitionStarting = true;
        this.wakeRecognition.start();
        this.isListeningWake = true;
        console.log("👂 Wake word detection started");
      }

    } catch (e) {

      console.error(
        "Wake word error:",
        e.message
      );
      this.wakeRecognitionStarting = false;
    }
  }

  stopWakeWord() {

    this.isWakeWordActive = false;

    if (this.wakeRecognition) {

      try {

        this.wakeRecognition.stop();

        this.isListeningWake = false;

      } catch (e) {}
    }
  }

  // ✅ ONLY RETURN TRANSCRIPT
  // ❌ NO BACKEND EXECUTION HERE

  listen(onInterim) {

    return new Promise((resolve, reject) => {

      if (!this.recognition) {

        reject(
          "Speech Recognition not supported"
        );

        return;
      }

      this.stopWakeWord();

      let finalTranscript = "";

      this.recognition.onresult = (
        event
      ) => {

        let interim = "";

        for (
          let i = event.resultIndex;
          i < event.results.length;
          ++i
        ) {

          if (event.results[i].isFinal) {

            finalTranscript +=
              event.results[i][0].transcript;

          } else {

            interim +=
              event.results[i][0].transcript;
          }
        }

        if (onInterim) {

          onInterim(
            interim || finalTranscript
          );
        }
      };

      this.recognition.onerror = (
        event
      ) => {

        console.error(
          "🎤 Voice Error:",
          event.error
        );

        this.isListening = false;
        this.recognitionStarting = false;
        
        // ✅ BETTER ERROR MESSAGES
        if (event.error === 'no-speech') {
          reject("No speech detected. Please try again.");
        } else if (event.error === 'not-allowed') {
          reject("Microphone access denied.");
        } else if (event.error === 'network') {
          reject("Network error. Check your connection.");
        } else {
          reject(event.error);
        }
      };

      this.recognition.onend = () => {

        this.isListening = false;
        this.recognitionStarting = false;
        
        console.log("🎤 Recognition ended, transcript:", finalTranscript);
        resolve(finalTranscript);
      };

      try {

        // ✅ STOP FIRST IF ALREADY RUNNING
        if (this.isListening || this.recognitionStarting) {
          try {
            this.recognition.stop();
            this.isListening = false;
            this.recognitionStarting = false;
          } catch (e) {
            console.warn("Could not stop recognition:", e.message);
          }
        }

        // ✅ ADD SMALL DELAY BEFORE RESTARTING
        setTimeout(() => {
          try {
            this.recognitionStarting = true;
            this.isListening = true;
            this.recognition.start();
            console.log("🎤 Listening...");
          } catch (e) {
            this.isListening = false;
            this.recognitionStarting = false;
            console.error("Failed to start recognition:", e.message);
            reject(e);
          }
        }, 100);

      } catch (e) {

        this.isListening = false;
        this.recognitionStarting = false;
        reject(e);
      }
    });
  }

  stop() {

    this.isListening = false;

    if (this.recognition) {

      try {

        this.recognition.stop();

      } catch (e) {}
    }
  }

  // ===== NEW METHODS FOR PREMIUM UI =====

  /**
   * Start listening for voice input
   * @param {Function} onResult - Callback when speech ends
   * @param {Function} onError - Error callback
   * @returns {Promise<string>} Final transcript
   */
  startListening(onResult, onError) {
    return this.listen((transcript) => {
      if (onResult) onResult(transcript);
    }).then((finalTranscript) => {
      if (onResult) onResult(finalTranscript);
      return finalTranscript;
    }).catch((error) => {
      if (onError) onError(error);
      throw error;
    });
  }

  /**
   * Stop listening for voice input
   */
  stopListening() {
    this.stop();
  }

  /**
   * Speak text using text-to-speech
   * @param {string} text - Text to speak
   * @returns {Promise<void>}
   */
  speak(text) {
    return new Promise((resolve, reject) => {
      if (!window.speechSynthesis) {
        reject("Speech Synthesis not supported");
        return;
      }

      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      utterance.onstart = () => {
        console.log("Speech started");
      };

      utterance.onend = () => {
        console.log("Speech ended");
        resolve();
      };

      utterance.onerror = (error) => {
        console.error("Speech error:", error);
        reject(error);
      };

      try {
        window.speechSynthesis.speak(utterance);
      } catch (error) {
        reject(error);
      }
    });
  }
}

export const voiceEngine =
  new VoiceEngine();

export default voiceEngine;