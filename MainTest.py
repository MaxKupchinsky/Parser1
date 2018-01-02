from xml.dom import minidom
from xml.dom.minidom import Element

dom = minidom.parse("test.xml")
dom.normalize()

node1=dom.getElementsByTagName("node1")[0]
print("<node1 attr=\"str\">TestNode</node1>")
print("name="+node1.nodeName)
print("attr="+node1.getAttribute("attr"))
print("attr="+node1.attributes.item(0).value)
print("value="+node1.childNodes[0].nodeValue)
print("\n")

# """
for child in dom.getElementsByTagName("array"):
    for ch in child.childNodes:
        if isinstance(ch, Element):
            print(ch.nodeName)
            #print(ch.attributes.item(0).value)
            if ch.getAttribute("field") != "":
                print(ch.getAttribute("field"))
            #print(ch.childNodes[0].nodeValue)
    print("-----------------\n")

#"""