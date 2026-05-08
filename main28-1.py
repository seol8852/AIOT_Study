import urllib.request
import json

api_key = '0aafca2752f24952554ababc8376967c'

#서울 날씨 데이터를 요청할 API 주소 생성
url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid=0aafca2752f24952554ababc8376967c&units=metric&lang=en&cnt=8"

with urllib.request.urlopen(url) as r: #API 주소로 요청 보내고 응답 받기
    data = json.loads(r.read()) #받은 데이터를 JSON → Python 딕셔너리로 변환

text = ""
for i in range(8): #8개의 예보 데이터에서 시간, 온도, 습도, 날씨 설명 추출하여 문자열로 만들기
    item = data['list'][i] #i번째 예보 데이터
    hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2) #UTC 시간에서 한국 시간으로 변환하여 시(hour) 추출
    temp = item['main']['temp'] #온도 추출
    humi = item['main']['humidity'] #습도 추출
    desc = item['weather'][0]['description'] #날씨 설명 추출 (예: "clear sky", "light rain" 등)
    text = text + "(" + str(hour) + "h " # 시간 정보 추가
    text = text + str(temp) + "C " # 온도 정보 추가
    text = text + str(humi) + "% " # 습도 정보 추가
    text = text + str(desc) + ")" # 날씨 설명 정보 추가

print(text)