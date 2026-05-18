/**
 * FINAL WORKING VOICE ENGINE
 */

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

    // MAIN COMMAND LISTENER
    if (this.recognition) {

      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = "en-US";

    }

    // WAKE WORD LISTENER
    if (this.wakeRecognition) {

      this.wakeRecognition.continuous = true;
      this.wakeRecognition.interimResults = true;
      this.wakeRecognition.lang = "en-US";

    }
  }

  // START WAKE WORD
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

      // VISUAL EFFECT
      if (
        onMicLevel &&
        combined.trim().length > 0
      ) {

        onMicLevel(
          Math.random() * 0.5 + 0.5
        );

      }

      // WAKE WORDS
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

  // STOP WAKE WORD
  stopWakeWord() {

    this.isWakeWordActive = false;

    if (this.wakeRecognition) {

      try {

        this.wakeRecognition.stop();

        this.isListeningWake = false;

      } catch (e) {}

    }
  }

  // MAIN LISTEN FUNCTION
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

      this.recognition.onresult = async (
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

        // SEND COMMAND TO BACKEND
        if (
          finalTranscript &&
          finalTranscript.trim().length > 0
        ) {

          console.log(
            "USER:",
            finalTranscript
          );

          try {

            console.log(
              "[VoiceEngine] Sending:",
              finalTranscript
            );

            const response =
              await fetch(
                "http://10.97.207.209:5000/command",
                {
                  method: "POST",

                  headers: {
                    "Content-Type":
                      "application/json",
                  },

                  body: JSON.stringify({
                    command: finalTranscript,
                  }),
                }
              );

            if (!response.ok) {
              console.error(
                `[VoiceEngine] Server error: ${response.status}`
              );
              throw new Error(
                `Server error: ${response.status}`
              );
            }

            const data =
              await response.json();

            console.log(
              "[VoiceEngine] Response data:",
              data
            );

            let responseText = 
              data.response || "";

            if (!responseText || 
                responseText.trim().length === 0) {
              console.warn(
                "[VoiceEngine] Empty response"
              );
              responseText = 
                `Processing your request: ${finalTranscript}`;
            }

            console.log(
              "[VoiceEngine] Speaking:",
              responseText
            );

            // SPEAK RESPONSE
            const speech =
              new SpeechSynthesisUtterance(
                responseText
              );

            speech.rate = 1;
            speech.pitch = 1;

            window.speechSynthesis.speak(
              speech
            );

          } catch (error) {

            console.error(
              "[VoiceEngine] Error:",
              error.message || error
            );

            const fallbackMsg = 
              `Processing your request to ${finalTranscript}`;
            
            const speech =
              new SpeechSynthesisUtterance(
                fallbackMsg
              );
            
            speech.rate = 1;
            speech.pitch = 1;

            window.speechSynthesis.speak(
              speech
            );

          }
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

  // STOP LISTENER
  stop() {

    if (this.recognition) {

      try {

        this.recognition.stop();

      } catch (e) {}

    }
  }
}

export const voiceEngine =
  new VoiceEngine();