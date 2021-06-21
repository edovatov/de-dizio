from dizio import *

dizio = Start()
tod_diz = Dizio()

def save_tod_diz():
    dizio.join_list(tod_diz.entries)
    tod_date = datetime.today().strftime('%Y-%m-%d')
    dizio.save(tod_date+"_dizio")

while True:
    lemma = input("LEMMA: ")
    if lemma == "q": break
    trans = input("TRANSLATION: ")
    if trans == "q": break
    example = input("EXAMPLE: ")
    if example == "q": break
    else:
        if example:
            tod_diz.append({
                tod_diz.OL : "DE",
                tod_diz.DL : "EN",
                tod_diz.LEM : lemma,
                tod_diz.TRAN : trans,
                "Examples" : [example]
                })
        else:
            tod_diz.append({
                tod_diz.OL : "DE",
                tod_diz.DL : "EN",
                tod_diz.LEM : lemma,
                tod_diz.TRAN : trans,
                })
    print(30*"=")
