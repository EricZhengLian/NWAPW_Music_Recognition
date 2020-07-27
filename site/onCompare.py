import sys, json, time
fileName = sys.argv[1]
userID = sys.argv[2]
data = {}
data["fileName"] = fileName
data["userID"] = userID
data["match"] = "no matches found"
data["confidence"] = 0
data["complete"] = True
time.sleep(10)
#at this point we pretend to have processed the file.
#print(data)
out = json.dumps(data)
print(out)