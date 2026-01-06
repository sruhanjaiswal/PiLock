from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import time

ARDUINO_PORT = "/dev/ttyUSB0"  # change if needed
BAUD_RATE = 9600

arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

app = Flask(__name__)
CORS(app)

PASSWORD = "0000"
wrong_attempts = 0

@app.route("/pilock", methods=["POST"])
def pilock():
    global wrong_attempts
    data = request.json
    action = data.get("action")
    password = data.get("password", "")

    # Password protected LOCK/UNLOCK
    if action in ["LOCK", "UNLOCK"]:
        if password != PASSWORD:
            wrong_attempts += 1
            arduino.write(b"WRONG\n")
            return jsonify({"status": "WRONG ATTEMPT"})
        else:
            wrong_attempts = 0
            arduino.write(f"{action}\n".encode())
            arduino.write(b"RECOGNIZED\n")
            return jsonify({"status": "RECOGNIZED"})

    # Command box actions
    if action in ["SERVO_0","SERVO_90","SERVO_180","LED12_ON","LED12_OFF","LED13_ON","LED13_OFF"]:
        arduino.write(f"{action}\n".encode())
        return jsonify({"status": f"{action} executed"})

    return jsonify({"status": "UNKNOWN ACTION"})

if __name__ == "__main__":
    print(f"Connected to Arduino on {ARDUINO_PORT}")
    app.run(host="0.0.0.0", port=5000)
