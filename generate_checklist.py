import sys
import calendar
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

import parse_wiki
import pprint

month_num = datetime.now().month
month_name = calendar.month_name[month_num]
year_num = datetime.now().year
c = calendar.Calendar()
data = get_parts(get_page_contents())
print(data)

doc = SimpleDocTemplate("Checklist_{}_{}.pdf".format(year_num, month_name), pagesize=landscape(A4),
                        rightMargin=72,leftMargin=72,
                        topMargin=40,bottomMargin=0)
elements = []

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

elements.append(Paragraph("<font size=30>Checklist generated {} {}</font>".format(month_name, year_num), styles["Center"]))

t=Table(data[name][quantity])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('ALIGN',(0,0),(-1,-1),'RIGHT'),
                       #('BACKGROUND',(0, 0),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('TEXTCOLOR',(5,0),(-1,-1),colors.red)]))
elements.append(t)
doc.build(elements)

