from src.query_word import *
from src.import_excel import *
from src.config import *
from src.constant import *

from os import system
import random
from termcolor import colored
import pyttsx3
import eng_to_ipa as ipa

dash ="=============================================================="
dashln =dash+"\n"
session_word = []
def sound(english):
    engine = pyttsx3.init()
    engine.say(english)
    engine.runAndWait()

def ok():
    sound("Good")
    print(colored('OK', 'green'))
    print(dashln)

def wrong():
    sound("write again")
    print(colored('WRONG', 'red'))

def high_light(word,senence,color):
    if senence == None:
        result = color+word+CEND
    else:
        result = senence.replace(word,color+word+CEND)
        result = senence.replace(word.lower(),color+word.lower()+CEND)
    return result

def main_menu():
    print(dash)
    print("---------------HACKNAO1500---------------")
    print(dashln)
    print("[1]. Update vocabulary!")
    print("[2]. Study vocabulary!")
    print("[3]. Revise vocabulary!")

    print("\n[0]. Exit!")
    print("-----------------------------------------\n")

def update_vocabulary():
    loc="C:\\Users\\ASUS\\Documents\\hacknao1500\\Unit1_LanguageLearning.xlsx"
    import_excel(loc)

def sub_menu2():
    print(dash)
    print("-----------2.STUDY VOCABULARY------------")
    print(dashln)
    print("[1]. Unit!")
    print("[2]. Total_times!")
    print("[3]. Fail_ratio!")

    print("\n[0]. Return HACKNAO1500!")
    print(dashln)
def reset_menu(menu):
    system("cls")
    if(menu == "main_menu"):
        main_menu()
    elif(menu == "sub_menu2"):
        sub_menu2()

def vocabularies_of_unit():
    while True:
        command = input(">>> command/unit_code: ")
        unit_code = command
        if (command == "-h"):
            print("\nOption h/help l/list")
        elif (command == "-l"):
            units = get_all_unit()
            i = 0
            for u in units:
                i +=1
                if (i % 15 == 0):
                    input(">>> Enter to continue!")
                print("\n",u.unit_code," ===> ",u.unit_topic)
        elif (get_by_unit(unit_code) != None):
            return get_by_unit(unit_code)
        elif (command == '-q' or command == "-quit"):
            reset_menu("sub_menu2")
            break
        elif (get_one_unit(unit_code) == None):
            print("\nunit code not found!")
        else:
            return get_vocabularies()
    return None



def vocabularies_of_total_times():
    print("vocabulary of total times")

def vocabularies_of_fail_ratio():
    print("vocabulary of ratio")

def check_read(list_words):
    index = 0
    system("cls")
    print("========== CHECK READ ================")
    for w in list_words:
        index +=1
        print("[",index,"].",w.english," >>> ",w.vietnamese)
    try:
        index = int(input("Enter/index to Continue...")) -1
        print(index)
    except:
        index = 0
    list_words = list_words[index:]
    random.shuffle(list_words)
    list_wrong_words = []

    for w in list_words:
        index += 1
        print("[",index,"]. CHECK READ")
        print("English: ?")
        print("VietNamese:",w.vietnamese)
        print("Example: ",high_light(w.vietnamese,w.sentent_vietnamese,CYELLOW2))
        print(dash)

        input_word = input(">>> ")
        if(input_word == "-q" or input_word == "-quit"):
            list_wrong_words = []
            break
        elif (input_word == "-w" or input_word == "-wrong"):
            break
        if(input_word.lower() == w.english.lower()):
            print("English: "+high_light(w.english,None,CBLUE2))
            ok()
            sound(w.english)
            increment_right_times(w.english)
        else:
            list_wrong_words.append(w)
            print("English: "+high_light(w.english,None,CRED2))
            increment_wrong_times(w.english)
            wrong()
        # input_sentence = input(">>> ")
        # if(input_sentence == "-q" or input_sentence == "-quit"):
        #     return []
        # if(standard_string(input_sentence.lower())
        #         == standard_string(w.sentent_english.lower())):
        #     print("Example: "+high_light(w.english,w.sentent_english,CBLUE2))
        #     ok()
        #
        # else:
        #     list_wrong_words.append(w)
        #     print("===> ",high_light(w.english,w.sentent_english,CRED2))
        #     wrong()


    return list_wrong_words

def check_listen(list_words):
    index = 0
    system("cls")
    print("========== CHECK LISTEN ================")
    for w in list_words:
        index +=1
        print("[",index,"].",w.english," >>> ",w.vietnamese)
    try:
        index = int(input("Enter/index to Continue...")) -1
    except:
        index = 0

    list_words = list_words[index:]
    random.shuffle(list_words)
    list_wrong_words = []
    for w in list_words:
        index += 1
        print("[",index,"]. CHECK LISTEN")
        print("English: ?")
        print(dash)
        sound(w.english)
        input_word = input(">>> ")

        if(input_word== "-q" or input_word == "-quit"):
            return []
        if(input_word.lower() == w.english.lower()):
            print("English: "+high_light(w.english,None,CBLUE2))
            print("VietNamese: ",high_light(w.vietnamese,None,CYELLOW2))
            ok()
            increment_right_times(w.english)

        else:
            list_wrong_words.append(w)
            print("English: "+high_light(w.english,None,CRED2))
            wrong()
            increment_wrong_times(w.english)


    return list_wrong_words

def check_again(lst_words):
    lst_words_wrong = check_read(lst_words)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_read(lst_words_wrong)
    lst_words_wrong = check_listen(lst_words)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_listen(lst_words_wrong)

def word_info(idx,word):
    system("cls")
    print("[",idx+1,"]. STUDY VOCABULARY ")
    print("English: ",high_light(word.english,None,CBLUE2))
    print("Vietnamese: ",high_light(word.vietnamese,None,CYELLOW2))
    print("Pronunce: /",word.pronounce,"/")
    print("Type: ",TYPE_WORD[word.type_word])
    print("Example: ",high_light(word.english,word.sentent_english,CBLUE2))
    print("IPA:    /",ipa.convert(word.sentent_english),"/")
    print("Mean: ",high_light(word.vietnamese,word.sentent_vietnamese,CYELLOW2))

    print("\nRight times: ",colored(word.right_times, 'green'))
    print("Wrong times: ",colored(word.wrong_times, 'red'))
    print(dash)

def study_word(idx,word):
    while True:
        word_info(idx,word)
        input_word = input(">>> ")
        if(input_word.startswith("-")):
            if((input_word == "-n" or input_word == "-next")
                or (input_word == "-p" or input_word == "-prefix")
                or (input_word == "-nn" or input_word == "-nextnot")
                or (input_word == "-q"or input_word == "-quit")
                or (input_word.startswith("-j"))
                or (input_word.startswith("-ja"))
                or (input_word == "-u" or input == "-update")):
                return input_word
            elif(input_word == "-cl"or input_word == "-clear"):
                global session_word
                session = []
            elif(input_word == "-ch"or input_word == "-check"):
                check_again([word])
            elif(input_word == "-cha"or input_word == "-checkall"):
                check_again(session_word)
            elif(input_word == "-h"or input_word == "-help"):
                print("-n/-next : next word and save into session")
                print("-nn/-nextnot : next word and not save into session")
                print("-p/-prefix: prefix word")
                print("-j/-jump<order>: go to order word")
                print("-ch/-check : check current word and save it into session")
                print("-cha/-checkall : next all words in session")
                print("-q/-quit : quit study vocabularies")
                print("-h/-help : show all command")
                input("Enter to continue...")
            else:
                input("Command not found...")
        else:
            if ((input_word.lower() == word.english.lower())
                or (standard_string(input_word.lower())
                        == standard_string(word.sentent_english.lower()))):
                word.right_times += 1
                increment_right_times(word.english)
                print("Vietnamese: ",colored(word.vietnamese, 'yellow'))
                sound(input_word.lower())
            else:
                word.wrong_times +=1
                increment_wrong_times(word.english)
    return input_word

def study_start(vocabularies):
    i = 0
    global session_word
    for v in vocabularies:
        i += 1
        print("[",i,"] ",v.english," ===> ",v.vietnamese)
    input("Enter to continue...")
    #random.shuffle(vocabularies)
    i = 0
    while True:
        word_info(i,vocabularies[i])
        sound(vocabularies[i].english)
        input_word = study_word(i,vocabularies[i])
        if(input_word == "-n" or input_word == "-next"):
            session_word.append(vocabularies[i])
            if(i<len(vocabularies)-1):
                i += 1
        elif(i<len(vocabularies) and (input_word == "-nn" or input_word == "-nextnot")):
            i += 1
        elif(i>0 and (input_word == "-p" or input_word == "-prefix")):
            i -= 1
        elif(input_word.startswith("-ja")):
            try:
                i = int(input_word[3:]) - 1
                session_word = []
                for ii in range (i):
                    session_word.append(vocabularies[ii])
            except:
                pass
        elif(input_word.startswith("-j")):
            try:
                i = int(input_word[2:]) - 1
            except:
                pass
        elif (input_word == "-u" or input_word == "-update"):
            update_vocabulary()
            vocabularies = get_vocabularies()
        elif(input_word == "-q"or input_word == "-quit"):
            reset_menu("sub_menu2")
            break

def study_vocabulary():
    sub_option = -1
    while sub_option != 0:
        if(sub_option == 1):
            vocabularies = get_vocabularies()
            if(vocabularies != None):
                if(len(vocabularies) > 0):
                    study_start(vocabularies)
                else:
                    print("Not any vocabulary!")
                    reset_menu("sub_menu2")
        elif (sub_option == 2):
            vocabularies_of_total_times()
        elif (sub_option == 3):
            vocabularies_of_fail_ratio()
        else:
            reset_menu("sub_menu2")
        try:
            sub_option = int(input(">>> Your choice: "))
        except:
            sub_option = -1
    reset_menu("main_menu")

def get_vocabularies():
    global session_word
    session_word = []
    # get all unit
    units = get_all_unit()
    for i in range(len(units)):
        print("["+str(i+1)+"]     Code:",units[i].unit_code,"     Topic:",units[i].unit_topic)

    print("\n 0 >>>If you want quit!")
    # get chooses
    chooses = input("input choose: ")
    if(chooses.startswith("0")):
        return
    u_list = []
    for u in chooses.split(","):
        us = u.split("-")
        if len(us)>1 :
            try:
                start = int(us[0])
                end = min(int(us[1])+1,len(units)+1)
                for i in range(start,end):
                    u_list.append(i)
            except:
                pass
        else:
             u_list.append(u)

    # get unit code list

    unit_code_list = []
    for i in u_list:
        try:
            idx = int(i)-1
            unit_code_list.append(units[idx].unit_code)
        except:
            pass

    # get vocabularies
    vocabularies = []
    for uc in unit_code_list:
        vocabularies.extend(get_by_unit(uc))
    return vocabularies

def revise_vocabulary():
    vocabularies = get_vocabularies()
    # revise
    lst_words_wrong = check_read(vocabularies)
    while len(lst_words_wrong) > 0 :
        lst_words_wrong = check_read(lst_words_wrong)

def main():
    global session_word
    session_word=[]
    option = -1
    while (option != 0):
        if (option == 1):
            update_vocabulary()
        elif (option == 2):
            study_vocabulary()
        elif (option == 3):
            revise_vocabulary()

        try:
            reset_menu("main_menu")
            option = int(input(">>> Your choice: "))
        except:
            option = -1
main()
