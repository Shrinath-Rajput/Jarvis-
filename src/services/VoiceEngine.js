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

    this.isWakeWordActive = false;
    this.isListeningWake = false;

    if (this.recognition) {
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = "en-US";
    }

    if (this.wakeRecognition) {
      this.wakeRecognition.continuous = true;
      this.wakeRecognition.interimResults = true;
      this.wakeRecognition.lang = "en-US";
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

        console.log("WAKE WORD DETECTED");

        this.stopWakeWord();

        onWakeDetected();
      }
    };

    this.wakeRecognition.onerror = (event) => {

      console.log(
        "Wake Error:",
        event.error
      );

      if (event.error === 'not-allowed') {
        this.stopWakeWord();
      }
    };

    this.wakeRecognition.onend = () => {

      this.isListeningWake = false;

      if (this.isWakeWordActive) {

        setTimeout(() => {

          try {

            if (!this.isListeningWake) {

              this.wakeRecognition.start();

              this.isListeningWake = true;
            }

          } catch (e) {}

        }, 1000);
      }
    };

    try {

      if (!this.isListeningWake) {

        this.wakeRecognition.start();

        this.isListeningWake = true;
      }

    } catch (e) {

      console.log(
        "Wake already running"
      );
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
          "Voice Error:",
          event.error
        );

        reject(event.error);
      };

      this.recognition.onend = () => {

        resolve(finalTranscript);
      };

      try {

        this.recognition.start();

      } catch (e) {

        reject(e);
      }
    });
  }

  stop() {

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