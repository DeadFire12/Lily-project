import pyaudiowpatch as pyaudio
import audioop
import time

p = pyaudio.PyAudio()

print("INPUT DEVICES")
print("=============")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)

    if info["maxInputChannels"] > 0:
        print()
        print("INDEX:", i)
        print("NAME:", info["name"])
        print("CHANNELS:", info["maxInputChannels"])
        print("SAMPLE RATE:", info["defaultSampleRate"])
        print("HOST API:", info["hostApi"])

print()
print("================================")
print("TESTING MICROPHONE INDEX 9")
print("================================")

mic_index = 9

info = p.get_device_info_by_index(mic_index)

print("Name:", info["name"])
print("Channels:", info["maxInputChannels"])
print("Sample rate:", info["defaultSampleRate"])
print()

try:

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=int(info["defaultSampleRate"]),
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=1024
    )

    print("Speak loudly for 5 seconds.")
    print("Say: HELLO LILY")
    print()

    start = time.time()
    highest = 0

    while time.time() - start < 5:

        data = stream.read(
            1024,
            exception_on_overflow=False
        )

        level = audioop.rms(data, 2)

        if level > highest:
            highest = level

    stream.stop_stream()
    stream.close()

    print()
    print("HIGHEST SOUND LEVEL:", highest)

    if highest == 0:
        print("RESULT: ZERO AUDIO")
    elif highest < 500:
        print("RESULT: VERY QUIET")
    else:
        print("RESULT: AUDIO DETECTED")

except Exception as e:

    print()
    print("ERROR:", type(e).__name__)
    print("DETAIL:", repr(e))

p.terminate()

print()
print("TEST FINISHED")

input("Press Enter to exit...")