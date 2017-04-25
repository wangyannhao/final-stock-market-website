import json

data = open('./static/js/jsons/nabil.json').read() #opens the json file and saves the raw contents
jsonData = json.dumps(data) #converts to a json structure
