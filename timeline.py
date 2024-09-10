import json, uuid, os

def gen_unique_id():
    id = uuid.uuid4()
    return str(id).upper()

class Labels:
    labels = {
        "Corrective Feedback" : {
                        "name": "Corrective Feedback",
                        "group": "Primary Coaching Behaviour"
                    },
        "General Feedback +ve" : {
                        "name": "General Feedback +ve",
                        "group": "Primary Coaching Behaviour"
                    },
        "General Feedback -ve" : {
                        "name": "General Feedback +ve",
                        "group": "Primary Coaching Behaviour"
                    },
        "Specific Feedback +ve" : {
                        "name": "Specific Feedback +ve",
                        "group": "Primary Coaching Behaviour"
                    },
        "Specific Feedback -ve" : {
                        "name": "Specific Feedback +ve",
                        "group": "Primary Coaching Behaviour"
                    },
        "Humour" : {
                        "name": "Humour",
                        "group": "Primary Coaching Behaviour"
                    },
        "Hustle" : {
                        "name": "Hustle",
                        "group": "Primary Coaching Behaviour"
                    },
        "Instruction" : {
                        "name": "Instruction",
                        "group": "Primary Coaching Behaviour"
                    },
        "Management - Criticisms" : {
                        "name": "Management - Criticisms",
                        "group": "Primary Coaching Behaviour"
                    },
        "Management - Direct" : {
                        "name": "Management - Direct",
                        "group": "Primary Coaching Behaviour"
                    },
        "Management - Indirect" : {
                        "name": "Management - Indirect",
                        "group": "Primary Coaching Behaviour"
                    },
        "Positive Modelling" : {
                        "name": "Positive Modelling",
                        "group": "Primary Coaching Behaviour"
                    },
        "Negative Modelling" : {
                        "name": "Negative Modelling",
                        "group": "Primary Coaching Behaviour"
                    },
        "Praise" : {
                        "name": "Praise",
                        "group": "Primary Coaching Behaviour"
                    },
        "Punishment / Scold" : {
                        "name": "Punishment / Scold",
                        "group": "Primary Coaching Behaviour"
                    },
        "Question Open" : {
                        "name": "Question Open",
                        "group": "Primary Coaching Behaviour"
                    },
        "Question Closed" : {
                        "name": "Question Closed",
                        "group": "Primary Coaching Behaviour"
                    },
        "Response to Question" : {
                        "name": "Response to Question",
                        "group": "Primary Coaching Behaviour"
                    },
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