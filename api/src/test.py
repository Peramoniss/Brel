import requests
import subprocess
import time

proc = subprocess.Popen(["uvicorn", "src.app:app", "--host", "127.0.0.1", "--port", "8000"])
time.sleep(2)

# lyrics = "I am not afraid to keep on living\nI am not afraid to walk this world alone\nHoney, if you stay you'll be forgiven\nNothing you can say can stop me going home\n\nThese bright lights have always blinded me\nThese bright lights have always blinded me, I say"
lyrics = "Hello darkness, my old friend\n\nI've come to talk to you again"

data = {
    "lyrics": lyrics,
    "lang": "pt",
    "strat": "stanza"
}

data = requests.post("http://127.0.0.1:8000/translate/", json=data)
print(data.text)

proc.terminate()