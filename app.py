from flask import Flask
from flask import render_template, jsonify, request
from functions import classification, entity
from functions.intentHandler import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template("home.html")


@app.route('/chat', methods=["POST"])
def chat():
    """
    chat end point that performs NLU using our custom scripts
    """
    try:
        query = request.form["text"]
        # Extracting the post request - TEXT
        clf = classification.classification()
        # Creating a classification object
        intent = clf.classify(query)[0]
        print("Intent:" + str(intent))
        # intent matching
        if "job" in query:
            intent = "jobs"
        elif "blog" in query:
            intent = "get_blogs"
        elif "event" in query:
            intent = "event-request"

        response_text = ""
        # The response text which is sent back to the front end
        if type(intent) != "NoneType":
            if intent == "intro" or intent == "greet":
                response_text = hello(query)
            elif intent == "get_blogs" and len(query.split()) > 1:
                response_text = get_blogs(query)
            elif intent == "jobs" and len(query.split()) > 1:
                response_text = job(query)
            elif intent == "general" and len(query.split()) > 1:
                response_text = purpose(query)
            elif intent == "module" and len(query.split()) > 1:
                response_text = "The module part is still under progress"
            elif intent == "event-request" and len(query.split()) > 1:
                response_text = event_request(query)
            elif intent == "stop":
                response_text = "See you soon"
        return jsonify({"status": "success", "response": response_text})
    # Sending the response
    except Exception as e:
        print(e)
        return jsonify({"status": "success", "response": "Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000,debug=True)
