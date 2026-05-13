import json

with open('parties.json', 'r') as file:
    parties = json.load(file)
    
# print(json.dumps(parties, indent=4))

class party:
    def __init__(self, name:str, votes:int):
        self.name = name
        self.votes = votes

    def count_party_percentage(votes: int, total_votes:int) -> float:
        party_percentage:float = (votes*100)/total_votes
        return party_percentage
    
    voting_margin:bool = False
    
