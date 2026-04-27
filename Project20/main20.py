#웹 서버를 만들 Flask와 하드웨어 핀을 제어할 LED 기능을 사용하기 위해 필요한 라이브러리를 임포트한다.
from flask import Flask 
from gpiozero import LED 

#객체 생성
app = Flask(__name__) #Flask 웹 서버 객체 생성
red_led = LED(21)  #라즈베리파이 핀 중 21번 핀에 연결된 led 객체 생성

@app.route('/') #사용자가 기본 주소창에 접속했을 때 아래 코드를 실행
def flask():
    return "hello Flask" #웹 브라우저에 "hello Flask"라는 문구를 띄워준다.

@app.route('/ledon') #사용자가 /ledon 주소창에 접속했을 때 아래 코드를 실행
def ledOn():
    red_led.on() #코드가 실행되면서 라즈베리파이 21번 핀에 전기가 통해 실제 하드웨어 불이 켜짐
    return "<h1> LED ON </h1>"  #그 후 브라우저 화면에는 HTML의 <h1> 태그를 입힌 "LED ON"이라는 큰 글씨를 띄워줌

@app.route('/ledoff') #사용자가 /ledoff 주소창에 접속했을 때 아래 코드를 실행
def LedOff():
    red_led.off() #코드가 실행되면서 라즈베리파이 21번 핀에 흐르던 전기가 끊어져 실제 하드웨어 불이 꺼짐
    return "<h1> LED OFF </h1>"  #그 후 브라우저 화면에는 HTML의 <h1> 태그를 입힌 "LED OFF"라는 큰 글씨를 띄워줌

if __name__ == "__main__": #이 파이썬 파일이 다른 곳에서 불려온 게 아니라, 터미널에서 직접 실행되었을 때만 아래 코드를 작동시키라는 파이썬만의 규칙
    app.run(host="0.0.0.0", port=80) #만들어둔 서버를 드디어 가동, 80번 포트에서 같은 공유기를 쓰는 위부 기기에서도 접속 가능