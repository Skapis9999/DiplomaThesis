![Stars](https://img.shields.io/github/stars/Skapis9999/DiplomaThesis)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Top Language](https://img.shields.io/github/languages/top/Skapis9999/DiplomaThesis)
![Languages](https://img.shields.io/github/languages/count/Skapis9999/DiplomaThesis)

# DiplomaThesis
This is my Diploma Thesis "Development of a Private Dynamic Internet-based Question-Answering System"

# Topic
In this thesis, an attempt is made to develop a digital question-answering assistant that dynamically
searches the web for answers. This system, using pre-trained models and software technologies, answers user’s questions by using all the online information. The portability of the system can ensure a private experience as well as answers from specialized data sources.
Experimental results demonstrate that this system is sufficiently accurate while achieving the purposes for which it was developed. The analytical and conversational style of conventional digital assistants is sacrificed in order to exploit the maximum amount of information. Furthermore, the extensions of the system may lead to its use in specialised systems where the information available is limited and again comes from the internet but only from a specific source.

# How to Run

## Install
Install [Elastic Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#deb-key)

## Changes in the code
Change Line 30 in file stage1.py adding your own path to a directory where the data will be temporarily stored. Do the same with line 50. 

Enable your programming environment: ```source env/bin/activate```

Export the flask app: ```export FLASK_APP=app```

Run the application: ```flask run```

Open a browser and type in the URL ```http://127.0.0.1:5000/```.


