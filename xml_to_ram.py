from xml.dom.minidom import parse
from xml.dom.minidom import Element as md_element
from minidom_fixed import *
from objects import Schema
from objects import Domain
from objects import Table
from objects import Field
from objects import Constraint
from objects import Index


def xml_to_ram(path):
    try:
        dom = parse(path)
        dom.normalize()
    except Exception:
        print("xml parse exception")
    return _get_schema(dom)


def _get_schema(dom):  # переделать
    schemas = []
    try:
        dom_schema = dom.getElementsByTagName("dbd_schema")
        if dom_schema == []:
            raise Exception("Schema not found")
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
                else:
                    raise Exception("Unknown schema attribute: " + attr_name)

            for child in schema.childNodes:
                if isinstance(child, md_element):
                    if child.nodeName == "domains":
                        tmp_schema.domains = _get_domains(child)
                    elif child.tagName == "tables":
                        tmp_schema.tables = _get_tables(child)
        schemas.append(tmp_schema)
    except Exception as e:
        print(e)
    return schemas


def _get_domains(dom_domains):
    domains =[]
    try:
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
                            else:
                                raise Exception("Unknown domain prop:"+prop)
                    else:
                        raise Exception("Unknown domain attribute:" + attr_name)
                domains.append(tmp_domain)
    except Exception as e:
        print(e)
    return domains


def _get_tables(dom_tables):
    tables =[]
    try:
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
                            else:
                                raise Exception("Unknown table prop:"+prop)
                    else:
                        Exception("Unknown table attribute:" + attr_name)

                for child in table.childNodes:
                    if isinstance(child, md_element):
                        if child.nodeName == "field":
                            tmp_table.fields.append(_get_fields(child))

                for child in table.childNodes:
                    if isinstance(child, md_element):
                        if child.nodeName == "field":
                            continue
                        elif child.nodeName == "constraint":
                            tmp_table.constraints.append(_get_constraints(child))
                        elif child.nodeName == "index":
                            tmp_table.indexes.append(_get_indexes(child))
                        else:
                            raise Exception("Unknown table child: " + child.nodeName
                                            + " in " + tmp_table.name)
                tables.append(tmp_table)
    except Exception as e:
        print(e)
    return tables


def _get_fields(dom_field):
    tmp_field = Field()
    try:
        for attr_name, attr_val in dom_field.attributes.items():
            if attr_name == "name":
                tmp_field.name = attr_val
            elif attr_name == "rname":
                tmp_field.rname = attr_val
            elif attr_name == "description":
                tmp_field.description = attr_val
            elif attr_name == "domain":
                tmp_field.domain = attr_val
            elif attr_name == "type":
                tmp_field.type = attr_val
            elif attr_name == "props":
                for prop in attr_val.split(', '):
                    if prop == "input":
                        tmp_field.prop_input = True
                    elif prop == "edit":
                        tmp_field.prop_edit = True
                    elif prop == "show_in_grid":
                        tmp_field.prop_show_in_grid = True
                    elif prop == "show_in_details":
                        tmp_field.prop_show_in_details = True
                    elif prop == "is_mean":
                        tmp_field.prop_is_mean = True
                    elif prop == "autocalculated":
                        tmp_field.prop_autocalculated = True
                    elif prop == "required":
                        tmp_field.prop_required = True
                    else:
                        raise Exception("Unknown field prop:" + prop)
            else:
                raise Exception("Unknown field attribute:" + attr_name)
    except Exception as e:
        print(e)
    return tmp_field


def _get_constraints(dom_constraint):
    tmp_constraint = Constraint()
    try:
        for attr_name, attr_val in dom_constraint.attributes.items():
            if attr_name == "name":
                tmp_constraint.name = attr_val
            elif attr_name == "kind":
                tmp_constraint.kind = attr_val
            elif attr_name == "reference":
                tmp_constraint.reference = attr_val
            elif attr_name == "expression":
                tmp_constraint.expression = attr_val
            elif attr_name == "props":
                for prop in attr_val.split(', '):
                    if prop == "has_value_edit":
                        tmp_constraint.prop_has_value_edit = True
                    elif prop == "cascading_delete":
                        tmp_constraint.prop_cascading_delete = True
                    elif prop == "full_cascading_delete":
                        tmp_constraint.prop_full_cascading_delete = True
                    else:
                        raise Exception("Unknown constraint prop:" + prop)
            elif attr_name == "items":
                for detail in attr_val.split(', '):
                    tmp_constraint.details.append(detail);
            else:
                raise Exception("Unknown constraint attribute:" + attr_name)
    except Exception as e:
        print(e)
    return tmp_constraint


def _get_indexes(dom_index):
    tmp_index = Index()
    try:
        for attr_name, attr_val in dom_index.attributes.items():
            if attr_name == "name":
                tmp_index.name = attr_val
            elif attr_name == "kind":
                tmp_index.kind = attr_val
            elif attr_name == "props":
                for prop in attr_val.split(', '):
                    if prop == "local":
                        tmp_index.prop_local = True
                    elif prop == "uniqueness":
                        tmp_index.prop_uniqueness = True
                    elif prop == "fulltext":
                        tmp_index.prop_fulltext = True
                    else:
                        raise Exception("Unknown index prop:" + prop)
            elif attr_name == "field":
                for detail in attr_val.split(', '):
                    tmp_index.details.append(detail);
            else:
                raise Exception("Unknown index attribute:" + attr_name)
    except Exception as e:
        print(e)
    return tmp_index
