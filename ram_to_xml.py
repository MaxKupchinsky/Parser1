from xml.dom.minidom import parse
from xml.dom.minidom import Element as md_element
from minidom_fixed import Document
#import minidom_fixed
from objects import Schema
from objects import Domain
from objects import Table
from objects import Field
from objects import Constraint
from objects import Index
from codecs import open

def ram_to_xml(schemas):
    if schemas is None:
        raise ValueError("Schemas is None")
    xml = Document()

    for schema in schemas:
        xml_schema =_print_xml_schema(schema,xml)
        xml.appendChild(xml_schema)

        xml_schema.appendChild(xml.createElement("custom"))

        xml_domains = xml.createElement("domains")
        xml_schema.appendChild(xml_domains)
        for domain in schema.domains:
            xml_domain = _print_xml_domain(domain,xml)
            xml_domains.appendChild(xml_domain)
        # переделать
        xml.writexml(open("Materials\\q.xml", 'w', 'utf-8'), '', '  ', '\n', 'utf-8')

    return xml


def _print_xml_schema(schema: Schema, xml: Document):
    xml_schema = xml.createElement("dbd_schema")
    if schema.fulltext_engine is not None:
        xml_schema.setAttribute("fulltext_engine", schema.fulltext_engine)
    if schema.version is not None:
        xml_schema.setAttribute("version", schema.version)
    if schema.name is not None:
        xml_schema.setAttribute("name", schema.name)
    if schema.description is not None:
        xml_schema.setAttribute("description", schema.description)
    return xml_schema


def _print_xml_domain(domain: Domain, xml: Document):
    xml_domain = xml.createElement("domain")

    if domain.name is not None:
        xml_domain.setAttribute('name', domain.name)
    if domain.description is not None:
        xml_domain.setAttribute('description', domain.description)
    if domain.type is not None:
        xml_domain.setAttribute('type', domain.type)
    if domain.align is not None:
        xml_domain.setAttribute('align', domain.align)
    if domain.width is not None:
        xml_domain.setAttribute('width', domain.width)
    if domain.length is not None:
        xml_domain.setAttribute('length', domain.length)
    if domain.precision is not None:
        xml_domain.setAttribute('precision', domain.precision)

    props = []
    if domain.prop_case_sensitive:
        props.append('case_sensitive')
    if domain.prop_show_null:
        props.append('show_null')
    if domain.prop_show_lead_nulls:
        props.append('show_lead_nulls')
    if domain.prop_thousands_separator:
        props.append('thousands_separator')
    if domain.prop_summable:
        props.append('summable')
    if len(props) > 0:
        xml_domain.setAttribute('props', ', '.join(props))

    if domain.scale:
        xml_domain.setAttribute('scale', domain.scale)
    if domain.char_length:
        xml_domain.setAttribute('char_length', domain.char_length)
    return xml_domain
