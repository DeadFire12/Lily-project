import pyttsx3


try:

    import pyaudiowpatch as pyaudio

    import sys

    sys.modules["pyaudio"] = pyaudio

    import speech_recognition as sr

    AUDIO_AVAILABLE = True

except Exception:

    AUDIO_AVAILABLE = False


_engine = None


def get_engine():

    global _engine

    if _engine is None:

        _engine = pyttsx3.init()

        _engine.setProperty(
            "rate",
            175
        )

        _engine.setProperty(
            "volume",
            1.0
        )

    return _engine


def speak(text):

    try:

        engine = get_engine()

        engine.say(text)

        engine.runAndWait()

        return True

    except Exception as e:

        print(
            "Voice output error:",
            e
        )

        return False


def listen():
    if not AUDIO_AVAILABLE:
        return None

    recognizer = sr.Recognizer()

    try:
        microphones = sr.Microphone.list_microphone_names()

        mic_index = None

        # Use the second Realtek microphone endpoint.
        # The first one (index 5) was returning silence.
        # The second one (index 9) receives the real microphone audio.
        for index, name in enumerate(microphones):
            if index == 9 and "Microphone (Realtek High Definition Audio)" in name:
                mic_index = index
                break

        if mic_index is None:
            print("Voice input error: Realtek microphone endpoint 9 not found.")
            return None

        with sr.Microphone(
            device_index=mic_index,
            sample_rate=44100,
            chunk_size=1024
        ) as source:

            print("Lily is listening...")
            print("Speak now! 🎙️")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            recognizer.pause_threshold = 1.0
            recognizer.non_speaking_duration = 0.5

            print("I'm ready — go ahead! 🎤")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        print("Lily is thinking...")

        text = recognizer.recognize_google(audio)

        return text

    except sr.WaitTimeoutError:
        print("Voice input error: You didn't start speaking in time.")
        return None

    except sr.UnknownValueError:
        print("Voice input error: I heard audio, but couldn't understand the words.")
        return None

    except sr.RequestError as e:
        print("Voice input error: Google speech service problem:", e)
        return None

    except Exception as e:
        print("Voice input error:", type(e).__name__, repr(e))
        return None