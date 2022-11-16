#Quizlet
from log import Drawer
from server import database
import os
clear = lambda: os.system('cls')
import random

def check_write_ans(a,b):
    a = str(a).strip().lower()
    b = str(b).strip().lower()
    if len(a) == 0 or len(b) == 0: 
        print("len 0")
        return False
    if len(a) != len(b): 
        return False
    for i, x in enumerate(a):
        if b[i] != x : 
            print(b[i], " <> ", x)
            return False
    return True
    
def main():
    #INIT 
    log = Drawer()
    
    while True:
        random.seed(random.randint(50, 100))
        random.seed(random.randint(100, 1000))
        #MENU
        clear()
        log.main_menu(database.get_topics())
        try:
            topic = int(input("Choose topic to practice[1-{}]: ".format(len(database.get_topics())))) - 1
            database.get_topics()[topic]
            database.set_topic(topic)
        except:
            assert 0, "nhap sai vcd cai id top pic"


        try: num = int(input(f"What Number of question in the ensue test do u want ̣(default {database.get_len_topic()}): ")) 
        except: num = database.get_len_topic()


        #statistic
        correct = 0
        words = []
        for i in range(num):
            quest = database.gen_quest()
            true_ans = log.quest(question=quest['q'], answer=quest['a'], 
                                noise=quest['noise'], qtype=quest['t'], pronouce=quest['p'])
            
            while True:
                ur_ans = input("\n\tEnter ur answer : ")
                if true_ans < 0: break
                flag = True
                try:
                    int(ur_ans)
                except:
                    print("\t!!!Answer is a number")
                    flag = False
                if flag : break
                

            flag = False
            if true_ans > 0:
                if true_ans == int(ur_ans): 
                    correct += 1
                    database.base_weight[quest['id']] += 1
                    flag = True
                    words += [quest['id']]
            else:
                if check_write_ans(quest["a"], ur_ans): 
                    correct += 1
                    database.base_weight[quest['id']] += 1
                    flag = True
                    words += [quest['id']]

            log.showcase(answer=quest['a'], qtype=quest['t'], flag=flag)

        log.statistic(false_rate=num-correct, true_rate=correct, 
                    all_len=len(database.df), nwords=len(set(words)), topic=database.get_name_topic())
        database.save_profile()
        k = input("press any key for continue (Q for quit)")
        if k.lower() == "q": break

if __name__ == "__main__":

    main()