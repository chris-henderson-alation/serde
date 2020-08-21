# -*- coding: utf-8 -*-

from definitions import *

import re

import enum


class ChessPiece(u8):
    
    WhiteKing    = 1
    WhiteQueen   = 2
    WhiteRook    = 3
    WhiteBishop  = 4
    WhiteKnight  = 5
    WhitePawn    = 6
    BlackKing    = 7
    BlackQueen   = 8
    BlackRook    = 9
    BlackBishop  = 10
    BlackKnight  = 11
    BlackPawn    = 12
    Empty        = 13

    asString = {
        WhiteKing  :  '♔',
        WhiteQueen :  '♕',
        WhiteRook  :  '♖',
        WhiteBishop:  '♗',
        WhiteKnight:  '♘',
        WhitePawn  :  '♙',
        BlackKing  :  '♚',
        BlackQueen :  '♛',
        BlackRook  :  '♜',
        BlackBishop:  '♝',
        BlackKnight:  '♞',
        BlackPawn  :  '♟',
        Empty      :  ' ',
    }

    @classmethod
    def deserialize(cls, piece):
        piece = super(u8, cls).deserialize(piece)
        return cls.asString.get(piece, str(piece))

    @classmethod
    def validate(cls, piece):
        if piece not in cls.asString:
            raise Exception("{} is not a chess piece!".format(piece))

class Rectangle(Deserialize):
    def __new__(self, typeTarget, length, width):
        return ArrayOf(ArrayOf(typeTarget, length), width)


class Square(Deserialize):
    def __new__(self, typeTarget, length):
        return Rectangle(typeTarget, length, length)


class ChessBoard(Square(ChessPiece, 8)):
    pass

class SSN(String):
    @classmethod
    def validate(cls, ssn):
        if not re.match("^\d{3}-\d{2}-\d{4}$", ssn):
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
    nation = String.optional()

    class record(Deserialize):
        wins = u32.default(0)
        losses = u32.default(0)

class Game(Deserialize):

    playerOne = Player
    playerTwo = Player
    board = ChessBoard
    audience = ArrayOf(Person).default([])

game = """
{
    "playerOne": {
        "name": "Alice",
        "age": 34,
        "nation": "Chessoslovakia",
        "emergencyContacts": [
            {
                "name": "Bob",
                "age": 38
            }, 
            {
                "name": "Gertrude",
                "age": 36,
                "ssn": "123-45-6788"
            }
        ],
        "record": {
            "wins": 42
        }
    },
    "playerTwo": {
        "name": "Eve",
        "age": 34,
        "emergencyContacts": [
            {
                "name": "Pauline",
                "age": 26
            }, 
            {
                "name": "Geno",
                "age": 21,
                "ssn": "896-72-1543"
            }
        ],
        "record": {
            "losses": 42
        }
    },
    "board": [
        [9, 11, 10, 7, 8, 10, 11, 9],
        [12, 12, 12, 12, 12, 12, 12, 12],
        [13, 13, 13, 13, 13, 13, 13, 13],
        [13, 13, 13, 13, 13, 13, 13, 13],
        [13, 13, 13, 13, 13, 13, 13, 13],
        [13, 13, 13, 13, 13, 13, 13, 13],
        [6, 6, 6, 6, 6, 6, 6, 6], 
        [3, 5, 4, 1, 2, 4, 5, 3]
    ]
}
"""

try:
    Game.deserialize(game)
except Exception as e:
    print(e)

# Player.deserialize("""
# {
#     "name": "Alice",
#     "age": 34,
#     "nation": "Chessoslovakia",
#     "emergencyContacts": [
#         {
#             "name": "Bob",
#             "age": 38
#         }, 
#         {
#             "name": "Gertrude",
#             "age": 36,
#             "ssn": "123-45-6788"
#         }
#     ],
#     "record": {
#         "wins": 42
#     }
# }
# """)

# Player.deserialize("""
# {
#     "name": "Eve",
#     "age": 34,
#     "emergencyContacts": [
#         {
#             "name": "Pauline",
#             "age": 26
#         }, 
#         {
#             "name": "Geno",
#             "age": 21,
#             "ssn": "896-72-1543"
#         }
#     ],
#     "record": {
#         "losses": 42
#     }
# }
# """)

# print(ChessBoard.deserialize("""[
#     [9, 11, 10, 7, 8, 10, 11, 9],
#     [12, 12, 12, 12, 12, 12, 12, 12],
#     [13, 13, 13, 13, 13, 13, 13, 13],
#     [13, 13, 13, 13, 13, 13, 13, 13],
#     [13, 13, 13, 13, 13, 13, 13, 13],
#     [13, 13, 13, 13, 13, 13, 13, 13],
#     [6, 6, 6, 6, 6, 6, 6, 6], 
#     [3, 5, 4, 1, 2, 4, 5, 3]
# ]"""))




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

