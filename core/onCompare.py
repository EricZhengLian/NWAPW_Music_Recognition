#print("python running")
import sys, json, time, os
time.sleep(3) #wait for the file to upload first
fileName = sys.argv[1]
userID = sys.argv[2]
dbname = sys.argv[3]
data = {}
path = "../site/comparisons/" + fileName
from db import Database
#print("marker 1")
db = Database()

#print("Database initialized")
csvpath = "./"
if str(os.getcwd()).endswith("site"):
	csvpath = "../core/"

db.load(csvpath+f"{dbname}.csv", csvpath+f"{dbname}_fingerprints.csv") #right now we load this because it's the only csv file there is.

#print("files loaded")

data["fileName"] = fileName
data["userID"] = userID
data["match"] = "no matches found"
data["confidence"] = 0
data["complete"] = False
a = []
try:
	a = db.query(path, log=False)
except:
	print("Something went wrong")

#print("marker 2")

#output might look like this: {'SONG_ID': '07B2461E5D6CFD6F2EDCE43736898C7F3AFE7D06', 'SONG_NAME': 'opera/常思思 - 炫境.wav', 'CONFIDENCE': 0.0035650623885918, 'OFFSET_DIFFERENCE': -1284, 'OFFSET_DIFFERENCE_IN_SEC': 0.09288}
if len(a) > 0:
	data["match"] = a["SONG_NAME"]
	data["confidence"] = 1#a["CONFIDENCE"]
	data["complete"] = True
out = json.dumps(data)
print(out)

try:
	os.system("rm " + path)
except:
	pass