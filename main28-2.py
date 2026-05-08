import urllib.request
import json
import datetime 
import asyncio # 비동기 프로그래밍을 위한 라이브러리
from telegram import Bot # 텔레그램 봇 API 라이브러리 임포트

telegram_id = '8391939' #텔레그램 id
my_token = '119374839:FFlkejl1AbCdEfGhIjKlMnOpQrStUvWxYz' #틀레그램 봇 토큰값
api_key = '0aafca2752f24952554ababc8376967c' #OpenWeatherMap API 키값

bot = Bot(token=my_token)  #텔레그램 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22] # 사용자 정의 시간 알림 
ALERT_TIMES = ["08:30", "15:20"]  # 사용자 정의 시간 알림 (예: "08:30", "15:20")

def getWeather(): 
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid=0aafca2752f24952554ababc8376967c&units=metric&lang=en&cnt=8"

    with urllib.request.urlopen(url) as r: #API 주소로 요청 보내고 응답 받기
        data = json.loads(r.read()) #받은 데이터를 JSON → Python 딕셔너리로 변환

    text = "" #8개의 예보 데이터에서 시간, 온도, 습도, 날씨 설명 추출하여 문자열로 만들기
    for i in range(8):
        item = data['list'][i]
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
        temp = item['main']['temp']
        humi = item['main']['humidity']
        desc = item['weather'][0]['description']
        text += f"({hour}h {temp}C {humi}% {desc})\n"

    return text #최종적으로 만들어진 문자열 반환

async def main(): #비동기 함수 정의, 텔레그램 메시지 전송과 시간 체크를 동시에 처리하기 위해 사용
    try:
        while True:
            now = datetime.datetime.now() #현재 시간 정보 가져오기
            hm = now.strftime('%H:%M')  #  현재 시간을 "HH:MM" 형식의 문자열로 변환

            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0 #현재 시간이 ALERT_HOURS에 정의된 시간 중 하나이고, 분과 초가 모두 0일 때 알림 조건 충족
            is_alert_time = hm in ALERT_TIMES and now.second == 0  #현재 시간이 ALERT_TIMES에 정의된 시간 중 하나이고, 초가 0일 때 알림 조건 충족

            if is_alert_hour or is_alert_time: #알림 조건이 충족되면 getWeather() 함수를 호출하여 날씨 정보를 가져오고, 텔레그램 메시지로 전송
                msg = getWeather() #날씨 정보를 가져오는 함수 호출
                print(msg) #콘솔에도 날씨 정보 출력 (디버깅용)
                await bot.send_message(chat_id=telegram_id, text=msg) #텔레그램 봇을 사용하여 메시지 전송, await 키워드를 사용하여 비동기적으로 처리

            await asyncio.sleep(1) #1초마다 현재 시간을 체크하여 알림 조건이 충족되는지 확인, asyncio.sleep()을 사용하여 비동기적으로 대기

    except KeyboardInterrupt: #사용자가 키보드 인터럽트 (Ctrl+C)를 발생시키면 프로그램이 종료되도록 처리
        pass #  프로그램 종료 시 특별한 작업이 필요하지 않으므로 pass로 처리

asyncio.run(main())