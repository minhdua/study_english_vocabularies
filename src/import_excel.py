import xlrd
from . import new_word
from .query_unit import *
from .query_word import *
import re
# Give the location of the file


def standard_string(st):
    pattern = re.compile(r'(^\s+)|(\s+$)|\s\s')
    st = re.sub(pattern,'',st)
    return st.capitalize()

def standard(e):
    lst = []
    lst.append(int(e[0]))
    for i in range(1,6) :
        lst.append(standard_string(str(e[i])))
    return lst

def import_excel(loc):
    wb = xlrd.open_workbook(loc)
    for sheet in wb.sheets():
        unit_code = sheet.cell_value(0,1).upper()
        unit_topic = sheet.cell_value(1,1)
        print(unit_code," ===> ",unit_topic)
        update_or_insert_unit(unit_code,unit_topic)
        start = 4
        for i in range(start,sheet.nrows):
            e = sheet.row_values(i)
            e = standard(e)
            english = e[0]
            #word = new_word.NewWords(e[1],e[2],e[3],e[4],e[5],unit_code)
            update_or_insert_word(e[0],e[1],e[2],e[3],e[4],e[5],unit_code)
