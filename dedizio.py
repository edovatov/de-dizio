from dizio import *

def import_german_nouns():
    '''Imports a list of German nouns as [lemma, gender, plural]'''
    with open("simple_nouns_table.csv", "r", encoding = "utf8") as nouns:
        reader = csv.reader(nouns)
        list_of_german_nouns = []
        for row in reader:
            list_of_german_nouns.append(row[:])
        return list_of_german_nouns

__list_of_german_nouns = import_german_nouns()

def german_noun_analysis(string):
    ''' Input: string (german word)
        Output: if the word is a german noun, returns a tuple (gender, plural)'''
    for row in __list_of_german_nouns:
        if row[0].lower() == string.lower(): return (row[1],row[2])
    return (None, None)

class DEDizio(Dizio):
    
    GEN = "Gender (w.n.)"
    PLUR = "Plural (w.n.)"
    status = "status"
    
    def __init__(self, iniz=[]):
        filtered_iniz = [entry for entry in iniz
             if set(entry.keys())>=set([self.OL, self.DL])
             and lang_code(entry[self.OL]) == 'DE'
             and lang_code(entry[self.DL]) == 'EN'
            ]
        Dizio.__init__(self)
        Dizio.join_list(self, filtered_iniz)
    
    @property
    def twocols(self):
        return [{'DE':entry[self.LEM], 'EN':entry[self.TRAN]}
                for entry in self.entries]

    @property
    def nouns(self):
        return [entry for entry in self.entries if self.isparsednoun(entry)]

    def isparsednoun(self, entry):
        return self.GEN in entry.keys()
        
    def parse_nouns(self):
        unparsed = [entry for entry in self.entries
                    if "parsed" not in entry.values()]
        for entry in unparsed:
                gender,plural = german_noun_analysis(entry[self.LEM])
                if gender:
                    entry[self.LEM] = entry[self.LEM]
                    entry[self.GEN] = gender
                    entry[self.PLUR] = plural
                else: entry[self.LEM] = entry[self.LEM].lower()
                entry[self.status] = "parsed"

    def print_useful(self, excl = [Dizio().DATE, "status"]):
        Dizio.print_useful(self, excl)
        
    def gn_with_article(self,entry):
        if self.isparsednoun(entry):
            if entry[self.GEN] == 'm': return "der"
            if entry[self.GEN] == 'f': return "die"
            if entry[self.GEN] == 'n': return "das"
        else: raise ValueError("Not a noun")

    def random_translation(self):
        randentry = choice(self.entries)
        if self.isparsednoun(randentry):
            print("{}: {} {}".format(*[randentry[self.OL].upper(),
                                self.gn_with_article(randentry),
                                randentry[self.LEM].capitalize()]
                              ))
        else:
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
                
    def random_noun(self):
        rand_noun = choice(self.nouns)
        sing_art = self.gn_with_article(rand_noun)
        print("{}: {}".format(*["NOUN",
                                rand_noun[self.LEM].capitalize()]
                              ))
        input()
        if self.PLUR in rand_noun.keys() and bool(rand_noun[self.PLUR]):
            print("WITH ARTICLE: {0} {1}, die {2}".format(*[
                            sing_art,
                            rand_noun[self.LEM].capitalize(),
                            rand_noun[self.PLUR].capitalize()
                            ]))        
        else:
            print("WITH ARTICLE: {0} {1}".format(*[
                            sing_art,
                            rand_noun[self.LEM].capitalize()
                            ]))
        print("TRANSLATION: {}".format(*[rand_noun[self.TRAN]]))
        if self.EX in rand_noun.keys():
            for ex in rand_noun[self.EX]:
                print("{}: {}".format(*[self.EX.upper(),ex]
                                      ))

    def exercise(self, kind = "translations", number = 10):
        if kind.lower() == "translations":
            for i in range(number):
                self.random_translation()
                print("\n"+30*"=")
                if input()=='q': break
        elif kind.lower() == "nouns":
            for i in range(number):
                self.random_noun()
                print("\n"+30*"=")
                if input()=='q': break
        else: raise ValueError("Unknown exercise type")

