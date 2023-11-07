# https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
from flask import Flask, abort, request, render_template,jsonify,Response, send_file
from markupsafe import escape
import time
import os 
from os.path import exists
from stage0 import stage0
from stage1 import stage1
from stage2 import stage2
from stage3 import stage3
from quick_answer_serp import quick_answer_serp, str_to_bool
from werkzeug.utils import secure_filename

app = Flask(__name__)

# main page. Prints the returned value
@app.route('/')
# def hello_world():
#     return 'Hello, Docker 4!'
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

        # Get the value of a monotonic clock using time.monotonic() method 
        value = time.monotonic()
        enable_quick_answer = None
        text = request.form['text']
        question = text
        language = request.form['language']
        website = request.form['website']
        enable_quick_answer = str_to_bool(request.form['enable_quick_answer'])
        detailed_answer = str_to_bool(request.form['detailed_answer'])
        model = request.form['model']

        if text == '':
            return jsonify({'error': 'Please enter a value for \'textInput\'.'}), 400

        print(text)
        print(language)
        print(enable_quick_answer)
        print(website)

        print("----------------ElasticsearchDocumentStore Initializing----------------")
        from haystack.document_stores import ElasticsearchDocumentStore

        # Get the host where Elasticsearch is running, default to localhost
        host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

        document_store = ElasticsearchDocumentStore(
            host=host,
            username="",
            password="",
            index="document"
        )
        print("----------------ElasticsearchDocumentStore Initialized----------------")
        
        file_exists = exists("Data/dataT.txt")
        results = []
        
        file_exists = False # it has to be removed
        if file_exists:
            print("[][][]")
            [answer0, table] = stage0("Data/", document_store, question,model)
            srt = ""
            results_score = []
            for i in answer0:
                if i[1] == None:
                    srt = srt + "<br>" + "The answer is: <b>"+ i[0]+ "</b> with as score of "+ " None "+ " in website: " + i[2] + "<br>" +  " context: " + i[3] + "<br>" + "<br>" 
                elif i[2] == None:
                    srt = srt + "<br>" + "The answer is: <b>"+ i[0]+ "</b> with as score of "+ str(i[1])+ " in website: " + "None"
                else:
                    srt = srt + "<br>" + "The answer is: <b>"+ i[0]+ "</b> with as score of "+ str(i[1])+ " in website: " + i[2] + "<br>" +  " context: " + i[3] + "<br>" + "<br>" 
                results_score.append(i[1])
            results.append(srt)
            results.append(results_score)
            print(results_score)
            if answer0[0][1] > 0.8:           
                value0 = time.monotonic()
                v0 = value0 - value
                timeResults = "Stage 0 lasted "+ str(v0) + " seconds"
                results.append(timeResults)
                response = {'results': results}
                return jsonify(response)
        else:
            print("[[[[[No previous questions]]]]]")

        value1 = time.monotonic()
        print("----------------Stage 1----------------")
        
        [url, dic, important_word, df, target_websites] = stage1(question,language,website)
        value2 = time.monotonic()
        print("----------------Check for Quick Answer----------------")
        print(enable_quick_answer)
        if enable_quick_answer == True:
            print("----------------Stage quick----------------")
            # very quick answer. Limited results per month. Enable !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            quick_results = quick_answer_serp(question)
            srt0=""
            for i in quick_results:
                srt0 = srt0 + "<br>" + "The answer is: "+ i[0]+ " with as score of "+ str(i[1])
            results.append(srt0)
            if detailed_answer==False:
                if quick_results[0][1]>0.9:
                    response = {'results': results}
                    return jsonify(response)
        else:
            print("----------------No Quick Answer----------------")
        value3 = time.monotonic()    

        # Process the question and get the results
        print("----------------Stage 2----------------")
        [answer1, table] = stage2(url, dic, document_store, important_word, df, question,model)
        srt = ""
        results.append(url)
        results_score = []
        results_score1 = []
        for i in answer1:
            srt = srt + "<br>" + "The answer is: <b>"+ i[0]+ "</b> with as score of "+ str(i[1])
            results_score.append(i[1])
            results_score1.append(i[1])
            results_score.append("<br>")
        results.append(srt)
        # results.append(results_score)
        # print(results_score)
        value4 = time.monotonic()
        if detailed_answer==False:
                print(answer1[0][1])
                if float(answer1[0][1])>0.91:
                    response = {'results': results}
                    return jsonify(response)
        print("----------------Stage 3----------------")
        [answer2] = stage3(url, dic, document_store, important_word, df,target_websites, question,model,table) 
        srt2 = ""
        results_score = []
        results_score2 = []
        j = 0    
        for i in answer2:
            if i[2] == None:
                print("Skipped because of None value")
                continue
            j = j +1
            srt2 = srt2 + "<br>" + str(j) + "   " + "The answer is: <b>"+ i[0]+ "</b> with as score of "+ str(i[1])+ " in website: " + i[2] + "<br>" +  " context: " + i[3] + "<br>" + "<br>" 
            results_score.append(i[1])
            results_score2.append(i[1])
            results_score.append("<br>")
        results.append(srt2)
        # results.append(results_score)
        # print(results_score)
        value5 = time.monotonic()

        time_results_only=[]
        times_results_1 = []
        values = []
        values.append(value1 - value)
        values.append(value2 - value1)
        values.append(value3 - value2)
        values.append(value4 - value3)
        values.append(value5 - value4)
        timeResults = "Getting the queries from the user lasted "+ str(values[0])+ " seconds. <br>"+ "Stage 1  lasted "+ str(values[1])+ " seconds. <br>"+ "Fast Answer (if enabled) lasted "+ str(values[2])+ \
              " seconds. <br>"+ "Stage 2  lasted "+ str(values[3])+ " seconds. <br>"+ "Stage 3  lasted "+ str(values[4])+ " seconds. <br>"
        for v in values:
            time_results_only.append("<br>")
            time_results_only.append(v)
            times_results_1.append(v)
        
        results.append(timeResults)
        # results.append(time_results_only)
        
        # Return the results as JSON response
        response = {'results': results}
        print(results_score1)
        print("---------------------------------------------")
        print(results_score2)
        print("---------------------------------------------")
        print(times_results_1)
        # print(response)
        return jsonify(response)

    return render_template('my-form.html')

    #     return render_template('my-form.html', question=question, result=srt)
    # return render_template('my-form.html')

# https://pythonbasics.org/flask-upload-file/
@app.route('/Import/')
def upload_file1():
   return render_template('upload.html')

@app.route('/Import/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

# https://dev.to/grahammorby/let-users-download-files-in-flask-5gjg
@app.route('/download/')
def download():
    path = 'results.txt'
    return send_file(path, as_attachment=True)

# about page
@app.route('/about/')

def about():
    return render_template('about.html')

@app.route('/results/')
def results():
    results = ['This is the first result.',
                'This is the second result.',
                'This is the third result.',
                'This is the fourth result.'
                ]

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', debug=True)