#print("python running")
import sys, json, time, os
time.sleep(3) #wait for the file to upload first
fileName = sys.argv[1]
userID = sys.argv[2]
dbname = sys.argv[3]
data = {}
path = "../site/uploads/" + fileName
from db import Database
#print("marker 1")
db = Database()

#print("Database initialized")
csvpath = "./"
if str(os.getcwd()).endswith("site"):
	csvpath = "../core/"

db.load(csvpath+f"{dbname}.csv", csvpath+f"{dbname}_fingerprints.csv") #right now we load this because it's the only csv file there is.
db.add(path)
db.save(csvpath+f"{dbname}.csv", csvpath+f"{dbname}_fingerprints.csv")
print("file added!")
try:
	os.system("rm " + path)
except:
	pass
