import cv2
import os
import wave
import pyaudio

serious = 0
chunk = 1024
p = pyaudio.PyAudio()

def soundopen(path):
    with wave.open(path, 'rb') as f:
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
            channels = f.getnchannels(),
            rate = f.getframerate(),
            output = True)

        data = f.readframes(chunk)
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
    return

def size(seridisease):
    if seridisease == 1:
        soundopen('zobssalsize.wav')
    elif seridisease == 2:
        soundopen('beansize.wav')
    elif seridisease == 3:
        soundopen('500size.wav')
    else:
        soundopen('ggulsize.wav')
    return

def detectAndDisplay(frame):
    #connect to haarcascade xml file
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    print(cv2_base_dir)
    face_cascade_path = os.path.join(cv2_base_dir, 'data\haarcascade_frontalface_alt.xml')
    # ill1_cascade_path = os.path.join(cv2_base_dir,'data\gunsun.xml') #건선
    ill1_cascade_path = os.path.join(cv2_base_dir, 'data\gumbeoseot.xml')  # 검버섯
    ill2_cascade_path = os.path.join(cv2_base_dir, 'data\littlepimple.xml')  # 좁쌀 여드름
    ill3_cascade_path = os.path.join(cv2_base_dir, 'data\paekban.xml') #백반증
    ill4_cascade_path = os.path.join(cv2_base_dir, 'data\paekban.xml')
    ill5_cascade_path = os.path.join(cv2_base_dir, 'data\paekban.xml')
    ill6_cascade_path = os.path.join(cv2_base_dir, 'data\pimple.xml')

    # haarcascade
    face_cascade = cv2.CascadeClassifier()
    ill1_cascade = cv2.CascadeClassifier()
    ill2_cascade = cv2.CascadeClassifier()
    ill3_cascade = cv2.CascadeClassifier()
    ill4_cascade = cv2.CascadeClassifier()
    ill5_cascade = cv2.CascadeClassifier()
    ill6_cascade = cv2.CascadeClassifier()

    #xml file load
    if not face_cascade.load(cv2.samples.findFile(face_cascade_path)):
        print('no such file')
    if not ill1_cascade.load(cv2.samples.findFile(ill1_cascade_path)):
        print('no such file')
    if not ill2_cascade.load(cv2.samples.findFile(ill2_cascade_path)):
        print('no such file')
    if not ill3_cascade.load(cv2.samples.findFile(ill3_cascade_path)):
        print('no such file')
    if not ill4_cascade.load(cv2.samples.findFile(ill4_cascade_path)):
        print('no such file')
    if not ill5_cascade.load(cv2.samples.findFile(ill5_cascade_path)):
        print('no such file')
    if not ill6_cascade.load(cv2.samples.findFile(ill6_cascade_path)):
        print('no such file')
        exit(0)

    #face detection
    faces = face_cascade.detectMultiScale((frame))
    x_list = [] #좌표값
    y_list = []

    cnt1 = 0 #gumbeoseot count
    cnt2 = 0 #pimple count
    cnt3 = 0 #baekban count
    cnt4 = 0
    cnt5 = 0
    cnt6 = 0

    label1 = 'gumbeoseot'
    label2 = 'littlepimple'
    label3 = 'paekban'
    label4 = 'daesang'
    label5 = 'hongban'
    label6 = 'pimple'

    global veryserious
    global serious1
    global serious2
    global serious3
    global serious4
    global serious5
    global serious6

    for (x, y, w, h) in faces:
        center = (x+w//2, y+h//2)
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 4)
        faceROI = frame[y:y+h, x: x+w]

        #gray = cv2.cvtColor(faceROI, cv2.COLOR_BGR2GRAY) #gray scale
        #ill1 = ill1_cascade.detectMultiScale(gray, 1.3, 5)
        ill1 = ill1_cascade.detectMultiScale((faceROI))
        ill2 = ill2_cascade.detectMultiScale((faceROI))
        ill3 = ill3_cascade.detectMultiScale((faceROI))
        ill4 = ill1_cascade.detectMultiScale((faceROI))
        ill5 = ill2_cascade.detectMultiScale((faceROI))
        ill6 = ill3_cascade.detectMultiScale((faceROI))

        #gumbeoseot
        for (x3, y3, w3, h3) in ill1:
            cnt1+=1 #counting

            ill1_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill1_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill1_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            if radius > 0 and radius < 10:
                serious1 = 1
            elif radius >= 10 and radius < 30:
                serious1 = 2
            elif radius >=30 and radius <50:
                serious1 = 3
                veryserious = 1
            else:
                serious1 = 4
                veryserious = 1
            text = (x + x3 + w3 // 2 + radius, y + y3 + h3 // 2 + radius) #text 위치

            frame = cv2.circle(frame, ill1_center, radius, (255,0,0), 1) #draw circle
            frame = cv2.putText(frame, label1+str(cnt1), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0)) #labelling

        #little pimple
        for (x3, y3, w3, h3) in ill2:
            cnt2+=1 #counting

            ill2_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill2_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill2_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            print(radius)
            if radius > 0 and radius < 10:
                serious2 = 1
            elif radius >= 10 and radius < 30:
                serious2 = 2
            elif radius >= 30 and radius < 50:
                serious2 = 3
                veryserious = 1
            else:
                serious2 = 4
                veryserious = 1
            text = (x+x3+w3//2+radius, y+y3+h3//2+radius) #text 위치

            frame = cv2.circle(frame, ill2_center, radius, (0,0,255), 1) #draw circle
            frame = cv2.putText(frame, label2+str(cnt2), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255)) #labelling

        for (x3, y3, w3, h3) in ill3:
            cnt3+=1 #counting

            ill3_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill3_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill3_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            print(radius)
            if radius > 0 and radius < 10:
                serious3 = 1
            elif radius >= 10 and radius < 30:
                serious3 = 2
            elif radius >= 30 and radius < 50:
                serious3 = 3
                veryserious = 1
            else:
                serious3 = 4
                veryserious = 1
            text = (x+x3+w3//2+radius, y+y3+h3//2+radius) #text 위치

            frame = cv2.circle(frame, ill3_center, radius, (0,0,255), 1) #draw circle
            frame = cv2.putText(frame, label3+str(cnt3), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255)) #labelling

        for (x3, y3, w3, h3) in ill4:
            cnt4+=1 #counting

            ill1_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill4_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill4_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            if radius > 0 and radius < 10:
                serious4 = 1
            elif radius >= 10 and radius < 30:
                serious4 = 2
            elif radius >=30 and radius <50:
                serious4 = 3
                veryserious = 1
            else:
                serious4 = 4
                veryserious = 1
            text = (x + x3 + w3 // 2 + radius, y + y3 + h3 // 2 + radius) #text 위치

            frame = cv2.circle(frame, ill4_center, radius, (255,0,0), 1) #draw circle
            frame = cv2.putText(frame, label4+str(cnt4), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0)) #labelling

        for (x3, y3, w3, h3) in ill5:
            cnt5+=1 #counting

            ill1_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill5_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill5_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            if radius > 0 and radius < 10:
                serious5 = 1
            elif radius >= 10 and radius < 30:
                serious5 = 2
            elif radius >=30 and radius <50:
                serious5 = 3
                veryserious = 1
            else:
                serious5 = 4
                veryserious = 1
            text = (x + x3 + w3 // 2 + radius, y + y3 + h3 // 2 + radius) #text 위치

            frame = cv2.circle(frame, ill5_center, radius, (255,0,0), 1) #draw circle
            frame = cv2.putText(frame, label5+str(cnt5), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0)) #labelling

        for (x3, y3, w3, h3) in ill6:
            cnt6+=1 #counting

            ill1_center = (x+x3+w3//2, y+y3+h3//2)
            x_list.append(ill6_center[0]) #좌표값 받아서 list로 저장
            y_list.append(ill6_center[1])

            radius = int(round((w3+h3)*0.15)) #labelling 원 반지름
            if radius > 0 and radius < 10:
                serious6 = 1
            elif radius >= 10 and radius < 30:
                serious6 = 2
            elif radius >=30 and radius <50:
                serious6 = 3
                veryserious = 1
            else:
                serious6 = 4
                veryserious = 1
            text = (x + x3 + w3 // 2 + radius, y + y3 + h3 // 2 + radius) #text 위치

            frame = cv2.circle(frame, ill6_center, radius, (255,0,0), 1) #draw circle
            frame = cv2.putText(frame, label6+str(cnt6), text, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0)) #labelling

    cnt = [cnt1, cnt2, cnt3, cnt4, cnt5, cnt6]  # counting list
    label = [label1, label2, label3, label4, label5, label6]  # label list
    serious = [serious1, serious2, serious3, serious4, serious5, serious6] #serious list

    soundopen('detect.wav')
    return x_list, y_list, cnt, label, serious, frame, veryserious


#camera capture
def camera():
    cap = cv2.VideoCapture(0) #0 or -1
    if cap.isOpened():
        ret, img = cap.read()
        soundopen('take.wav')
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if ret:
            #cv2.imshow('camera-0', img)
            cv2.imwrite('face.jpg', img)
            #cv2.waitKey(0)
        else:
            print('no camera!')

    cap.release()
    cv2.destroyAllWindows()

    return img
