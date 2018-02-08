from xml.dom.minidom import parse
from xml.dom.minidom import Element as md_element
from minidom_fixed import *
from xml_to_ram import xml_to_ram
from ram_to_xml import *
from test_xml_ram import test


if __name__ == "__main__":
    try:
        test('Materials\\tasks.xml', 'Materials\\tasks1.xml')
        test('Materials\\prjadm.xdb.xml', 'Materials\\prjadm1.xml')
    except Exception as e:
        print(e)
    #ram_to_xml(xml_to_ram(dom), "Materials\\q.xml")


"""
_domain = dom.getElementsByTagName("domains")[0]
for child in _domain.childNodes:
    if isinstance(child, mdElement):
        print(child.nodeName)
"""

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