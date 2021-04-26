import socket
import pyaudio
import threading


FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 8192

sound = pyaudio.PyAudio()

def speaker_thread():
    global data, ostream
    while True:
           if data:
            ostream.write(data[0])
            del data[0]

ostream = sound.open(rate=RATE, channels=1, format=FORMAT, output=True, frames_per_buffer=CHUNK, start=False)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    host ='172.30.1.34' #서버ip
    soc.bind((host, 8080))
    soc.listen(1)
    conn, addr= soc.accept()
    conn1, addr1 = soc.accept()
    ostream.start_stream()
    data = []
    th = threading.Thread(target=speaker_thread) #스피커쓰레드 시작점
    th.start()

    while True:
        data.append(conn1.recv(CHUNK))
    ostream.stop_stream()