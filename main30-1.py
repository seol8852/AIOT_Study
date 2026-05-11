import paho.mqtt.client as mqtt  #MQTT 통신을 위한 라이브러리
import time #시간 관련 함수 (sleep)
from gpiozero import LED #라즈베리파이 GPIO로 LED 제어
import threading  #동시에 여러 작업 실행 (멀티스레드)

#GPIO 핀 번호 기준으로 LED를 연결
greenLed = LED(16) 
blueLed = LED(20) 
redLed = LED(21) 

#MQTT 메시지를 받았을 때 자동으로 실행되는 함수
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload)) #어떤 토픽에서 어떤 데이터가 왔는지 출력
    message = msg.payload.decode() #메시지는 바이트 형태 → 문자열로 변환
    print(message)
    if message == "green_on": 
        greenLed.on()
    elif message == "green_off":
        greenLed.off()
    elif message == "blue_on":
        blueLed.on()
    elif message == "blue_off":
        blueLed.off()
    elif message == "red_on":
        redLed.on()
    elif message == "red_off":
        redLed.off()

client = mqtt.Client()  #MQTT 클라이언트 객체 생성
client.on_message = on_message #MQTT 메시지를 받았을 때 실행될 함수 등록, 클라이언트 객체의 on_message 속성에 on_message 함수를 할당하여 메시지가 도착할 때마다 해당 함수가 호출되도록 설정

broker_address="10.60.10.226" #MQTT 서버(IP: 10.60.10.226)에 연결
client.connect(broker_address) #MQTT 서버에 연결한 후, "led"라는 토픽을 구독하여 해당 토픽으로 들어오는 메시지를 받을 준비를 함
client.subscribe("led",1) #"led"라는 토픽을 구독, QoS 1 (한 번 이상 전달 보장)

count = 0 #숫자 카운트용
def send_message(): #MQTT로 계속 메시지를 보내는 함수
    global count #함수 밖 변수 count 사용
    while 1:   # 무한 루프, 1초마다 count를 증가시키고 MQTT로 "hello" 토픽에 count 값을 문자열로 보내는 작업을 반복
        count += 1 #count 값을 1씩 증가
        client.publish("hello", str(count)) #MQTT로 "hello" 토픽에 count 값을 문자열로 보내기, 예: "1", "2", "3", ...
        time.sleep(1.0) #1초마다 메시지를 보내도록 sleep 함수를 사용하여 대기

task = threading.Thread(target=send_message) # send_message 함수를 별도의 스레드에서 실행하기 위해 threading.Thread 객체 생성, target 매개변수에 send_message 함수를 지정하여 해당 함수가 스레드에서 실행되도록 설정
task.start() #스레드 시작, send_message 함수가 별도의 스레드에서 실행되기 시작, 이로 인해 MQTT 메시지를 보내는 작업이 메인 스레드와 동시에 실행될 수 있게 됨

client.loop_forever() #MQTT 클라이언트의 네트워크 루프를 시작, 이 함수는 MQTT 서버와의 연결을 유지하고, 메시지를 수신할 때마다 on_message 콜백 함수를 호출하는 역할을 함, 이 함수가 호출되면 프로그램은 MQTT 통신을 계속 처리하면서 종료되지 않고 대기 상태가 됨