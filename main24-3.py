import urllib.request, json, tkinter, tkinter.font 
#urllib.request: 인터넷에서 데이터를 가져오는데 사용
#json: 인터넷에서 받아온 텍스트 데이터를 파이썬이 다루기 쉬운 사전 형태로 변환
#tkinter, tkinter.font: GUI 창과 글꼴을 만드는데 사용
 
API_KEY = "0aafca2752f24952554ababc8376967c" #오픈웨더 api키
 
def tick1Min():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric" #날씨 정보를 요청할 인터넷 주소 설정
    with urllib.request.urlopen(url) as r: #인터넷 주소로 요청을 보내고 응답을 받음
        data = json.loads(r.read()) #받은 응답을 텍스트로 읽어서 json.loads() 함수를 사용하여 파이썬 사전 형태로 변환
    temp = data["main"]["temp"] #사전에서 "main" 키의 값(또 다른 사전)에서 "temp" 키의 값을 가져옴 
    humi = data["main"]["humidity"] #사전에서 "main" 키의 값(또 다른 사전)에서 "humidity" 키의 값을 가져옴
    label.config(text=f"{temp:.1f}C   {humi}%") #label 위젯의 텍스트를 온도와 습도로 업데이트. 온도는 소수점 한 자리까지 표시되고, 습도는 정수로 표시
    window.after(20000, tick1Min) #window.after() 메서드를 사용하여 20000밀리초(20초) 후에 tick1Min 함수를 다시 호출하도록 설정. 이렇게 하면 20초마다 날씨 정보가 업데이트됨
 
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY")
window.geometry("400x100") # 창의 크기를 400x100 픽셀로 설정
window.resizable(False, False) #창의 크기를 고정하여 사용자가 창의 크기를 변경하지 못하도록 설정. 첫 번째 False는 가로 크기, 두 번째 False는 세로 크기에 대한 설정
font = tkinter.font.Font(size=30) 
label = tkinter.Label(window, text="", font=font) #tkinter.Label() 함수를 사용하여 label 위젯을 생성. 첫 번째 매개변수로 window를 전달하여 label이 이 창에 속하도록 지정
label.pack() #label.pack() 메서드를 호출하여 label 위젯을 창에 배치
tick1Min() 