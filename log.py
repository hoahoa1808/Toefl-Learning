import sys
from loguru import logger
import random
colors = ["red", "cyan", "white", "green", "blue", "yellow"] 
class Drawer(object):
    def __init__(self) -> None:
        #formatlog
        # logger.remove()
        # logger.add(sys.stdout, format="<red>(NDA)</red>[{level}]|<green>{time:YYYY-MM-DD HH:mm:ss}</green> --> {message}",
        #         level="INFO", colorize=True)

        #other level
        logger.level("MAINMENU", no=40, color="<yellow>", icon="🐍")
        logger.level("QUESTION", no=42, color="<blue>", icon="🐖")
        logger.level("ANSWER", no=41, color="<red>", icon="🐖")
        logger.level("SHOWCASEANSWER", no=42, color="<red>", icon="🐖")
        logger.level("STATISTIC", no=43, color="<red>", icon="🐖")
        self.logger = logger

        #temparory mem
        


    def main_menu(self, topic:list):
        msg = ""
        print("\t\t\t\t\t <-----MAIN MENU----->\t")
        for i, x in enumerate(topic): 
            c = random.choice(colors)
            x = x + " "* (20-len(x)) if len(x) < 20 else x[:20]
            msg += "\t{}.{} ".format(i+1,x)
            if (i+1) % 5 == 0 or i == len(topic)-1: 
                logger.remove()
                logger.add(sys.stdout, format= "\n<{}>".format(c) + "{message}"+ "</{}> \n".format(c,c), level="MAINMENU", colorize=True)
                self.log("mainmenu", msg)
                msg = ""

        


    def quest(self, question, answer:str=None, noise:list=None, qtype="choice", pronouce=""):
        logger.remove()
        logger.add(sys.stdout, format="\n--><red>?</red>[<yellow>"+qtype+"</yellow>]:  {message}" 
                                    + f"\n--><magenta>%</magenta>[<yellow>Pronouce</yellow>]: <cyan>{pronouce}</cyan>", 
                    level="QUESTION", colorize=True)
        self.log("question", question)
        da = -1
        if qtype=="choice":
            da = self.answer(answer=answer, noise=noise)
        return da
        

    def answer(self, answer:str, noise:list):
        logger.remove()
        logger.add(sys.stdout, format="\n<blue>{message}</blue>", level="ANSWER", colorize=True)
        stt = [answer] + noise
        random.shuffle(stt)
        msg = ""
        for i, x in enumerate(stt): msg += "\t{}. {} ".format(i+1,x)
        self.log("answer", msg)
        return stt.index(answer) + 1

    def showcase(self, answer, qtype="choice", flag=True):
        logger.remove()
        if not flag: flag = f"\t!!!<red>{flag}</red>"
        else : flag = f"\t!!!<green>{flag}</green>"
        logger.add(sys.stdout, format=flag +" --->ANSWER: <yellow>{message}</yellow>", level="SHOWCASEANSWER", colorize=True)
        self.log("showcaseanswer", answer)
            
    def statistic(self, false_rate, true_rate, all_len, nwords, topic):
        logger.remove()
        logger.add(sys.stdout, format="\t--Fasle: <red>{message}</red>", level="STATISTIC", colorize=True)
        total = false_rate + true_rate
        print(f"\nSummary {total} Quests for learning {nwords} / {all_len} in topic \`{topic}\`")
        false_rate = false_rate / total * 100
        true_rate  = true_rate / total * 100
        fbar = "=" * int(false_rate) + f" | {false_rate:4f}"
        self.log("statistic", fbar)
        
        
        logger.remove()
        logger.add(sys.stdout, format="\t--True : <green>{message}</green>", level="STATISTIC", colorize=True)
        tbar = "=" * int(true_rate) + f" | {true_rate:4f}"
        self.log("statistic", tbar)

    def log(self,level, msg):
        '''Args
        level: (str) type of logs channel/process. examples: TRAINLOG, TESLOG
        msg  : (str) message
        '''
        self.logger.log(level.upper(), msg)


if __name__ == "__main__":
    l = Drawer()

    l.log("mainmenu", "okbaby!!!")
    l.main_menu(topic=["health", "university life"])
    l.quest("hay chon gia dung", qtype="write")
    l.quest("hay chon gia dung", answer="haha", noise=["hahah", "hihihi", "hihss"])
    l.statistic(5, 10)
    l.showcase("haha")
 