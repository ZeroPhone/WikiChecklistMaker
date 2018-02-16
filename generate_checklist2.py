import os, time, datetime
import parse_wiki
from data_to_pdf import DataToPdf

data = parse_wiki.get_parts(parse_wiki.get_page_contents())

print(data)

fields = (
    ('name', 'Name'),
#    ('quantity', 'Quantity'),
#    ('subcategories', 'Subcategories'),
#    ('notes', 'Notes'),
    
)

doc = DataToPdf(fields, data)
doc.export('LogFiles.pdf')
