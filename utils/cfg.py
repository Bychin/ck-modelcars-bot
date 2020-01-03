import json

with open("cfg.json") as f:
    cfg = json.loads(f.read())

def get_param(setting):
    return cfg.get(setting)
