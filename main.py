from xml.dom.minidom import parse
from xml.dom.minidom import Element as md_element
from minidom_fixed import *
from objects import *


def nn(title, val):
    if val is not (None):
        return title + " " + str(val)
    else:
        return ""


def _get_schema(dom):  # переделать
    schemas = []
    dom_schema = dom.getElementsByTagName("dbd_schema")
    for schema in dom_schema:
        tmp_schema = Schema()
        for attr_name, attr_val in schema.attributes.items():
            if attr_name == "fulltext_engine":
                tmp_schema.fulltext_engine = attr_val
            elif attr_name == "version":
                tmp_schema.version = attr_val
            elif attr_name == "name":
                tmp_schema.name = attr_val
            elif attr_name == "description":
                tmp_schema.description = attr_val

        for child in schema.childNodes:
            if isinstance(child, md_element):
                if child.nodeName == "domains":
                    tmp_schema.domains = _get_domains(child)
                elif child.tagName == "tables":
                    tmp_schema.tables = _get_tables(child)
        schemas.append(tmp_schema)
    return schemas


def _print_schema(schemas):
    print("SCHEMA")
    t = 0
    for schema in schemas:
        t += 1
        print(str(t) + nn(" fulltext_engine =", schema.fulltext_engine)
        + nn(", version =", schema.version)
        + nn(", name =", schema.name)
        + nn(", description =", schema.description))
        print()
        _print_domains(schema.domains)
        _print_tables(schema.tables)
    print()

def _get_domains(dom_domains):
    domains =[]
    for domain in dom_domains.childNodes:
        if isinstance(domain, md_element):
            tmp_domain = Domain()
            for attr_name, attr_val in domain.attributes.items():
                if attr_name == "name":
                    tmp_domain.name = attr_val
                elif attr_name == "description":
                    tmp_domain.description = attr_val
                elif attr_name == "type":
                    tmp_domain.type = attr_val
                elif attr_name == "data_type_id":
                    tmp_domain.data_type_id = attr_val
                elif attr_name == "length":
                    tmp_domain.length = attr_val
                elif attr_name == "char_length":
                    tmp_domain.char_length = attr_val
                elif attr_name == "precision":
                    tmp_domain.precision = attr_val
                elif attr_name == "scale":
                    tmp_domain.scale = attr_val
                elif attr_name == "width":
                    tmp_domain.width = attr_val
                elif attr_name == "align":
                    tmp_domain.align = attr_val
                elif attr_name == "props":
                    for prop in attr_val.split(', '):
                        if prop == "show_null":
                            tmp_domain.prop_show_null = True
                        elif prop == "show_lead_nulls":
                            tmp_domain.prop_show_lead_nulls = True
                        elif prop == "thousands_separator":
                            tmp_domain.prop_thousands_separator = True
                        elif prop == "summable":
                            tmp_domain.prop_summable = True
                        elif prop == "case_sensitive":
                            tmp_domain.prop_case_sensitive = True
            domains.append(tmp_domain)
    return domains

def _print_domains(domains):
    t = 0
    print("DOMAINS")
    for domain in domains:
        t += 1
        print(str(t) + nn(", name =", domain.name)
            + nn(", description =", domain.description)
            + nn(", type =", domain.type)
            + nn(", data_type_id =", domain.data_type_id)
            + nn(", length =", domain.length)
            + nn(", char_length =", domain.char_length)
            + nn(", precision =", domain.precision)
            + nn(", scale =", domain.scale)
            + nn(", width =", domain.width)
            + nn(", align =", domain.align)

            + nn(", show_null", domain.prop_show_null)
            + nn(", show_lead_nulls =", domain.prop_show_lead_nulls)
            + nn(", thousands_separator =", domain.prop_thousands_separator)
            + nn(", summable =", domain.prop_summable)
            + nn(", case_sensitive =", domain.prop_case_sensitive))
    print()

def _get_tables(dom_tables):
    tables =[]
    for table in dom_tables.childNodes:
        if isinstance(table, md_element):
            tmp_table = Table()
            for attr_name, attr_val in table.attributes.items():
                if attr_name == "name":
                    tmp_table.name = attr_val
                elif attr_name == "description":
                    tmp_table.description = attr_val
                elif attr_name == "temporal_mode":
                    tmp_table.temporal_mode = attr_val
                elif attr_name == "means":
                    tmp_table.means = attr_val
                elif attr_name == "props":
                    for prop in attr_val.split(', '):
                        if prop == "add":
                            tmp_table.prop_add = True
                        elif prop == "edit":
                            tmp_table.prop_edit = True
                        elif prop == "delete":
                            tmp_table.prop_delete = True
            tables.append(tmp_table)
    return tables

def _print_tables(tables):
    t = 0
    print("TABLES")
    for table in tables:
        t += 1
        print(str(t) + nn(", name =", table.name)
              + nn(", description =", table.description)
              + nn(", temporal_mode =", table.temporal_mode)
              + nn(", means =", table.means)
              + nn(", prop_add =", table.prop_add)
              + nn(", prop_edit =", table.prop_edit)
              + nn(", prop_delete =", table.prop_delete))
    print()

def _get_fields(dom):
    return None

dom = parse("Materials\\tasks.xml")
dom.normalize()
_print_schema(_get_schema(dom))
#_get_domains(dom)
#_print_domains(_get_domains(dom))
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