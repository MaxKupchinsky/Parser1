def nn(title, val):
    if val is not (None):
        return title + " " + str(val)
    else:
        return ""


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
