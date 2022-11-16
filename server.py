import random
import math
import os
import pandas as pd
import yaml

path = "words.xlsx"
profile = "profile.yaml"

class DB:
    def __init__(self) -> None:
        self.efile = pd.ExcelFile(path)
        self.topics = self.efile.sheet_names 
        
        #for practise
        self.df = None
        self.focus = None #id topic
        self.base_weight = []
        self.rand_weight = []


        #profile
        with open(profile, 'r') as file:
            self.profile = yaml.load(file, Loader=yaml.Loader)

            print(self.profile)


    def get_topics(self):
        return self.topics
    def get_name_topic(self):
        if not self.df is None:
            return self.topics[self.focus]
        else: return "None"
    def get_len_topic(self):
        if not self.df is None:
            return len(self.df)
        else: return 0

    def set_topic(self, index):
        self.focus = index
        self.df = self.efile.parse(self.topics[index])
        if self.topics[self.focus] in self.profile.keys():
            self.base_weight = self.profile[self.topics[self.focus]]
            self.base_weight = self.base_weight if self.profile[self.topics[self.focus]] == len(self.df) else self.base_weight + [0] * (len(self.df) - len(self.base_weight))
        else : self.base_weight =  [0] * (len(self.df))
        
        
        for i, x in enumerate(self.base_weight):
            self.rand_weight += [i] * max(0, 3-x)
        if len(self.rand_weight) == 0: self.save_profile()

        # print(self.base_weight)
        # print(self.rand_weight)

    def gen_quest(self):
        if len(self.rand_weight) == 0 : self.set_topic(self.focus)
        i = random.choice(self.rand_weight)
        self.rand_weight.pop(self.rand_weight.index(i))
        quest = {
            "id": i,
            "a": str(self.df.iloc[i, 0]).strip().lower(),
            "p": str(self.df.iloc[i, 1]).strip(),
            "q": str(self.df.iloc[i, 2]),
            "noise": [],
            "t": "choice"
        }
        if random.choice([False, True,  True, False, True, True]): 
            quest['t'] = "write"
            return quest
        noise = []
        while len(noise) < 3 and len(noise) < len(self.df) - 1:
            j = random.randint(0, len(self.df)-1)
            if j not in noise and i != j:
                noise += [j]
                quest["noise"].append(str(self.df.iloc[j, 0]).strip().lower())
        self.base_weight[i] += 1
            
        return quest

    def track(self, **kwargs):
        for k in kwargs:
            self.profile[k] = kwargs[k]

    def save_profile(self):
        self.base_weight = [ min(x, 3) for x in self.base_weight]
        if self.base_weight.count(3) > 9 / 10 * len(self.df): 
            self.base_weight = [0] * len(self.df)
        self.profile[self.topics[self.focus]] = self.base_weight
        with open(profile, 'w') as outfile:
            yaml.dump(self.profile, outfile, default_flow_style=False)

database = DB()

if __name__ == '__main__':
    l  = DB()
    l.set_topic(1)
    print(l.gen_quest())
