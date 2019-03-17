import json


class formatJSON():
    def __init__(self, fileName):
        self.fileName = fileName

    def formatJSON(self):
        path = "newJSON.json"
        newJSON = open(path, 'w')
        newJSON.write('[ ')
        with open(self.fileName, 'r') as infile:
            data = infile.read()
            new_data = data.replace('}\n{', '},\n{')
            json_data = json.loads(f'[{new_data}]')
            print(json_data)
            newJSON.write(new_data)
        newJSON.write(' ]')
        newJSON.close()
