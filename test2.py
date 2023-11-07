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

app = Flask(__name__)
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
        time.sleep(5) 
        results.append(text+text)
        response = {'results': results}


        text = request.form['text']
        results = [text, text + "23424432"]
        response = {'results': results}

        # <Emit an event before sleeping>

        # Sleep for 5 seconds
        time.sleep(5)

        results.append(text + text)
        # <Emit an event>

        # Return a response
        return jsonify(response)        

    # return render_template('testing.html')
    # return render_template('my-form2.html')
    return render_template('my-form.html')


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

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
    # socketio.run(app)