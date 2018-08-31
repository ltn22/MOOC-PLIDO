import CBOR as cbor

var1 = 100
var2 = 34.5
var3 = "off"
var4 = -3

j = {
  "max" : var1,
  "temp" : var2,
  "state" : var3,
  "delta" : var4
}

c = cbor.dumps(j)
print (c)
print ("CBOR Length:", c.length())
print ("CBOR Value:", c.value())

j2 = cbor.loads(c)
print (j2["temp"])
