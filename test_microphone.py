import sys

import pyaudiowpatch as pyaudio

sys.modules["pyaudio"] = pyaudio

import speech_recognition as sr


recognizer = sr.Recognizer()

microphones = sr.Microphone.list_microphone_names()

print("Available microphones:")

for index, name in enumerate(microphones):
    print(index, ":", name)


mic_index = None

for index, name in enumerate(microphones):
    if "Microphone (Realtek High Definition Audio)" in name:
        mic_index = index
        break


print()
print("Selected microphone:", mic_index)

if mic_index is None:
    print("ERROR: Realtek microphone was not found.")
    input("Press Enter to exit...")
    raise SystemExit


try:

    with sr.Microphone(device_index=mic_index) as source:

        print()
        print("Lily is listening...")
        print("Say: Hello Lily")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10
        )

    print()
    print("Audio captured!")
    print("Lily is sending the audio for recognition...")

    text = recognizer.recognize_google(audio)

    print()
    print("Lily heard:", text)

except Exception as e:

    print()
    print("ERROR TYPE:", type(e).__name__)
    print("ERROR:", repr(e))


input()