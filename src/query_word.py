from .connector import *
from .new_word import *
import eng_to_ipa as ipa

def insert_word(order,english,
            vietnamese,
            type_word,
            sentent_example_english,
            sentent_example_vietnamese,
            unit_code):
    if(english == ""):
        return
    pronounce = ipa.convert(english)
    mycursor = mydb.cursor()
    sql = "insert into \
            new_words(`order`,english,vietnamese,type_word,sentent_example_english, sentent_example_vietnamese,unit_code,pronounce) \
            values(%s,%s, %s, %s, %s, %s, %s,%s)"
    val = (order,
            english,
            vietnamese,
            type_word,
            sentent_example_english,
            sentent_example_vietnamese,
            unit_code,
            pronounce)
    mycursor.execute(sql, val)
    mydb.commit()

def update_word(
                order,
                english,
                vietnamese,
                type_word,
                sentent_example_english,
                sentent_example_vietnamese,
                unit_code
                ):
    mycursor = mydb.cursor()
    sql ="UPDATE new_words SET \
          `order` = %s, \
          vietnamese = %s, \
          type_word = %s, \
          sentent_example_english = %s, \
          sentent_example_vietnamese = %s, \
          unit_code = %s \
          WHERE english = %s"
    val =  (order,
            vietnamese,
            type_word,
            sentent_example_english,
            sentent_example_vietnamese,
            unit_code,
            english)
    mycursor.execute(sql,val)
    mydb.commit()

def get_one_word(english):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE english = %s"
    val = (english,)
    mycursor.execute(sql,val)
    w = mycursor.fetchall()
    if (len(w)>0):
        return result_to_word(w[0])
    return None

def get_all_word():
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words"
    mycursor.execute(sql)
    lst = []
    for w in mycursor.fetchall():
        lst.append(result_to_word(w))
    return lst

def get_by_unit(unit_code):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE unit_code=%s ORDER BY `order` ASC"
    val = (unit_code.upper(),)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
        lst.append(result_to_word(w))
    return lst

def get_by_total_times(times):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE (right_times + wrong_times) <= %s"
    val = (times,)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
        lst.append(result_to_word(w))
    return lst

def get_by_most_fail(percent):
    mycursor = mydb.cursor()
    sql ="SELECT * FROM new_words WHERE (wrong_times / (right_times + wrong_times))*100 >= %s"
    val = (percent,)
    mycursor.execute(sql,val)
    lst = []
    for w in mycursor.fetchall():
        lst.append(result_to_word(w))
    return lst

def increment_right_times(english):
    mycursor = mydb.cursor()
    sql ="UPDATE new_words SET \
          right_times = right_times + 1 \
          WHERE english = %s"
    val =  (english,)
    mycursor.execute(sql,val)
    mydb.commit()

def increment_wrong_times(english):
    mycursor = mydb.cursor()
    sql ="UPDATE new_words SET \
          wrong_times = wrong_times + 1 \
          WHERE english = %s"
    val =  (english,)
    mycursor.execute(sql,val)
    mydb.commit()

def update_or_insert_word(order,
                        english,
                        vietnamese,
                        type_word,
                        sentent_example_english,
                        sentent_example_vietnamese,
                        unit_code):
    if (get_one_word(english) == None):
        insert_word(order,
                    english,
                    vietnamese,
                    type_word,
                    sentent_example_english,
                    sentent_example_vietnamese,
                    unit_code)
    else:
        update_word(order,
                    english,
                    vietnamese,
                    type_word,
                    sentent_example_english,
                    sentent_example_vietnamese,
                    unit_code)


def result_to_word(result):

    w = NewWords(result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5],
                result[6])

    w.pronounce = result[7]
    w.right_times = result[8]
    w.wrong_times = result[9]
    w.create_date = result[10]
    w.last_study_date =result[11]
    return w
