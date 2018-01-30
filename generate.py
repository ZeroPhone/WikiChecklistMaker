"""
Code written with help of https://www.blog.pythonlibrary.org Reportlab tutorials

Code generates productivity calendars for a given month of current year. Pass the month number as first argument - like python generate.py 1 .
"""


import sys
import calendar
from copy import copy
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

month_num = int(sys.argv[1])
month_name = calendar.month_name[month_num]
year_num = datetime.now().year
c = calendar.Calendar()

# !! CHANGE pagesize to allow for different sizes perhaps through input (sys.argv[2] maybe)
doc = SimpleDocTemplate("Checklist_{}_{}.pdf".format(year_num, month_name.lower()), pagesize=landscape(A4),
                        rightMargin=72,leftMargin=72,
                        topMargin=40,bottomMargin=0)
elements = []

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

#Fun with Python and objects being duplicated
#data = 5*[7*[""]] #Sudden realisation
#data = 5*[7*copy([""])] #Naive attempt at fixing
#data = 5*[7*list([""])] #Same

#Well then.
data = [["" for x in range(7)] for x in range(5)]

weeknum = -1 #Starting with weekday 0 which will increment this immediately
for day, weekday in c.itermonthdays2(year_num, month_num):
   """itermonthdays2: return an iterator for the month month in the year year similar to itermonthdates(). Days returned will be tuples consisting of a day number and a week day number."""
   if weekday == 0:
       weeknum += 1
   if weeknum > 4: #Limiting ourselves to 5 columns
       weeknum = 0 #Coming back to the first column if it overlaps
   if day == 0:
       pass
   else:
       data[weeknum][weekday] = str(day).zfill(2)

elements.append(Paragraph("<font size=30>Productivity calendar for {} {}</font>".format(month_name, year_num), styles["Center"]))
elements.append(Spacer(1, 40))
t=Table(data,7*[1.5*inch], 5*[1.2*inch])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('ALIGN',(0,0),(-1,-1),'RIGHT'),
                       #('BACKGROUND',(0, 0),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('TEXTCOLOR',(5,0),(-1,-1),colors.red)]))
elements.append(t)
# write the document to disk
doc.build(elements)
