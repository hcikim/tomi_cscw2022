from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import numpy as np
import pickle, random
import stanfordnlp
import urllib.parse


app = Flask(__name__, static_url_path='')
app._static_folder = "static"
CORS(app, support_credentials=True)
	
# load parser. This sets up a default neural pipeline in English.
nlp = stanfordnlp.Pipeline()

@app.route('/', methods = ["GET"])
def index():
	print("test message")
	tmp = request.url.split("?")[1]
	msg = tmp.split("&")[0] # utterance
	uid = tmp.split("&")[1] # from which user
	sentence = urllib.parse.unquote(msg)
	# sentence = msg.replace("%20", " ")
	print(sentence)
	now = datetime.now()
	timestamp = datetime.timestamp(now)
	dt_object = datetime.fromtimestamp(timestamp)
	# print("test message before if line")

	if len(sentence.split()) > 2 and "?" not in sentence:

		doc = nlp(sentence)

		# if it has only one sentence
		if len(doc.sentences) == 1:
			js = getAss(doc.sentences[0])

		# if it has more than one sentences
		else:
			sen = random.sample(doc.sentences, 1)
			js = getAss(sen[0])

	else:
		temp = {0: " ", 1: " ", 2: " ", 3: " ", 4: " "}
		js = jsonify(temp)

		return js

	try:
		with open("../log/chat_log.pickle", "rb") as r:
			log = pickle.load(r)

		log["uid"].append(uid)
		log["time"].append(dt_object)
		log["usr_input"].append(sentence)
		log["return"].append(js.get_data(as_text=True))

		with open("../log/chat_log.pickle", "wb") as w2:
			pickle.dump(log, w2)

	except:
		log = {"uid": [], "time": [], "usr_input": [], "return": [], "intersact": []}
		
		log["uid"].append(uid)
		log["time"].append(dt_object)
		log["usr_input"].append(sentence)
		log["return"].append(js.get_data(as_text=True))
		
		with open("../log/chat_log.pickle", "wb") as w:
			pickle.dump(log, w)

	return js

def getAss(_sent):

	nouns = []
	nouns_idx = []

	# identify nouns
	for word in _sent.words:
		if "NN" in word.xpos:
			nouns.append(word.lemma)
			nouns_idx.append(word.index)

	# if it has only one noun
	if len(nouns) == 1:
		# get associated words of it
		temporal = initiate(nouns[0])
		return jsonify(temporal)

	# if it has more than one nouns
	elif len(nouns) > 1:
		return dep2prob(_sent, nouns, nouns_idx)

	else:
		temp = {0: " ", 1: " ", 2: " ", 3: " ", 4: " "}
		return jsonify(temp)


def dep2prob(_sent, nuns, nuns_idx):

	governs = []

	for word in _sent.words:
		# governor is index of governing lexicon
		governs.append(word.governor)

	prob = {}
	s = 0
	# print(nuns_idx)
	for idx in nuns_idx:
		cnt = governs.count(int(idx))
		# print(governs)
		prob[idx] = cnt
		s += cnt
		print(s)

	print(prob)
	for k in prob:
		prob[k] = prob[k] + 1

	print(prob)
	p = []

	for i in prob:
		p.append(float(prob[i] / (s + len(prob))))
	print(p)

	noun = np.random.choice(nuns, 1, p=p)
	print(nuns)
	temp = initiate(noun[0])

	return jsonify(temp)

def initiate(w):

	with open('../data/assoc_keys.pickle', 'rb') as p:
		words = pickle.load(p)

	with open('../data/12knouns.pickle', 'rb') as k12:
		kns = pickle.load(k12)

	try:
		# first check if there is any intersaction
		first = words[w.lower()]
		intersact = [ask for ask in first if ask in kns]

		if len(intersact):
			binary = 1

		else:
			binary = 0

		try:

			with open("../log/chat_log.pickle", "rb") as r1:
				log = pickle.load(r1)

			log["intersact"].append(binary)

			with open("../log/chat_log.pickle", "wb") as w21:
				pickle.dump(log, w21)

		except:
			log = {"uid": [], "time": [], "usr_input": [], "return": [], "intersact": []}
			
			log["intersact"].append(binary)
			
			with open("../log/chat_log.pickle", "wb") as w3:
				pickle.dump(log, w3)


		# if the intersacted nouns are more less than 5
		if len(intersact) < 5:

			distint = [key for key in first if key not in intersact]
			# randomly select more as much as needed
			add = random.sample(distint, 5 - len(intersact))
			recommend = add + intersact

		# if the intersacted nouns are equal or more than 5
		else:
			# just randomly select 5 out of them
			recommend = random.sample(intersact, 5)
		
		t = {}
		# print(recommend)
		for i in range(len(recommend)):
			t[i] = recommend[i]
		# print(t)
		return t

	except:
		temp = {0: " ", 1: " ", 2: " ", 3: " ", 4: " "}
		return temp


if __name__ == '__main__':
	app.run(debug=True)

