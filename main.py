from xml.dom.minidom import parse
from xml.dom.minidom import Element as mdElement
from minidom_fixed import *
from objects import *

dom = parse("Materials\\tasks.xml")
dom.normalize()

schema = Schema()
_schema = dom.documentElement

for attr_name, attr_val in _schema.attributes.items():
    if attr_name == "fulltext_engine":
        schema.fulltext_engine = attr_val


"""
node1=dom.getElementsByTagName("node1")[0]
print("<node1 attr=\"str\">TestNode</node1>")
print("name="+node1.nodeName)
print("attr="+node1.getAttribute("attr"))
print("attr="+node1.attributes.item(0).value)
print("value="+node1.childNodes[0].nodeValue)
print("\n")

for child in dom.getElementsByTagName("array"):
    for ch in child.childNodes:
        if isinstance(ch, mdElement):
            print(ch.nodeName)
            #print(ch.attributes.item(0).value)
            if ch.getAttribute("field") != "":
                print(ch.getAttribute("field"))
            #print(ch.childNodes[0].nodeValue)
    print("-----------------\n")
"""