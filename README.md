# ida-netnode
Humane API for storing and accessing persistent data in IDA Pro databases

# example:
```
n = netnode.Netnode("$ some.namespace")

# treat the netnode like a persistent dictionary:
n["key 1"] = "A"
n["key 2"] = "B"
print(n["key 1"]) --> "A"
print(n["key 2"]) --> "B"

# including the iteration APIs:
print(n.keys())     --> ["key 1", "key 2"]
print(n.values())   --> ["A", "B"]
print(n.items())    --> [("key 1", "A"), ("key 2", "B")]
print("key 1" in n) --> True

# store large amounts of data in a single value:
n["some key"] = "A" * 4096
print(n["some key"]) --> "AAAAAAA..."
```