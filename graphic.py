import tkinter as tk
from tkinter import *
import math
import random
from log import Drawer
from server import database
import time
colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"] 
random.seed(random.randint(50, 100))
random.seed(random.randint(100, 1000))
#FONT
helv24 = "Helvetica 24 bold"
time20 = "Times 20 bold italic"
btnf   = "Times 10"
notf   = "Helvetica 9 bold"
cali10 = 'Calibre 12 normal'

def check_write_ans(a,b):
    a = str(a).strip().lower()
    b = str(b).strip().lower()
    if len(a) == 0 or len(b) == 0: 
        return False
    if len(a) != len(b): 
        return False
    for i, x in enumerate(a):
        if b[i] != x : 
            return False
    return True

def revert_position(element):
    x = element.winfo_x()
    y = element.winfo_y()
    element.place(x = -x, y = -y) 

class Drawer(object):
    def __init__(self) -> None:
        #other level
        self.Wsize = 620
        self.demoninator = denominator = 5
        self.root =  tk.Tk()
        self.root.title = "Quizlet"
        self.main_canvas = tk.Canvas(self.root, width = self.Wsize, height = self.Wsize // denominator * (denominator-1), 
                        bg="#132266")
        text_header = "🫡Cùng học English 💯 "
        self.header = tk.Label(self.root, text=text_header, bd=3, anchor="n",cursor="dot" ,bg="#009999", font=helv24)
        self.title = tk.Label(self.root, text="HI!", font=time20, fg="red")

        self.topicFrame = tk.Frame(self.main_canvas, bg="#009999", relief=tk.RAISED, borderwidth=1)
        self.notification = tk.Label(self.root , text="Notification!!!", font=notf, fg="#0000cc", 
                        cursor="spider",  bg="#ffccff", height=1, justify=LEFT)

        #geography
        self.main_canvas.place(x=0, y = self.Wsize // denominator + 5); self.main_canvas.update()
        self.header.place(x = self.Wsize // denominator, y = 0); self.header.update()
        self.title.place(x=self.Wsize // denominator * 2 - 25, y=self.header.winfo_height() + 8)
        self.notification.place(x=10, y=self.Wsize // denominator  - 20 )
        
        self.mc_height = self.main_canvas.winfo_height()
        self.mc_width = self.main_canvas.winfo_width()
        self.topicFrame.place(x=8, y=20)

        #DATABASE
        self.database = database
        self.resetparam(mode=1)




        
    def run(self):

        self.root.minsize(self.Wsize, self.Wsize)  
        self.root.maxsize(self.Wsize, self.Wsize)

        self.main_menu(self.database.get_topics())
        self.root.mainloop()

    def resetparam(self, mode=1):
        """
        It resets the model to the initial state instead of destroying elements.
        
        :param mode: The model to use. 1 is the default reset full, 2 is the model with the extra features,
        defaults to 1 (optional)
        """
        self.__hasanswerd = False
        self.__true_ans = 0
        self.__count_quest = 0
        self.__numquests = 0
        self.__quest = None
        self.__distictwords = []
        self.__topic = None
        self.text_var=tk.StringVar()


    def main_menu(self, topic:list):
        self.resetparam()
        text = "MAIN MENU"
        self.title.config(text = text)
        ncols = 4
        for i in range(len(topic) // ncols + 1):
            for j in range(ncols):
                t = topic[i*(ncols)+j] if i * (ncols) + j < len(topic) else ""
                label = None 
                if t == "":
                    label = tk.Button(master=self.topicFrame, text=f"",
                                width=20, height=2, bg="#132266" )
                else:
                    label = tk.Button(master=self.topicFrame, text=f"{t}", fg="#{}".format(random.randint(100000, 999999)),
                                width=20, height=2, highlightcolor="#ff0066", command=self.wrap_test(i*(ncols)+j), 
                                cursor="heart", relief=GROOVE, font=btnf )
                label.grid(row=i, column=j)


    def create_test(self):
        self.questFrame = tk.Canvas(self.root, bg="#9999ff", width = self.Wsize, 
                                    height = self.Wsize // self.demoninator * (self.demoninator-1))
        self.questFrame.place(x=0, y = self.Wsize // self.demoninator + 5)
        self.progressbar = tk.Canvas(self.root, bg="#33cc33", width=self.Wsize // self.__numquests, height=60)
        self.progressbar.place(x=0, y = self.Wsize - 50)
        self.question = Label(self.questFrame, text="QUESTION:  ",  height=3);self.question.place(x=10, y=20)
        self.pronounce = Label(self.questFrame, text="PRONOUCE:  ", fg="blue");self.pronounce.place(x=10, y=80)
        self.choices = []
        noise = ["", "", "",""]
                
        for i, x in enumerate(noise): 
            tmp = tk.Button(master=self.questFrame, text=f"{x}", fg="white",bg="#000066",
                                width=30, height=2, highlightcolor="#ff0066", 
                                command=self.wrap_anser(true_ans="", btn_ans=x, btn=i),
                                cursor="target", relief=RAISED, font=btnf)     
            self.choices.append(tmp)
        self.write_input = tk.Entry(self.questFrame, textvariable=self.text_var ,bd =3, width=20)
        self.write_input.bind('<Return>', self.show_wanswer)
                
        self.nextbtn = tk.Button(master=self.questFrame, text=f"Next", fg="white",bg="#e6e600",
                                width=10, height=2, 
                                command=self.wrap_quests(),
                                cursor="man", relief=RAISED, font=btnf); self.nextbtn.place(x=self.mc_width // 2 - 80, y=320)
        self.endbtn = tk.Button(master=self.questFrame, text=f"END", fg="white",bg="#39004d",
                                width=10, height=2, 
                                command=self.end_test,
                                cursor="fleur", relief=RAISED, font=btnf); self.endbtn.place(x=self.mc_width // 2 + 20, y=320)
    
        self.show_quest()
        

    def show_quest(self):
        if self.__numquests == self.__count_quest:
            self.end_test()
            return
        self.__quest = self.database.gen_quest()
        true_ans = self.__quest['a']
        noise = self.__quest["noise"] + [self.__quest['a']]
        while len(noise) < 4: noise += ["???"];random.shuffle(noise);random.shuffle(noise)

        words = self.__quest["q"].split()
        questdetail = " "
        thres = 66
        for i in words:
            if len(questdetail) > thres:
                questdetail += f"{i}\n\t"
                thres += 50
            else: questdetail += f"{i} "  

        #questdetail = self.__quest["q"] #if len(self.__quest["q"]) < 100 else self.__quest["q"][:100] + "\n\t" + self.__quest["q"][100:]
        self.question.config(text= "QUESTION:{}".format(questdetail))
        self.pronounce.config(text= "PRONOUCE:{}".format(self.__quest["p"]))

        if self.__quest["t"] == "choice":
            for i, x in enumerate(noise):
                self.choices[i].config(text=x, 
                        command=self.wrap_anser(true_ans=true_ans, btn_ans=x, btn=i), 
                        fg="white",bg="#000066")

            bx = 50; by=150
            for i in range(1, len(self.choices) + 1):
                self.choices[i-1].place(x=bx, y=by)
                if i % 2 == 0: 
                    by += 50
                    bx = 50
                else: 
                    bx += 320
                    # by=150
            self.write_input.place(x=-bx, y=-by)
        else:
            self.text_var.set("")

            bx = 50; by=150
            self.write_input.config(bg="white")
            self.write_input.place(x=bx, y=by)
            for i in range(1, len(self.choices) + 1):
                self.choices[i-1].place(x=-bx, y=-by)
   
        
        self.log("")
        self.__hasanswerd = False
        self.__count_quest += 1
        self.update_processbar()


    def show_answer(self, check, btn): 
        if self.__hasanswerd: return
        self.__hasanswerd = True
        c = "#33cc33" if check else "#990000"
        self.choices[btn].config(bg=c)
        #send to server
        if check: 
            self.database.base_weight[self.__quest['id']] += 1
            self.__distictwords += [self.__quest['a']]
            self.log(mess="Correct 👍")
            self.__true_ans += 1
        else: 
            self.log(mess="Incorrect 👊!  True_answes is: {}".format(self.__quest['a']))
            for i in range(len(self.choices)):
                if self.choices[i].cget("text") == self.__quest['a']:
                    self.choices[i].config(bg="#33cc33")
                    break


    def show_wanswer(self, *args): 
        if len(self.text_var.get().strip())==0: return    
        if self.__hasanswerd: return
        self.__hasanswerd = True
        check = check_write_ans(self.__quest['a'], self.text_var.get())
        c = "#33cc33" if check else "#990000"
        self.write_input.config(bg=c)
        if check: 
            self.database.base_weight[self.__quest['id']] += 1
            self.__distictwords += [self.text_var.get()]
            self.log(mess="Correct 👍", sleep=3)
            self.__true_ans += 1
        else:
            self.log(mess="Incorrect 👊! True_answes is: {}".format(self.__quest['a'].upper()), sleep=3)
        # self.show_quest()
        

        
    def end_test(self):
        self.statistic(true_quests=self.__true_ans, total_quests=self.__numquests,
                    all_len=self.database.get_len_topic(),
                    nwords=len(set(self.__distictwords)), topic=self.database.get_name_topic())
        self.database.save_profile()
        self.title.config(text="MAIN MENU")
        self.title.place(x=self.Wsize // self.demoninator * 2 - 25, y=self.header.winfo_height() + 8)
        self.progressbar.destroy()
        self.questFrame.destroy()

    def update_processbar(self):
        try:self.progressbar.config(width=self.Wsize * self.__count_quest // self.__numquests)
        except: pass


    def statistic(self, true_quests, total_quests, all_len, nwords, topic):
        true_rate  = true_quests / total_quests * 100
        overMess = f"Summary {total_quests} Quests in topic `{topic}` : Accuracy - {true_rate:.2f}% | Process {nwords} / {all_len} words"
        self.notification.config(text=overMess, font=cali10)
    def log(self, mess, sleep=0):
        overMess = "!!!Notify:" + mess
        self.notification.config(text=overMess, font=notf)
        if sleep > 0:
            time.sleep(sleep)
        
    ################################################33
    #wrap function for button
    def wrap_quests(self):
        def x():
            self.show_quest()
        return x
    
    def wrap_anser(self, true_ans, btn_ans, btn):
        check = check_write_ans(true_ans, btn_ans)
        def inner():
            self.show_answer(check, btn) 
        return inner

    def wrap_test(self, id):
        def x():
            self.resetparam()
            self.database.set_topic(id)
            self.__topic = id
            self.__numquests = random.randint(5, min(25, self.database.get_len_topic())) if self.database.get_len_topic() > 5 else 5
            title = "TOPIC : " + self.database.get_name_topic().upper()
            self.title.config(text=title)
            self.title.place(x=self.Wsize // self.demoninator * 2 - len(title)*5, y=self.header.winfo_height() + 8)
            self.create_test()
        return x

            


  




if __name__ == '__main__':
    l = Drawer()
    l.run()
    


