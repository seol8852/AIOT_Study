#웹 서버를 만들 Flask와 하드웨어 핀을 제어할 LED 기능을 사용하기 위해 필요한 라이브러리를 임포트한다.
from flask import Flask 
from gpiozero import LED 

app = Flask(__name__) #Flask 웹 서버 객체 생성
red_led = LED(21) #라즈베리파이 핀 중 21번 핀에 연결된 led 객체 생성

@app.route('/')  #사용자가 기본 주소창에 접속했을 때 아래 코드를 실행
def home():
    return render_template("index.html") # 미리 만들어둔 HTML 파일을 화면에 띄움

@app.route('/data', methods=['POST']) #HTML 폼에서 POST 방식으로 /data 주소창에 접속했을 때 아래 코드를 실행  
def data():
    data = request.form['led'] # HTML 폼에서 'led'라는 이름으로 보낸 값 가져오기
    
    #  HTML 폼에서 'led'라는 이름으로 보낸 값이 'on'이면 LED 켜고, 'off'이면 LED 끄기
    if data == 'on': 
        red_led.on()
    elif data == 'off': 
        red_led.off()
        
    return home() # LED 제어 후 다시 메인 화면(index.html)으로 돌아감

if __name__ == "__main__": #이 파이썬 파일이 다른 곳에서 불려온 게 아니라, 터미널에서 직접 실행되었을 때만 아래 코드를 작동시키라는 파이썬만의 규칙
    app.run(host="0.0.0.0", port=80) ##만들어둔 서버를 드디어 가동, 80번 포트에서 같은 공유기를 쓰는 위부 기기에서도 접속 가능