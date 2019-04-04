import json

list = ['40', '20', '10', 'positive']
x = [
    {"positive": list[0], "neutral": list[1],
        "negative": list[2], "verdict": list[3]}
]
# x = json.dumps(None)
# x = {}
# x["positive"] = list[0]
# x["neutral"] = list[1]
# x["negative"] = list[2]
# x["verdict"] = list[3]
print(x)
print(type(x))
print(json.dumps(x))
print(type(json.dumps(x)))
# print(json.loads(x))
# print(type(json.loads(x)))
