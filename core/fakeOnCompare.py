#mainly for testing purposes
import sys, json, time, os
fileName = sys.argv[1]
userID = sys.argv[2]
dbname = sys.argv[3]
data = {}
path = "../site/comparisons/" + fileName
time.sleep(5)


data["fileName"] = fileName
data["userID"] = userID
data["match"] = "example match"
data["confidence"] = 0
data["complete"] = True

out = json.dumps(data)
print(out)