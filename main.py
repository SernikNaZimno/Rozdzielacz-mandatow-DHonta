import json

with open('parties.json', 'r') as file:
    parties = json.load(file)
    
print(json.dumps(parties, indent=4))