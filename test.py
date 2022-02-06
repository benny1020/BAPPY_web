import json

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

class test():
    def __init__(self):
        self.a='a'
        self.b='b'
        self.c=["abc","asd","sdd"]

t = []

t1 = test()
t2 = test()
t.append(dumper(t1))
t.append(dumper(t2))

print(t)
print(t[0]['c'][0])

print(json.dumps(t))
