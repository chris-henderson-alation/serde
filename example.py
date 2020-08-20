from definitions import *

import re


class Rectangle(Deserialize):
    def __new__(self, typeTarget, length, width):
        return ArrayOf(ArrayOf(typeTarget, width), length)


class Square(Deserialize):
    def __new__(self, typeTarget, length):
        return Rectangle(typeTarget, length, length)

class ChessBoard(Square(u8, 8)):
    pass

class SSN(String):
    @classmethod
    def validate(cls, ssn):
        if not re.match("\d{3}-\d{2}-\d{4}", ssn):
            raise Exception("not a social security number!")

class Name(String):
    @classmethod
    def validate(cls, name):
        if len(name) > 256:
            raise Exception("this may be culturaly insenstive, but that name is just too long for our database to handle")

class Person(Deserialize):

    name = Name
    age = u8 # After-all no is over 255 and no is under 0, right?
    ssn = SSN.optional() # This is an internationl competition, so not everyone is going to have a US SSN.


class Player(Person):

    emergencyContacts = ArrayOf(Person, length=2)

Player.deserialize("""
{
    "name": "Alice",
    "age": 34,
    "emergencyContacts": [{
        "name": "Bob",
        "age": 38,
        "ssn": "123-45-6789"
    }, {
        "name": "Eve",
        "age": 36,
        "ssn": "123-45-6788"
    }]
}
""")

class Game(Deserialize):

    playerOne = Player
    playerTwo = Player
    board = ChessBoard

print(Square(u8, 3).deserialize('[[1, 2, 3], [3, 4,3], [5, 6,3]]'))
print(ChessBoard.deserialize("""[
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8],
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8], 
    [1, 2, 3, 4, 5, 6, 7, 8]
]"""))
# print(LimitedLength.deserialize('[1,2,3,4,5]'))


# print(UnsignedByte.deserialize("1"))
# print(UnsignedByte.deserialize("255"))

class Column(Deserialize):

    type = String # this would be an enum but you get the point.
    name = String
    comments = String.optional()

class Table(Deserialize):

    name = String
    columns = ArrayOf(Column)
    comments = String.optional()

class StoredProcedure(Deserialize):

    code = String
    comments = String.optional()

class Schema(Deserialize):

    name = String
    tables = ArrayOf(Table)
    procedures = ArrayOf(StoredProcedure).optional()
    # comments = String.option(required=False)
    comments = String.optional()

class Database(Deserialize):

    schemas = ArrayOf(Schema)
    fp_groups = ArrayOf(ArrayOf(Integer))

database = '''
{
    "fp_groups": [[1,2,3,4], [5,6,7,8], 9],
    "schemas": [
        {
            "name": "Healthcare",
            "tables": [
                {
                    "name": "Dentists",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                },
                {
                    "name": "MDs",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Alation",
            "procedures": [
                {
                    "code": "SELECT * FROM Winning",
                    "comment": "Documented code is best code"
                },
                {
                    "code": "SELECT revenue, growth FROM SalesProjections"
                }
            ],
            "tables": [
                {
                    "name": "Engineering",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                },
                {
                    "name": "SalesProjections",
                    "columns": [
                        {
                            "name": "revenue",
                            "type": "float",
                            "comment": "secret"
                        },
                        {
                            "name": "growth",
                            "type": "float"
                        }
                    ]
                }
            ]
        }
    ]
}

'''

# try:
#     print(Database.deserialize(database).schemas[1].procedures[0].code)
# except Exception as e:
#     print(e)

