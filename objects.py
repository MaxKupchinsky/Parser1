class Schema:
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.description = None

        self.domains = []
        self.tables = []

class Domain:
    def __init__(self):
        self.name = None
        self.description = None
        self.type = None
        self.length = None
        self.char_length = None
        self.precision = None
        self.scale = None
        self.width = None
        self.align = None

        self.prop_show_null = False
        self.prop_show_lead_nulls = False
        self.prop_thousands_separator = False
        self.prop_summable = False
        self.prop_case_sensitive = False

class Table:
    def __init__(self):
        self.name = None
        self.description = None
        self.temporal_mode = None
        self.means = None

        self.prop_add = False
        self.prop_edit = False
        self.prop_delete = False

        self.fields = []
        self.constraints = []
        self.indexes = []

class Constraint:
    def __init__(self):
        self.name = None
        self.kind = None
        self.reference = None
        self.expression = None

        self.prop_has_value_edit = False
        self.prop_cascading_delete = False
        self.prop_full_cascading_delete = False

        self.details = []  # items

class ConstraintDetail:
    def __init__(self):
        self.detail = None

class Index:
    def __init__(self):
        self.name = None
        self.kind = None  # зависит от prop

        self.prop_local = False
        self.prop_uniqueness = False
        self.prop_fulltext = False

        self.details = []  # field

class IndexDetail:
    def __init__(self):
        self.detail = None
        self.expression = None
        self.descend = None

class Field:
    def __init__(self):
        self.name = None
        self.rname = None
        self.description = None
        self.domain = None
        self.type = None

        self.prop_input = False
        self.prop_edit = False
        self.prop_show_in_grid = False
        self.prop_show_in_details = False
        self.prop_is_mean = False
        self.prop_autocalculated = False
        self.prop_required = False