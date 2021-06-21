import csv
import pandas as pd
import json
import pickle
from random import choice
from datetime import datetime

def lang_code(lang):
    """Returns the international code of a language"""
    if lang.lower() in ['tedesco','deutsch','german','de']: return 'DE'
    elif lang.lower() in ['italiano','italienisch','italian','it']: return 'IT'
    elif lang.lower() in ['inglese','englisch','english','en']: return 'EN'
    else: return lang

class Dizio:
    ## Standard Labels
    OL    = 'Original Language'
    DL    = 'Destination Language'
    LEM   = 'Lemma'
    TRAN  = 'Translation'
    dizio_columns = [OL,DL,LEM,TRAN]
    DATE  = "Date added"
    EX    = "Examples"
    STATUS = "status"
    
    def __init__(self, iniz=[]):
        '''Each entry is a dictionary containing
                Original language, destination language,
                lemma, translation and possibly other info'''
        self.entries = []

    @property
    def lemmata(self):
        '''List of all lemmas'''
        return [entry[self.LEM] for entry in self.entries]

    @property
    def basic_entries(self):
        return [{i:entry[i] for i in self.dizio_columns}
                for entry in self.entries]

    @property
    def lower_entries(self):
        return [{self.OL:entry[self.OL],
                 self.DL:entry[self.DL],
                 self.LEM:entry[self.LEM].lower(),
                 self.TRAN:entry[self.TRAN].lower()}
                for entry in self.entries]
    
    def alpha_sort(self):
        self.entries.sort(key = lambda di : di.get(self.LEM))

    def date_sort(self):
        self.entries.sort(key = lambda di : di.get(self.DATE))
    
##    def check_duplicates: to do
    def isentry(self, entry):
        basic_entry = {i:entry[i] for i in self.dizio_columns}
        return basic_entry in self.basic_entries

    def append(self, entry):
        if type(entry) != dict:
            raise ValueError('Wrong type, expected "dict"')
        if self.DATE in entry.keys(): pass
        else: entry[self.DATE] = datetime.now()
        if set(self.dizio_columns) <= set(entry.keys()):
            entry[self.OL] = lang_code(entry[self.OL])
            entry[self.DL] = lang_code(entry[self.DL])
            entry[self.LEM] = entry[self.LEM].strip(" \n\t").lower()
            entry[self.TRAN] = entry[self.TRAN].strip(" \n\t").lower()
            ord_entry = {key:entry[key] for key in self.dizio_columns}
            others  =   {key:entry[key] for key in entry.keys()
                         if key not in self.dizio_columns}
            for i,old_entry in enumerate(self.lower_entries):
                if ord_entry.items() <= old_entry.items():
                    self.entries[i] = {**old_entry, **others}
                    return
            self.entries.append({**ord_entry,**others})
        else:
            raise ValueError('Missing information')
        
    def join_list(self, li):
        for item in li:
            self.append(item) 
            
    def load_csv(self, path):
        with open(path, mode='r'#, encoding="utf-8-sig"
                  ) as ts:
                reader = csv.reader(ts)
                from_csv = [{self.OL : row[0],
                             self.DL : row[1],
                             self.LEM :row[2],
                             self.TRAN : row[3]} for row in reader
                            ]
                self.join_list(from_csv)

    def load_json(self, path):
        with open(path,'r') as diz:
            di = json.load(diz)
            self.join_list(di)
    
    def load_pickle(self, path):
        with open(path,'rb') as diz:
            di = pickle.load(diz)
            self.join_list(di)
            
    def export_json(self, name):
        self.alpha_sort()
        with open(name+'.json','w') as dizio:
            json.dump(self.entries, dizio,
                      ensure_ascii=False, sort_keys=False,
                      indent=4, default = str)

    def export_pickle(self, name):
        self.alpha_sort()
        with open(name+'.p','wb') as savefile:
            pickle.dump(self.entries, savefile)

    def save(self, name):
        self.export_pickle(name)
        self.export_json(name)

    def show_list(self, sorting = "alpha"):
        if sorting == "alpha":
            self.alpha_sort()
        if sorting == "date":
            self.date_sort()
        for entry in self.entries:
            if len(entry[self.LEM]) <= 25:
                print('{}: {: <25} {}: {: <25}'.format(
                    *[entry[self.OL], entry[self.LEM],
                      entry[self.DL], entry[self.TRAN]]))
            else:
                print('{}: {}\n'.format(*[entry[self.OL], entry[self.LEM]])
                      +30*" "+
                      "{}: {}".format(*[entry[self.DL], entry[self.TRAN]]))

    def show_table(self, columns = dizio_columns):
        df = pd.DataFrame(self.entries, columns = columns)
        print(df)

    def print_everything(self):
        self.alpha_sort()
        for entry in self.entries:
            print(entry)

    def print_useful(self, excl = [DATE, STATUS]):
        self.alpha_sort()
        for entry in self.entries:
            print({k:entry[k] for k in entry.keys() if k not in excl})
            
    def add_example(self):
        lemma = input("Lemma: ")
        example = input("Example: ")
        for entry in self.entries:
            if entry[self.LEM].lower() == lemma.lower():
                if "Examples" in entry.keys():
                    entry['Examples'].append(example)
                else:
                    entry['Examples'] = []
                    entry['Examples'].append(example)
                    
        ## To do: what if there is no 'entry' with this 'lemma'?

    def add_info(self):
        lemma = input("Lemma: ")
        key = input("Key: ")
        value = input("Value: ")
        for entry in self.entries:
            if entry[self.LEM].lower() == lemma.lower():
                entry[key] = value

    def add_entry(self):
        orig = input("Original language: ")
        dest = input("Destination language: ")
        lem  = input("Lemma: ")
        trans = input("Translation: ")
        ex = [input("Example: ").strip(" \n\t")]
        if ex:
            entry = {self.OL: orig,
                     self.DL: dest,
                     self.LEM: lem,
                     self.TRAN: trans,
                     self.EX: ex}
        else:
            entry = {   self.OL: orig,
                        self.DL: dest,
                        self.LEM: lem,
                        self.TRAN: trans}
        self.append(entry)

    def delete_info(self):
        while True:
            lem = input("Insert lemma: ")
            if lem == "q": break
            indices = self.search(lem)
            if len(indices) == 0:
                print("Lemma not present")
                break
            elif len(indices) == 1:
                ind = indices[0]
            else:
                ind = input("Which one?\n")
                if ind == "q": break
                elif int(ind) not in indices:
                    raise ValueError("Wrong value")
                    break
                else: ind = int(ind)
            entry = self.entries[ind]
            print(30*"=")
            while True:
                keys = [k for k in entry.keys()
                        if k not in [self.OL, self.DL, self.LEM, self.DATE]]
                print("The following information is available:")
                for i in range(len(keys)):
                    print("{} -> {}: {}".format(*[i, keys[i]], entry[keys[i]]))
                d = input("Which one do you want to delete?\n")
                if d == "q": break
                else:
                    del entry[keys[int(d)]]
                out = input("Do you want to delete other info? Y/N\n")
                if out.lower() == "y": pass
                elif out.lower() == "n": break
                else:
                    print("Invalid input.")
                    break
            break
                
        
    def search(self, lemma, excl = [DATE, STATUS]):
        indices = []
        for index in range(len(self.entries)):
            if self.entries[index]['Lemma'].lower() == lemma.lower().strip(" \n\t"):
                indices.append(index)
                print("{}: {}".format(*[index,
                                        {k:self.entries[index][k]
                                         for k in self.entries[index].keys()
                                         if k not in excl}]))
        return indices        

    def random_translation(self):
        randentry = choice(self.entries)
        print("{}: {}".format(*[randentry[self.OL].upper(),
                                randentry[self.LEM]]
                              ))
        input()
        print("{}: {}".format(*[randentry[self.DL].upper(),
                                randentry[self.TRAN]]
                              ))
        if self.EX in randentry.keys():
            for ex in randentry[self.EX]:
                print("{}: {}".format(*[self.EX.upper(),ex]
                                      ))

            
def select_lang(diz,orig,dest):
    new_diz_entries = [entry    for entry in diz.entries
                        if entry[diz.OL] == lang_code(orig)
                        and entry[diz.DL] == lang_code(dest)]
    return Dizio(new_diz_entries)


