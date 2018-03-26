from codecs import open
from ram_to_xml import ram_to_xml
from xml_to_ram import xml_to_ram


def compare(source, result):
    with open(result, 'r', 'utf8') as source_file, \
            open(source, 'r', 'utf8') as result_file:
        equal = True
        for source_line in source_file:
            result_line = result_file.readline()
            if source_line.split(' ') != result_line.split(' '):
                print('Differences in:')
                print(source_line)
                print(result_line)
                equal = False
        return equal


def test(input, output):
    xml_schemas = xml_to_ram(input)
    ram_to_xml(xml_schemas, output)
    if compare(input, output):
        print('Files are fully identical')
