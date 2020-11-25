
# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/mark_.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])

def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		request_json = flask.request.get_json()
		logger.info(f'{dt} Data: name={request_json}')
		try:
			preds = model.predict(request_json['name'])
		except AttributeError as e:
				logger.warning(f'{dt} Exception: {str(e)}')
				data['predictions'] = str(e)
				data['success'] = False
				return flask.jsonify(data)
		data["predictions"] = preds
		data["success"] = True
	return flask.jsonify(data)

if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 5001))
	app.run(host='localhost', debug=True, port=port)
