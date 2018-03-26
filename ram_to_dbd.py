import sqlite3
from dbd_const import *
import uuid


def ram_to_dbd(schemas, path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.executescript(SQL_DBD_Init)
    connection.commit()

    for schema in schemas:
        _add_domains(schema, cursor, connection)
        #_add_tables(schema, cursor, connection)
        #_add_fields(schema, cursor, connection)
        #_add_indexes(schema, cursor, connection)
       # _add_constraints(schema, cursor, connection)


    #connection.commit()
    connection.close()


def check(val):
    if val == "" or val is None:
        return ""
    else:
        return val

def _add_domains(schemas, cursor, connection):

        Q_INSERT_DOMAIN = """
            INSERT INTO dbd$domains (
                name,
                description,
                data_type_id,
                length,
                char_length,
                precision,
                scale,
                width,
                align,
                show_null,
                show_lead_nulls,
                thousands_separator,
                summable,
                case_sensitive,
                uuid)
            VALUES (?, ?, (SELECT id FROM dbd$data_types WHERE type_id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            """

        Q_CREATE_DOMAINS = """
            CREATE TEMP TABLE temp_domains (
                id  integer primary key autoincrement default(null),
                name varchar unique default(null),  
                description varchar default(null), 
                data_type_id integer not null,      
                length integer default(null),      
                char_length integer default(null),  
                precision integer default(null),    
                scale integer default(null),        
                width integer default(null),        
                align char default(null),           
                show_null boolean default(null),    
                show_lead_nulls boolean default(null),      
                thousands_separator boolean default(null),  
                summable boolean default(null),             
                case_sensitive boolean default(null),  
                uuid varchar unique not null   
            );
            """

        Q_INSERT_TEMP_DOMAIN = """
                INSERT INTO temp_domains (
                    name,
                    description,
                    data_type_id,
                    length,
                    char_length,
                    precision,
                    scale,
                    width,
                    align,
                    show_null,
                    show_lead_nulls,
                    thousands_separator,
                    summable,
                    case_sensitive,
                    uuid)
                VALUES (?, ?, (SELECT id FROM dbd$data_types WHERE type_id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

        Q_RELEASE_DOMAINS = """
                INSERT INTO dbd$domains (
                    name,
                    description,
                    data_type_id,
                    length,
                    char_length,
                    precision,
                    scale,
                    width,
                    align,
                    show_null,
                    show_lead_nulls,
                    thousands_separator,
                    summable,
                    case_sensitive,
                    uuid
                )
                SELECT DISTINCT
                    name,
                    description,
                    data_type_id,
                    length,
                    char_length,
                    precision,
                    scale,
                    width,
                    align,
                    show_null,
                    show_lead_nulls,
                    thousands_separator,
                    summable,
                    case_sensitive,
                    uuid
                FROM temp_domains;
                """

        cursor.executescript(Q_CREATE_DOMAINS)

        for domain in schemas.domains:
            tmp_domain = ()
            tmp_domain += check(domain.name),
            tmp_domain += check(domain.description),
            tmp_domain += check(domain.type),
            tmp_domain += check(domain.length),
            tmp_domain += check(domain.char_length),
            tmp_domain += check(domain.precision),
            tmp_domain += check(domain.scale),
            tmp_domain += check(domain.width),
            tmp_domain += check(domain.align),
            tmp_domain += 'TRUE' if domain.prop_show_null else 'FALSE',
            tmp_domain += 'TRUE' if domain.prop_show_lead_nulls else 'FALSE',
            tmp_domain += 'TRUE' if domain.prop_thousands_separator else 'FALSE',
            tmp_domain += 'TRUE' if domain.prop_summable else 'FALSE',
            tmp_domain += 'TRUE' if domain.prop_case_sensitive else 'FALSE',
            tmp_domain += uuid.uuid1().hex,

            connection.execute(Q_INSERT_DOMAIN, tmp_domain)

        cursor.executescript(Q_RELEASE_DOMAINS)

def _add_tables(schemas, cursor, connection):

    Q_INSERT_TABLE = """
            INSERT INTO dbd$tables (
                schema_id,
                name,
                description,
                can_add,
                can_edit,
                can_delete,
                temporal_mode,
                means)
            VALUES (?, (SELECT id FROM dbd$schemas WHERE name = ?), ?, ?, ?, ?, ?, ?)
            """

    for table in schemas.tables:
        tmp_table = ()
        tmp_table +=schemas.name,
        tmp_table += check(table.name),
        tmp_table += check(table.description),
        tmp_table += 'TRUE' if table.prop_add else 'FALSE',
        tmp_table += 'TRUE' if table.prop_edit else 'FALSE',
        tmp_table += 'TRUE' if table.prop_delete else 'FALSE',
        tmp_table += check(table.temporal_mode),
        tmp_table += check(table.means),

        connection.execute(Q_INSERT_TABLE, tmp_table)


def _add_fields(schemas, cursor, connection):

        Q_CREATE_TMP_FIELDS = """
            DROP TABLE IF EXISTS temp_dbd$fields;
            CREATE TEMP TABLE temp_dbd$fields (
                id integer primary key autoincrement default(null),
                t_id varchar not null,
                position integer not null,
                name varchar not null,
                russian_short_name varchar not null,
                description varchar default(null),
                d_id varchar not null,
                can_input boolean default(null),
                can_edit boolean default(null),
                show_in_grid boolean default(null),
                show_in_details boolean default(null),
                is_mean boolean default(null),
                autocalculated boolean default(null),
                required boolean default(null)
            );
            """

        Q_INSERT_FIELD = """
            INSERT INTO temp_dbd$fields (
                t_id,
                position,
                name,
                russian_short_name,
                description,
                d_id,
                can_input,
                can_edit,
                show_in_grid,
                show_in_details,
                is_mean,
                autocalculated,
                required)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

        Q_RELEASE_FIELDS = """
            INSERT INTO dbd$fields (
                table_id,
                position,
                name,
                russian_short_name,
                description,
                domain_id,
                can_input,
                can_edit,
                show_in_grid,
                show_in_details,
                is_mean,
                autocalculated,
                required
             )
            SELECT
                dbd$tables.id table_id,
                temp_dbd$fields.position,
                temp_dbd$fields.name,
                temp_dbd$fields.russian_short_name,
                temp_dbd$fields.description,
                dbd$domains.id domain_id,
                temp_dbd$fields.can_input,
                temp_dbd$fields.can_edit,
                temp_dbd$fields.show_in_grid,
                temp_dbd$fields.show_in_details,
                temp_dbd$fields.is_mean,
                temp_dbd$fields.autocalculated,
                temp_dbd$fields.required
            FROM temp_dbd$fields
            INNER JOIN dbd$tables ON dbd$tables.name = temp_dbd$fields.t_id
            INNER JOIN dbd$domains ON dbd$domains.name = temp_dbd$fields.d_id
            """

        cursor.executescript(Q_CREATE_TMP_FIELDS)

        for table in schemas.tables:
            for field in table.fields:
                field_index = table.fields.index(field) + 1
                target_field = ()
                target_field += table.name,
                target_field += field_index,
                target_field += check(field.name),
                target_field += check(field.rname),
                target_field += check(field.description),
                target_field += check(field.name),

                target_field += 'TRUE' if field.prop_input else 'FALSE',
                target_field += 'TRUE' if field.prop_edit else 'FALSE',
                target_field += 'TRUE' if field.prop_show_in_grid else 'FALSE',
                target_field += 'TRUE' if field.prop_show_in_details else 'FALSE',
                target_field += 'TRUE' if field.prop_is_mean else 'FALSE',
                target_field += 'TRUE' if field.prop_autocalculated else 'FALSE',
                target_field += 'TRUE' if field.prop_required else 'FALSE',

                connection.execute(Q_INSERT_FIELD, target_field)

        cursor.executescript(Q_RELEASE_FIELDS)


def _add_indexes(schemas, cursor, connection):

    Q_CREATE_TMP_INDEXES = """
            DROP TABLE IF EXISTS temp_dbd$indexes;
            CREATE TEMP TABLE temp_dbd$indexes (
                id integer primary key autoincrement default(null),
                t_name varchar not null,
                name varchar default(null),
                local boolean default(0),
                kind char default(null)
            );
            """

    Q_CREATE_TMP_INDEXES_DETAILS = """
        DROP TABLE IF EXISTS temp_dbd$index_details;
        CREATE TEMP TABLE temp_dbd$index_details (
            id integer primary key autoincrement default(null),
            index_name varchar not null,
            position integer not null,
            field_name varchar default(null),
            expression varchar default(null),
            descend boolean default(null),
            tab_name varchar not null 
        )
        """

    Q_ADD_TMP_INDEX = """
        INSERT INTO temp_dbd$indexes (
            t_name,
            name,
            local,
            kind)
        VALUES (?, ?, ?, ?);
        """

    Q_ADD_TMP_INDEX_DETAIL = """
        INSERT INTO temp_dbd$index_details (
            index_name,
            position,
            field_name,
            expression,
            descend,
            tab_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """

    Q_RELEASE_INDEXES = """
        INSERT INTO dbd$indices
            SELECT
                null,
                dbd$tables.id table_id,
                temp_dbd$indexes.name,
                temp_dbd$indexes.local,
                temp_dbd$indexes.kind
            FROM temp_dbd$indexes
            LEFT JOIN dbd$tables ON temp_dbd$indexes.t_name = dbd$tables.name;

        INSERT INTO dbd$index_details
            SELECT
                null,
                temp_dbd$indexes.id,
                temp_dbd$index_details.position,
                dbd$fields.id,
                temp_dbd$index_details.expression,
                temp_dbd$index_details.descend
            FROM temp_dbd$index_details
            LEFT JOIN temp_dbd$indexes ON temp_dbd$index_details.index_name = temp_dbd$indexes.name
            LEFT JOIN dbd$tables ON temp_dbd$index_details.tab_name = dbd$tables.name
            LEFT JOIN dbd$fields ON (temp_dbd$index_details.field_name = dbd$fields.name) AND (dbd$fields.table_id = dbd$tables.id);
        """

    cursor.executescript(Q_CREATE_TMP_INDEXES)
    cursor.executescript(Q_CREATE_TMP_INDEXES_DETAILS)

    for table in schemas.tables:
        for index in table.indexes:

            tmp_index, target_index_detail = (), ()
            tmp_index += table.name,
            tmp_index += index.name,
            tmp_index += 'TRUE' if index.prop_local else 'FALSE',

            # Props
            if index.prop_uniqueness:
                tmp_index += 'U',
            elif index.prop_fulltext:
                tmp_index += 'T',
            else:
                tmp_index += '',

            cursor.execute(Q_ADD_TMP_INDEX, tmp_index)

            # Позиция индекса
            position = table.indexes.index(index) + 1

            target_index_detail += index.name,
            target_index_detail += position,
            target_index_detail += check(index.field),
            target_index_detail += check(index.expression),

            target_index_detail += 'TRUE' if index.descend is not None else 'FALSE',

            target_index_detail += check(table.name),

            cursor.execute(Q_ADD_TMP_INDEX_DETAIL, target_index_detail)

    # Заполняем таблицу dbd$indices и удаляем временные имена
    cursor.executescript(Q_RELEASE_INDEXES)

def _add_constraints(schemas, cursor, connection):

    Q_CREATE_TMP_CONSTRAINTS = """
            DROP TABLE IF EXISTS temp_dbd$constraints;
            CREATE TEMP TABLE temp_dbd$constraints (
                id integer primary key autoincrement default (null),
                table_name varchar not null,
                constraint_name varchar default(null),
                constraint_type char default(null),
                reference_name varchar default(null),
                unique_key_id integer default(null),
                has_value_edit boolean default(null),
                cascading_delete boolean default(null),
                expression varchar default(null)
            );
            """

    Q_CREATE_TMP_CONSTRAINT_DETAILS = """
            DROP TABLE IF EXISTS temp_dbd$constraint_details;
            CREATE TEMP TABLE temp_dbd$constraint_details (
                id integer primary key autoincrement default(null),
                constraint_name varchar not null,
                position integer not null,
                field_name varchar not null default(null),
                tab_name varchar not null
            );
            """

    Q_ADD_TMP_CONSTRAINT = """
            INSERT INTO temp_dbd$constraints (
                table_name,
                constraint_name,
                constraint_type,
                reference_name,
                unique_key_id,
                has_value_edit,
                cascading_delete,
                expression)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

    Q_ADD_TMP_CONSTRAINT_DETAIL = """
            INSERT INTO temp_dbd$constraint_details (
                constraint_name,
                position,
                field_name,
                tab_name)
            VALUES (?, ?, ?, ?);
            """

    Q_RELEASE_CONSTRAINTS = """
            INSERT INTO dbd$constraints
                SELECT
                null,
                table_id,
                constraint_name,
                constraint_type,
                dbd$tables.id reference_id,
                unique_key_id,
                has_value_edit,
                cascading_delete,
                expression
                FROM
                (SELECT
                    temp_dbd$constraints.id const_id,
                    dbd$tables.id table_id,
                    temp_dbd$constraints.constraint_name,
                    temp_dbd$constraints.constraint_type,
                    temp_dbd$constraints.reference_name,
                    temp_dbd$constraints.unique_key_id,
                    temp_dbd$constraints.has_value_edit,
                    temp_dbd$constraints.cascading_delete,
                    temp_dbd$constraints.expression
                FROM temp_dbd$constraints
                LEFT JOIN dbd$tables ON temp_dbd$constraints.table_name = dbd$tables.name)
                LEFT JOIN dbd$tables ON reference_name = dbd$tables.name;

            INSERT INTO dbd$constraint_details
            SELECT
                null,
                temp_dbd$constraints.id const_id,
                temp_dbd$constraint_details.position,
                dbd$fields.id field_id
            FROM temp_dbd$constraint_details
            LEFT JOIN temp_dbd$constraints ON temp_dbd$constraint_details.constraint_name = temp_dbd$constraints.constraint_name
            LEFT JOIN dbd$tables ON temp_dbd$constraint_details.tab_name = dbd$tables.name
            LEFT JOIN dbd$fields ON (temp_dbd$constraint_details.field_name = dbd$fields.name) AND (dbd$fields.table_id = dbd$tables.id)
            """

    DELETE_TEMP_CONSTRAINTS_NAMES = """
                UPDATE dbd$constraints
                SET name=NULL
                WHERE name LIKE 'temp_%';
            """

    cursor.executescript(Q_CREATE_TMP_CONSTRAINTS)
    cursor.executescript(Q_CREATE_TMP_CONSTRAINT_DETAILS)

    for table in schemas.tables:
        for constraint in table.constraints:

            target_constraint, target_constraint_detail = (), ()
            target_constraint += table.name,
            target_constraint += constraint.name,
            target_constraint += "P" if "PRIMARY" in constraint.kind else "F",
            target_constraint += check(constraint.reference),
            target_constraint += "",

            target_constraint += 'TRUE' if constraint.prop_has_value_edit else 'FALSE',
            if constraint.prop_full_cascading_delete:
                target_constraint += 'TRUE',
            elif constraint.prop_cascading_delete is not None:
                target_constraint += "FALSE",
            else:
                target_constraint += "NULL",

            target_constraint += check(constraint.expression),
            cursor.execute(Q_ADD_TMP_CONSTRAINT, target_constraint)

            # Позиция констрейнта
            position = table.constraints.index(constraint) + 1
            target_constraint_detail += constraint.name,
            target_constraint_detail += position,
            target_constraint_detail += check(constraint.items),
            target_constraint_detail += table.name,
            cursor.execute(Q_ADD_TMP_CONSTRAINT_DETAIL, target_constraint_detail)

    # Заполняем таблицу dbd$indices и удаляем временные имена
    cursor.executescript(Q_RELEASE_CONSTRAINTS)
    cursor.executescript(DELETE_TEMP_CONSTRAINTS_NAMES)
