import json, uuid, os

def gen_unique_id():
    id = uuid.uuid4()
    return str(id).upper()

class Labels:
    labels = {
        "POSITIVE" : {
                        "name": "Positive",
                        "group": "Primary Coaching Behaviour"
                    },
        "NEGATIVE" : {
                        "name": "Negative",
                        "group": "Primary Coaching Behaviour"
                    }
    }

class Code:
    def __init__(self) -> None:
        self.startTime = -1
        self.endTime = -1
        self.uniqueId = gen_unique_id()
        self.instanceNum = -1
        self.labels = []
        
    def generateText(self) -> str:
        text = {
                    "endTime": self.endTime,
                    "instanceNum": self.instanceNum,
                    "notes": "",
                    "labels": self.labels,
                    "startTime": self.startTime,
                    "sharing": True,
                    "modifyCount": 4,
                    "uniqueId": self.uniqueId
                }
        
        return text
        

class Row:
    
    count = 0
    
    def __init__(self) -> None:
        self.name = "Coach Talking"
        self.colour = "#878787"
        self.uniqueId = gen_unique_id()
        
        Row.count += 1
        self.rowNum = Row.count
        
        self.instances = []
        self.instanceCount = 0
        
    def addInstance(self, code) -> None:
        self.instanceCount += 1
        code.instanceNum = self.instanceCount
        self.instances.append(code.generateText())
        
    def generateText(self) -> str:
        text = {
                    "modifyCount": 2,
                    "name": self.name,
                    "color": self.colour,
                    "instances": self.instances,
                    "uniqueId": self.uniqueId,
                    "rowNum": self.rowNum
                }
        
        return text

class Timeline:
    def __init__(self) -> None:
        self.rows = {}
        
    def addRow(self, row) -> None:
        self.rows[row.name] = row
        
    def generateText(self, path) -> str:
        
        rowText = []
        for row in self.rows.values():
            rowText.append(row.generateText())
        
        text = {
                    "timeline": {
                        "currentModifyCount": 4,
                        "uniqueId": gen_unique_id(),
                        "rows": rowText,
                        "labels": [
                            {
                                "group": "Coach talking",
                                "name": "Positive Feedback"
                            }
                        ],
                        "packagePath": path
                    },
                    "currentPlaybackTime": 0
                }
        
        return text
    
    def createFile(self, path, filename) -> None:
        with open( os.path.join(path, filename+'.SCTimeline'), 'w' ) as file:
            file.write(
                json.dumps(self.generateText(path), separators=(',', ':'))
                )