from definitions import *

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

try:
    print(Database.deserialize(database).schemas[1].procedures[0].code)
except Exception as e:
    print(e)


