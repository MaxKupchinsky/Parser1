from minidom_fixed import Document
from minidom_fixed import Element
from objects import Schema
from objects import Domain
from objects import Table
from objects import Field
from objects import Constraint
from objects import Index
from codecs import open


def ram_to_xml(schemas, path: str):
    if schemas is None:
        raise ValueError("Schema is None")
    xml = Document()
    for schema in schemas:
        xml_schema = _print_xml_schema(schema,xml)
        xml.appendChild(xml_schema)

        xml_schema.appendChild(xml.createElement("custom"))

        xml_domains = xml.createElement("domains")
        xml_schema.appendChild(xml_domains)
        for domain in schema.domains:
            xml_domain = _print_xml_domain(domain,xml)
            xml_domains.appendChild(xml_domain)

        xml_tables = xml.createElement("tables")
        xml_schema.appendChild(xml_tables)
        for table in schema.tables:
            xml_table = _print_xml_table(table,xml)
            xml_tables.appendChild(xml_table)

            for field in table.fields:
                xml_field = _print_xml_field(field, xml)
                xml_table.appendChild(xml_field)

            for constraint in table.constraints:
                xml_constraint = _print_xml_constraint(constraint, xml)
                xml_table.appendChild(xml_constraint)

            for index in table.indexes:
                xml_index = _print_xml_index(index, xml)
                xml_table.appendChild(xml_index)

        xml.writexml(open(path, 'w', 'utf-8'), '', '  ', '\n', 'utf-8')

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

    if domain.scale is not None:
        xml_domain.setAttribute('scale', domain.scale)
    if domain.char_length is not None:
        xml_domain.setAttribute('char_length', domain.char_length)
    return xml_domain


def _print_xml_table(table: Table, xml: Document):
    xml_table = xml.createElement("table")

    if table.name is not None:
        xml_table.setAttribute('name', table.name)
    if table.description is not None:
        xml_table.setAttribute('description', table.description)

    props = []
    if table.prop_add:
        props.append('add')
    if table.prop_edit:
        props.append('edit')
    if table.prop_delete:
        props.append('delete')
    if len(props) > 0:
        xml_table.setAttribute('props', ', '.join(props))

    if table.temporal_mode is not None:
        xml_table.setAttribute('temporal_mode', table.temporal_mode)
    if table.means is not None:
        xml_table.setAttribute('means', table.means)
    return xml_table


def _print_xml_field(field: Field, xml: Document):
    xml_field = xml.createElement("field")

    if field.name is not None:
        xml_field.setAttribute('name', field.name)
    if field.rname is not None:
        xml_field.setAttribute('rname', field.rname)
    if field.domain is not None:
        xml_field.setAttribute('domain', field.domain)
    if field.type is not None:
        xml_field.setAttribute('type', field.type)
    if field.description is not None:
        xml_field.setAttribute('description', field.description)

    props = []
    if field.prop_input:
        props.append('input')
    if field.prop_edit:
        props.append('edit')
    if field.prop_show_in_grid:
        props.append('show_in_grid')
    if field.prop_show_in_details:
        props.append('show_in_details')
    if field.prop_is_mean:
        props.append('is_mean')
    if field.prop_autocalculated:
        props.append('autocalculated')
    if field.prop_required:
        props.append('required')
    if len(props) > 0:
        xml_field.setAttribute('props', ', '.join(props))
    return xml_field


def _print_xml_constraint(constraint: Constraint, xml: Document):
    xml_constraint = xml.createElement("constraint")

    if constraint.name is not None:
        xml_constraint.setAttribute('name', constraint.name)
    if constraint.kind is not None:
        xml_constraint.setAttribute('kind', constraint.kind)
    if len(constraint.details) > 0:
        xml_constraint.setAttribute('items', ', '.join(constraint.details))
    if constraint.reference is not None:
        xml_constraint.setAttribute('reference', constraint.reference)
    if constraint.expression is not None:
        xml_constraint.setAttribute('expression', constraint.expression)

    props = []
    if constraint.prop_has_value_edit:
        props.append('has_value_edit')
    if constraint.prop_cascading_delete:
        props.append('cascading_delete')
    if constraint.prop_full_cascading_delete:
        props.append('full_cascading_delete')
    if len(props) > 0:
        xml_constraint.setAttribute('props', ', '.join(props))
    return xml_constraint


def _print_xml_index(index: Index, xml: Document):
    xml_index = xml.createElement("index")

    if index.name:
        xml_index.setAttribute('name', index.name)
    if len(index.details) > 0:
        xml_index.setAttribute('field', ', '.join(index.details))

    props = []
    if index.prop_local:
        props.append('local')
    if index.prop_uniqueness:
        props.append('uniqueness')
    if index.prop_fulltext:
        props.append('fulltext')
    if len(props) > 0:
        xml_index.setAttribute('props', ', '.join(props))

    return xml_index

