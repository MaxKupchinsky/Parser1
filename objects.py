class Schema:
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

class Domain:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.type = None
        self.data_type_id = None
        self.length = None
        self.char_length = None
        self.precision = None
        self.scale = None
        self.width = None
        self.align = None
        self.show_null = None
        self.show_lead_nulls = None
        self.thousands_separator = None
        self.summable = None
        self.case_sensitive = None
        self.uuid = None

class Table:
    def __init__(self):
        self.id = None
        self.schema_id = None
        self.name = None
        self.description = None
        self.can_add = None
        self.can_edit = None
        self.can_delete = None
        self.temporal_mode = None
        self.means = None
        self.uuid = None

class Constraint:
    def __init__(self):
        self.id = None
        self.table_id = None
        self.name = None
        self.constraint_type = None
        self.reference = None
        self.unique_key_id = None
        self.has_value_edit = None
        self.cascading_delete = None
        self.expression = None
        self.uuid = None

class ConstraintDetail:
    def __init__(self):
        self.id = None
        self.constraint_id = None
        self.position = None
        self.field_id = None

class Index:
    def __init__(self):
        self.id = None
        self.table_id = None
        self.name = None
        self.local = None
        self.kind = None
        self.uuid = None

class IndexDetail:
    def __init__(self):
        self.id = None
        self.index_id = None
        self.position = None
        self.field_id = None
        self.expression = None
        self.descend = None

class Field:
    def __init__(self):
        self.id = None
        self.table_id = None
        self.position = None
        self.name = None
        self.russian_short_name = None
        self.description = None
        self.domain_id = None
        self.can_input = None
        self.can_edit = None
        self.show_in_grid = None
        self.show_in_details = None
        self.is_mean = None
        self.autocalculated = None
        self.required = None
        self.uuid = None