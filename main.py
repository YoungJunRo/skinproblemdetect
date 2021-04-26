import time
import RPi.GPIO as GPIO
import wiringpi  # for dcmotor
import numpy
import sys
import detect.py
import math

import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
from uuid import uuid4

from twilio.rest import Client

global veryserious

#음성 관련 함수 정의

def fileUpload(file):
  cred = credentials.Certificate("project2-f2bf8-firebase-adminsdk-5m4z5-3ff18a224f.json")
  firebase_admin.initialize_app(cred, {
    # 'gs://project2-f2bf8.appspot.com/'
    'databaseURL': 'https://project2-f2bf8-default-rtdb.firebaseio.com/',
    'storageBucket': f'project2-f2bf8.appspot.com'
  })

  bucket = storage.bucket()
  firebase = db.reference()

  blob = bucket.blob('captureImages/' + file)
  new_token = uuid4()
  metadata = {'firebaseStorageDownloadTokens': new_token}
  blob.metadata = metadata

  blob.upload_from_filename(filename=file, content_type='image/jpeg')
  blob.make_public()

  firebase.update({'serious': veryserious})


def send():
  client = Client("AC347068dc563ce3cdeece8cafa2e63450", "d77c402a6320107b888c3d1093bb6578")
  client.messages.create(to="+82 10-7254-1582", from_="+16788317294", body="Check your patient!")

#하드웨어 제어 관련 함수 정의

def servoMotorCamera(pin, stat):  # 카메라 서보모터 함수

  t = 1 # t값으로 로봇팔 움직임 속도 조절가능

  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)
  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  #time.sleep(t)

  if stat == 0:  # 카메라 내려감
    pwm.ChangeDutyCycle(2.45)
    time.sleep(t)

  else:  # 카메라 올라감
    pwm.ChangeDutyCycle(5)
    time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor1(pin, degree):  # servomotor1 움직임 알고리즘
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 7.4

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(base, degree, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(base, degree, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor2(pin, degree): # servomotor2 움직임 알고리즘
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 6.9

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(base, degree, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(base, degree, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor3(pin, degree):  # servomotor3 움직임 알고리즘
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 5.25

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(base, degree, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(base, degree, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor4(pin, degree):  # servomotor4 움직임 알고리즘
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 4.5

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(base, degree, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(base, degree, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor1_init(pin, degree):  # 기본위치로 이동 시 serovomotor1 움직임
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 7.4

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(degree, base, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(degree, base, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor2_init(pin, degree):  # 기본위치로 이동 시 serovomotor2 움직임
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 6.9

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(degree, base, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(degree, base, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor3_init(pin, degree):  # 기본위치로 이동 시 serovomotor3 움직임
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 5.25

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(degree, base, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(degree, base, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor4_init(pin, degree):  # 기본위치로 이동 시 serovomotor4 움직임
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)

  #t = 0.015
  t = 0.05
  base = 4.5

  pwm = GPIO.PWM(pin, 50)

  pwm.start(0)
  # time.sleep(t)

  if degree >= base:
    for i in numpy.arange(degree, base, -0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)
  else:
    for i in numpy.arange(degree, base, 0.1):
      pwm.ChangeDutyCycle(i)
      time.sleep(t)

  pwm.stop()
  #GPIO.cleanup()


def servoMotor_move(pin1, pin2, pin3, pin4, degree_x, degree_y):  # 기본위치에서 detection 좌표로 움직이기

  servoMotor4(pin4, degree_y)
  time.sleep(1)
  servoMotor3(pin3, degree_y)
  time.sleep(1)
  servoMotor2(pin2, degree_x)
  time.sleep(1)
  servoMotor1(pin1, 12.6-degree_x)
  time.sleep(1)


def servoMoto_init(pin1, pin2, pin3, pin4, degree_x, degree_yr):  # detection 좌표에서 기본위치로 움직이기

  servoMotor1_init(pin1, 12.6-degree_x)
  time.sleep(1)
  servoMotor2_init(pin2, degree_x)
  time.sleep(1)
  servoMotor3_init(pin3, degree_y)
  time.sleep(1)
  servoMotor4_init(pin4, degree_y)
  time.sleep(1)


def servoMotor_on(pin3, pin4):  # start할때 off 위치에서 기본위치로
  servoMotor4_init(pin4, 2.3)
  time.sleep(1)
  servoMotor3_init(pin3, 3.0)
  time.sleep(1)


def servoMotor_off(pin3, pin4):  # 끌때 기본위치에서 off위치로
  servoMotor3(pin3, 3)
  time.sleep(1)
  servoMotor4(pin4, 2.3)
  time.sleep(1)


def servoMotor_break():    #긴급 stop 알고리즘 
  def servoMotor(pin, degree, t):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)
    pwm.start(0)
    #time.sleep(t)
    pwm.ChangeDutyCycle(degree)
    time.sleep(t)

    pwm.stop()
  pin1, pin2, pin3, pin4 = 11, 12, 13, 16 # 서보모터1~4
  t = 0.05
  servoMotor(11, 7.6, 1)
  time.sleep(t)
  servoMotor(12, 6.9, 1)
  time.sleep(t)
  servoMotor(13, 5.25, 1)
  time.sleep(t)
  servoMotor(16, 4.5, 1)


def dcMotor(dcspeed, dcstat):  #지시봉 전/후진 dc모터 알고리즘

  def setPinConfig(EN, INA, INB):
      wiringpi.pinMode(EN, OUTPUT)
      wiringpi.pinMode(INA, OUTPUT)
      wiringpi.pinMode(INB, OUTPUT)
      wiringpi.softPwmCreate(EN, 0, 255)

  def setMotorContorl(PWM, INA, INB, speed, stat):
      wiringpi.softPwmWrite(PWM, speed)

      if stat == FORWARD:
          wiringpi.digitalWrite(INA, HIGH)
          wiringpi.digitalWrite(INB, LOW)

      elif stat == BACKWARD:
          wiringpi.digitalWrite(INA, LOW)
          wiringpi.digitalWrite(INB, HIGH)

      elif stat == STOP:
          wiringpi.digitalWrite(INA, LOW)
          wiringpi.digitalWrite(INB, LOW)

  def setMotor(ch, speed, stat):
      if ch == CH1:
          setMotorContorl(ENA, IN1, IN2, speed, stat)
      else:
          setMotorContorl(ENB, IN3, IN4, speed, stat)

  wiringpi.wiringPiSetup()

  setPinConfig(ENA, IN1, IN2)

  setMotor(CH1, dcspeed, dcstat)

#dection 좌표와 서보모터 움직임 mapping 알고리즘 시작
min_duty = 2.4
max_duty = 11.5
duty = {1: (0, 0)} #duty 값 초기생성 (딕셔너리 형태) 
i = 1 #for문 돌리기 위한 변수 선언


def coord_mapping (coord_x, coord_y):

    coord_y = 640 - coord_y

    x_real = (23/480)*coord_x
    y_real = (3/64)*coord_y

    x_real = abs(x_real - 11.5)

    if y_real-7 >= 27 :
        print("can't point")

        return (4.6, 7.6)

    if x_real >= 21 :
        print("can't point")

        return (4.6, 7.6)

    degree_x = math.asin(x_real/27)
    degree_y = math.asin((y_real-7)/21)

    duty_y = min_duty+(degree_y*(max_duty-min_duty)/180)
    duty_x = min_duty+(degree_x*(max_duty-min_duty)/180)

    if coord_x >= 240:
        duty_x = 7.4 - (duty_x-min_duty)
    else:
        duty_x  = 7.4 + (duty_x-min_duty)

    return (round(duty_x, 2), round(duty_y, 2))

def mapping (x, y, duty): #리스트 x,y를 받아 딕셔너리 duty에 저장
    for i in range(len(x)):
        duty[i+1] = coord_mapping(x[i], y[i])


pin1, pin2, pin3, pin4 = 11, 12, 13, 16  # servomotor pin
camera_pin = 15  # camera servomotor
button_start1_pin, button_start2_pin = 36, 38  # start button sw5,6
# opt button sw1,2,3,4,7
button1_pin, button2_pin, button3_pin, button4_pin, button5_pin = 22, 24, 26, 32, 40

#for dcmotor
STOP = 0
FORWARD = 1
BACKWARD = 2

CH1 = 0

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 25
IN1 = 24
IN2 = 23

#GPIO 버튼 입력 신호 받기위한 코드
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_start1_pin, GPIO.IN)
GPIO.setup(button_start2_pin, GPIO.IN)
GPIO.setup(button1_pin, GPIO.IN)
GPIO.setup(button2_pin, GPIO.IN)
GPIO.setup(button3_pin, GPIO.IN)
GPIO.setup(button4_pin, GPIO.IN)
GPIO.setup(button5_pin, GPIO.IN)

i = 1  #for문 돌리기 위한 변수 선언
j = 1  # 음성 읽어주기 위한 변수

try:

    while True:  # 초반 기본세팅
      if GPIO.input(button_start1_pin) == 0 or GPIO.input(button_start2_pin) == 0:  # start button 눌렀을 때
        while True:
          if GPIO.input(button_start1_pin) == 1 or GPIO.input(button_start2_pin) == 1:
             servoMotorCamera(camera_pin, 0)  # 카메라서보, 0 내려감
             time.sleep(3)
             servoMotorCamera(camera_pin, 1)  # 카메라서보 올라감
             time.sleep(8)
             servoMotor_on(pin3, pin4)  # start 접는위치에서 기본위치
             time.sleep(1)
             img = detect.camera()
             x, y, cnt, label, serious, serious2, frame = detect.detectAndDisplay(img)
             if veryserious == 1:
               send()
             cv2.imwrite('firebase.jpg', frame)
             fileUpload('firebase.jpg')
             mapping(x, y, duty)
             time.sleep(10)
             break
        break

    while True:  # OPT버튼2, 결과값 바탕으로 서보모터 구동
      if GPIO.input(button2_pin) == 0:
        while True:
          if GPIO.input(button2_pin) == 1:
              print('button2 ok')
              #기본위치에서 n번째 detection 좌표로
              servoMotor_move(pin1, pin2, pin3, pin4, duty[i][0], duty[i][1]) 
              break
        break

    for i in range(1, len(duty)+1):
      a = 1  #for문 한번 돌 때마다 버튼3 처음에서 한번 읽어주기 위한 초기화 변수
      while True:  # OPT버튼3, 신호주면 dc모터 작동
        if GPIO.input(button3_pin) == 0:
          while True:
            if GPIO.input(button3_pin) == 1:
                #음성 읽어주기 1개 단위, 첫번째만 실행, j=1일 때 1번  
                if a == 0:
                  print('no voice')
                else:
                  if label1 == gumbuseot and j == 1:
                    detect.soundopen('gumbavaliable.wav')
                    detect.size(serious1)
                  elif label2 == littlepimple and j == 2:
                    detect.soundopen('littlepimpleavaliable.wav')
                    detect.size(serious2)
                  elif label3 == paekban and j == 3:
                    detect.soundopen('paekbanavaliable.wav')
                    detect.size(serious3)
                  elif label4 == daesang and j == 4:
                    detect.soundopen('daesangavaliable.wav')
                    detect.size(serious4)
                  elif label5 == hongban and j == 5:
                    detect.soundopen('hongbanavaliable.wav')
                    detect.size(serious5)
                  elif label6 == pimple and j == 6:
                    detect.soundopen('pimpleavaliable.wav')
                    detect.size(serious6)

                dcMotor(50, FORWARD)
                wiringpi.delay(1000)
                dcMotor(20, STOP)

                a = 0 #다음번 3번 버튼을 눌렸을 때 음성 실행하지 않기 위해서
                break
                          
        elif GPIO.input(button4_pin) == 0:
          while True:
            if GPIO.input(button4_pin) == 1:
              print('go to button4')
              break
            break

        elif GPIO.input(button5_pin) == 0: #긴급정지
          while True:
            if GPIO.input(button5_pin) == 1:
              print('stop')
              sys.exit('stop')

        elif GPIO.input(button1_pin) == 0: 
          while True:
            if GPIO.input(button1_pin) == 1:
              print('go to button1')
              i = len(duty)+1 #for문 벗어나고, 한번 더 클릭하면 실행됨
              break
            break

      while True:  # OPT버튼4, 신호주면 dc모터 원 위치후 다음꺼 작동
        if GPIO.input(button4_pin) == 0:
          while True:
              if GPIO.input(button4_pin) == 1:
                  dcMotor(100, BACKWARD)
                  wiringpi.delay(3000)
                  dcMotor(50, STOP)
                  if len(duty)+1 > i:
                    #n번째 detection 좌표에서 기본위치로
                    servoMoto_init(pin1, pin2, pin3, pin4, duty[i][0], duty[i][0])
                    #기본위치에서 n+1번째 detection 좌표로
                    servoMotor_move(pin1, pin2, pin3, pin4, duty[i+1][0], duty[i+1][1])
                  elif len(duty)+1 <= i:
                    servoMoto_init(pin1, pin2, pin3, pin4, duty[i][0], duty[i][0])
                    print('complete')
                  i += 1  # 다음 detection 번호로
                  j += 1  # 다음 음성 번호로
                  break
          break

        elif GPIO.input(button5_pin) == 0:
            while True:
              if GPIO.input(button5_pin) == 1:
                  servoMotor_break()
                  print('stop')
                  sys.exit('stop')

        elif GPIO.input(button1_pin) == 0:
            while True:
              if GPIO.input(button1_pin) == 1:
                  print('go to button1')
                  i = len(duty)+1
                  break
            break

    while True:  # OPT버튼1, 음성으로 종합 정보 알려주기 조건)마지막에만, 클릭해야함
       if GPIO.input(button1_pin) == 0:
          while True:
            if GPIO.input(button1_pin) == 1:
              if cnt1 == 1:
                detect.soundopen('gumb1.wav')
              elif cnt1 == 2:
                detect.soundopen('gumb2.wav')
              elif cnt1 == 3:
                detect.soundopen('gumb3.wav')
              elif cnt1 == 4:
                detect.soundopen('gumb4.wav')
              elif cnt1 == 5:
                detect.soundopen('gumb5.wav')
              else:
                detect.soundopen('gumbmany.wav')

              if cnt2 == 1:
                detect.soundopen('littlepimple1.wav')
              elif cnt2 == 2:
                detect.soundopen('littlepimple2.wav')
              elif cnt2 == 3:
                detect.soundopen('littlepimple3.wav')
              elif cnt2 == 4:
                detect.soundopen('littlepimple4.wav')
              elif cnt2 == 5:
                detect.soundopen('littlepimple5.wav')
              else:
                detect.soundopen('littlepimplemany.wav')

              if cnt3 == 1:
                detect.soundopen('paekban1.wav')
              elif cnt3 == 2:
                detect.soundopen('paekban2.wav')
              elif cnt3 == 3:
                detect.soundopen('paekban3.wav')
              elif cnt3 == 4:
                detect.soundopen('paekban4.wav')
              elif cnt3 == 5:
                detect.soundopen('paekban5.wav')
              else:
                detect.soundopen('paekbanmany.wav')

              if cnt4 == 1:
                detect.soundopen('daesang1.wav')
              elif cnt4 == 2:
                detect.soundopen('daesang2.wav')
              elif cnt4 == 3:
                detect.soundopen('daesang3.wav')
              elif cnt4 == 4:
                detect.soundopen('daesang4.wav')
              elif cnt4 == 5:
                detect.soundopen('daesang5.wav')
              else:
                detect.soundopen('daesangmany.wav')

              if cnt5 == 1:
                detect.soundopen('hongban1.wav')
              elif cnt5 == 2:
                detect.soundopen('hongban2.wav')
              elif cnt5 == 3:
                detect.soundopen('hongban3.wav')
              elif cnt5 == 4:
                detect.soundopen('hongban4.wav')
              elif cnt5 == 5:
                detect.soundopen('hongban5.wav')
              else:
                detect.soundopen('hongbanmany.wav')

              if cnt6 == 1:
                detect.soundopen('pimple1.wav')
              elif cnt6 == 2:
                detect.soundopen('pimple2.wav')
              elif cnt6 == 3:
                detect.soundopen('pimple3.wav')
              elif cnt6 == 4:
                detect.soundopen('pimple4.wav')
              elif cnt6 == 5:
                detect.soundopen('pimple5.wav')
              else:
                detect.soundopen('pimplemany.wav')
              print('alarm')
              break

       elif GPIO.input(button5_pin) == 0:
        while True:
          if GPIO.input(button5_pin) == 1:
            servoMotor_break()
            print('실행 종료')
            sys.exit('Finish')

# Ctrl + C키를 누르면 종료 됩니다.
except KeyboardInterrupt:
    print('실행 종료')
    servoMotor_off()
    # 종료시

# GPIO 클린업
finally:
    GPIO.cleanup()
