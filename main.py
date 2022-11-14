#Quizlet
from log import Drawer
from server import database
import os
clear = lambda: os.system('cls')
import random

random.seed(random.randint(50, 100))
random.seed(random.randint(100, 1000))

def main():
    #INIT 
    log = Drawer()
    
    while True:
        #MENU
        clear()
        log.main_menu(database.get_topics())
        try:
            topic = int(input("Choose topic to practice[1-{}]: ".format(len(database.get_topics())))) - 1
            database.get_topics()[topic]
            database.set_topic(topic)
        except:
            assert 0, "nhap sai vcd cai id top pic"


        try: num = int(input("What Number of question in the ensue test do u want ̣(default 1): ")) 
        except: num = 1


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
                if true_ans == ur_ans.strip().lower(): 
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