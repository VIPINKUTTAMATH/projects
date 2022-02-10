import json

class RuleEngine:
    def __init__(self,path):
        f = open(path)
        self.rules = json.load(f)
   
    def ExecuteRules(self, callback):
        for rule in self.rules['rules']:
            callback(rule['type'],rule['avg_min'],rule['avg_max'],rule['trigger_count'],rule['name'])
        
