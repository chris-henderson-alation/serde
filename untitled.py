import json
import inspect
import pprint

class Deserialize(object):

	# Try to keep the black magic to this one class.

	pp = pprint.PrettyPrinter(indent=2)	
	required = True

	@classmethod
	def option(cls, required=True):
		suffix = "Required" if required else "NotRequired"
		return type("{}{}".format(cls.__name__, suffix), (cls, ), {
			"required": required
			})

	@classmethod
	def deserialize(cls, raw):
		if isinstance(raw, str):
			raw = json.loads(raw)
		elif hasattr(raw, 'read') and callable(getattr(raw, 'read')):
			raw = json.load(raw)
		if isinstance(raw, dict):
			return cls.deser_dict(raw)
		elif isinstance(raw, list):
			if not issubclass(cls, ArrayOf):
				raise Exception("expected type {}, got an array".format(cls.__name__))
			return [cls.Type.deserialize(v) for v in raw]
		

	@classmethod
	def deser_dict(cls, raw):
		obj = cls()
		for k, v in cls.__dict__.items():
			if not inspect.isclass(v) or not issubclass(v, Deserialize):
				continue
			if k in raw:
				obj.__setattr__(k,  v.deserialize(raw[k]))
			elif not v.required:
				obj.__setattr__(k,  None)
			else:
				raise Exception("expected member {}".format(k))
		return obj


class Primitive(Deserialize):

	@classmethod
	def typeCheck(cls, terminal):
		return isinstance(terminal, cls.Type) or not cls.required and terminal is None

	@classmethod
	def deserialize(cls, terminal):
		if cls.typeCheck(terminal):
			return terminal
		raise Exception("wrong type: got {} want {}".format(terminal.__class__.__name__, cls.__name__, ))
	
class Integer(Primitive):
	Type = int

class String(Primitive):
	Type = str

class Float(Primitive):
	Type = float

class Boolean(Primitive):
	Type = bool

class ArrayOf(object):

	def __new__(self, target):
		return type(
			"ArrayOf<{}>".format(target.__name__ ), 
			(Deserialize, ArrayOf), 
			{"Type": target}
		)




class Column(Deserialize):

	type = String # this would be an enum but you get the point.
	name = String
	comments = String.option(required=False)

class Table(Deserialize):

	name = String
	columns = ArrayOf(Column)
	comments = String.option(required=False)

class StoredProcedure(Deserialize):

	code = String
	comments = String.option(required=False)	

class Schema(Deserialize):

	name = String
	tables = ArrayOf(Table)
	procedures = ArrayOf(StoredProcedure).option(required=False)
	comments = String.option(required=False)

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

print(Database.deserialize(database).schemas[1].procedures[0].code)