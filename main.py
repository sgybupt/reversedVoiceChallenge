import pyaudio
import keyboard

import time
import keyboard

print("""
Make Sure you are running this code with sudo in Mac. Privilege is needed, 
Due to the audio input.
""")

FORMAT = pyaudio.paInt16  # 2 Bytes
CHANNELS = 1
RATE = 44100
CHUNK = 1024
audio = pyaudio.PyAudio()

origin_data_b = b''
record_frames = []
reversed_data_b = b''

print("----------------------record device list---------------------")
input_device = 0
info = audio.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')
for i in range(0, num_devices):
    if int(audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0 \
            and "麦克风" in audio.get_device_info_by_host_api_device_index(0, i).get('name'):
        input_device = i
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

print("-------------------------------------------------------------")

output_device = 0
for i in range(0, num_devices):
    if int(audio.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0 \
            and "扬声器" in audio.get_device_info_by_host_api_device_index(0, i).get('name'):
        output_device = i
        print("Output Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))


def record_audio():
    global origin_data_b
    global record_frames
    global reversed_data_b
    print("-" * 80)
    print("recording started")
    print("if you want to stop, press q.")
    record_frames = []
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=input_device,
                        frames_per_buffer=CHUNK)
    while True:
        # for i in range(0, int(RATE // CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        record_frames.append(data)
        if keyboard.is_pressed('q'):
            print("q is pressed")
            break
    origin_data_b = b''.join(record_frames)
    stream.stop_stream()
    stream.close()
    print("recording stopped")

    record_frames_reversed = []
    for each in record_frames:
        each = bytearray(each)
        tmp = []
        for i, b in enumerate(each):
            if (i + 1) % 2 == 0:
                tmp.append(each[i - 1:i + 1])
        record_frames_reversed.append(b''.join(tmp[::-1]))
    reversed_data_b = b''.join(record_frames_reversed[::-1])
    print("audio has been reversed")


def play_reversed_audio():
    """
    开始播放声音
    """
    global reversed_data_b
    print("-" * 80)
    print("playing audios")
    stream = audio.open(format=audio.get_format_from_width(2),
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        output_device_index=output_device)

    stream.write(reversed_data_b)
    stream.close()


def play_origin_audio():
    """
    开始播放声音
    """
    global reversed_data_b
    print("-" * 80)
    print("playing audios")
    stream = audio.open(format=audio.get_format_from_width(2),
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        output_device_index=output_device)

    stream.write(origin_data_b)
    stream.close()


print("""
press 'a' to start recording, reversed recording will be played immediately.
press 'q' to stop recording
press 'o' to play origin recording
press 'r' to replay reversed recording
press 'esc' to EXIT
""")

while True:
    time.sleep(0.01)
    if keyboard.is_pressed("a"):
        record_audio()
    if keyboard.is_pressed("r"):
        play_reversed_audio()
    if keyboard.is_pressed("o"):
        play_origin_audio()
    if keyboard.is_pressed("esc"):
        break
audio.terminate()
