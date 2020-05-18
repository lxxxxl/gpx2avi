from flask import Flask
import time
app = Flask(__name__)
# FLASK_APP=sleep.py flask run

@app.route('/sleep/<seconds>')
def sleep(seconds):
    seconds_int = int(seconds)
    time.sleep(seconds_int)
    return 'Done'