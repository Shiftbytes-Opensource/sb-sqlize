import sys
sys.path.append('../')
from sqlize import Sqlize

s = Sqlize()

s.create_table({
    "name": "user",
    "attributes": [
        {
            "name" : "id",
            "type" :"string",
            "unique": True,
            "nullable" : False
        },
        {
            "name" : "name",
            "type" : "string",
            "unique": False,
            "nullable" : False
        },
        {
            "name" : "age",
            "type" : "string",
            "nullable" : True,
            "unique" : False
        }
        ]
})

print("create_table")
