# https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application


from flask import Flask, abort, request, render_template,jsonify,Response
from flask_socketio import SocketIO, emit, disconnect
from markupsafe import escape
from stage1 import stage1
from stage2 import stage2
from stage3 import stage3
from quick_answer_serp import quick_answer_serp
import time
from threading import Thread
from os.path import exists
import subprocess

from random import random
from threading import Lock
from datetime import datetime

"""
Background Thread
"""
thread = None
thread_lock = Lock()


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
app.config["TEMPLATES_AUTO_RELOAD"] = True

# main page. Prints the returned value
@app.route('/')
def hello():
    import datetime
    import pytz

    # Get the current UTC time
    utc_dt = datetime.datetime.utcnow()

    # Convert UTC time to Athens timezone
    athens_tz = pytz.timezone('Europe/Athens')
    athens_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(athens_tz)
    return render_template('index.html', utc_dt=athens_dt)

# textbox
@app.route('/SkapisBot/', methods=['GET', 'POST'])
def my_form():
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        results =[text , text+"23424432"]
        # Return the initial response immediately
        response = {'results': results}
        socketio.emit('update_results', response, namespace='/SkapisBot/')
        time.sleep(5) 
        results.append(text+text)
        response = {'results': results}
        socketio.emit('update_results', response, namespace='/SkapisBot/')
        # return jsonify({'message': 'Processing request'})


        # try:
        #     text = request.form['text']
        #     results =[text , text+"23424432"]
        #     proc = subprocess.Popen(['ping', '127.0.0.1', '-c', results], bufsize=0, stdout=subprocess.PIPE)
        #     emit('task_update', { 'results': results })
        #     proc.stdout.close()
        #     proc.wait()
        #     result = results.append(text+text+text)
        #     emit('task_update', {'result': result})
        #     disconnect()
        # except Exception as ex:
        #     print(ex)

        text = request.form['text']
        results = [text, text + "23424432"]
        response = {'results': results}

        # <Emit an event before sleeping>

        # Sleep for 5 seconds
        time.sleep(5)

        results.append(text + text)
        # <Emit an event>

        # Return a response
        # return jsonify(response)        

    return render_template('testing.html')
    # return render_template('my-form2.html')
    # return render_template('my-form.html')


@app.route('/results/')
def results():
    results = ['This is the first result.',
                'This is the second result.',
                'This is the third result.',
                'This is the fourth result.'
                ]

    return render_template('results.html', results=results)

# about page
@app.route('/about/')
def about():
    return render_template('about.html')


"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)

"""
Serve root index file
"""
@app.route('/example/')
def index():
    return render_template('example.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
    # socketio.run(app)