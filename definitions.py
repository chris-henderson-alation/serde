import json
import inspect

class Deserialize(object):


    @classmethod
    def optional(cls):
        return type("Optional" + cls.__name__, (cls, Optional), {})

    @classmethod
    def deserialize(cls, raw):
        if isinstance(raw, str):
            raw = json.loads(raw)
        elif hasattr(raw, 'read') and callable(getattr(raw, 'read')):
            raw = json.load(raw)
        if isinstance(raw, dict):
            return cls.deserialize_dict(raw)
        elif isinstance(raw, list):
            if not issubclass(cls, ArrayOf):
                raise Exception("expected type {}, got an array".format(cls.__name__))
            return [cls.Type.deserialize(v) for v in raw]
        

    @classmethod
    def deserialize_dict(cls, raw):
        obj = cls()
        for k, v in cls.__dict__.items():
            if not inspect.isclass(v) or not issubclass(v, Deserialize):
                continue
            if k in raw:
                obj.__setattr__(k,  v.deserialize(raw[k]))
            elif issubclass(v, Optional):
                obj.__setattr__(k,  None)
            else:
                raise Exception("expected member {}".format(k))
        return obj

class Optional():
    pass

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

    @classmethod
    def typeCheck(cls, terminal):
        return isinstance(terminal, unicode) or Primitive.typeCheck(cls, terminal)

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
