import socket
import pyaudio
import threading


FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 8192

sound = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    global soc1
    global data
    soc1.sendall(in_data)
    return (None, pyaudio.paContinue)

istream = sound.open(rate=RATE, channels=1, format=FORMAT, input=True,
                 frames_per_buffer=CHUNK, start=False, stream_callback=callback)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc1:
        print('클라이언트 시작')
        host = '172.30.1.34'
        soc.connect((host, 8080))
        soc1.connect((host, 8080))
        istream.start_stream()
        data = []

        while True:
            data.append(soc.recv(CHUNK))
            pass
        istream.stop_stream()
