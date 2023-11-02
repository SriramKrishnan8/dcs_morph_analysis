import os
import subprocess as sp
import re

svaras = "aAiIuUqQLeEoO"
natva_permissing_letters = svaras + "MkKgGfpPbBmyrvRh"
#natva_permissing_letters = "aAiIuUqQLeEoOMkKgGfpPbBmyrvRh"
natva_inhibiting_letters = "cCjJFtTdDNwWxXnlsS"

second_solution_pairs_iast = [('t', 'h'), ('ḥ', 's'), ('k', 'h'), ('ṭ', 's')]
second_solution_pairs_wx = [('w', 'h'), ('H', 's'), ('k', 'h'), ('t', 's')]

list_of_preverbs = [
    "A", "aBi", "anu", "api", "ava", "awi", "aXi", "ni", "nis", "pari",
    "pra", "prawi", "sam", "su", "upa", "ux", "vi", "xus", "parA", "ku",
    "niH", "nir", "saw", "asaw", "apa", "Afa", "Af", "UrI", "xur"
]

def natva_inhibited(aft_r):
    index_n = aft_r.find("n")
    if (index_n == (len(aft_r) - 1)):
        return (True, index_n)
    if index_n == -1:
        return (False, index_n)
    bef_n = aft_r[:index_n]
    bef_n_status = [False]
    bef_n_status = [True for (i,v) in enumerate(bef_n) if (v in natva_inhibiting_letters)]
    status = True if (True in bef_n_status) else False
    return (status, index_n)

def natva_status(first, second, letter):
    if (letter in first):
        index_r = first.rfind(letter)
        aft_r = first[(index_r + 1):]
        (status, index) = natva_inhibited(aft_r)
        if status:
            return (first, second)
        if ("n" in second):
            (status, index) = natva_inhibited(second)
            if not status:
                second = second[:index] + "N" + second[(index + 1):]
    return (first, second)
    
def natva(first, second):
    (first, second) = natva_status(first, second, "r")
    (first, second) = natva_status(first, second, "R")
    (first, second) = natva_status(first, second, "q")
    (first, second) = natva_status(first, second, "Q")
    (first, second) = natva_status(first, second, "L")
    return (first, second)

def get_sandhied_form(first, second, natva_needed = True):
    if ((not (first == "")) and (not (second == ""))):
        if ((first == "an") and (second[0] in svaras)):
            result_list = [str(first + second)]
            return result_list
            
        if natva_needed:
            (first, second) = natva(first, second)

        cur_wd = os.getcwd()
        sandhi_file = os.path.join(cur_wd, 'sandhi/sandhi.pl')
        
        p = sp.Popen(['perl', sandhi_file, first, second], stdout=sp.PIPE)
#        p = sp.Popen(['perl', 'sandhi/sandhi.pl', first, second], stdout=sp.PIPE)
        result = (p.communicate()[0]).decode('utf-8')
        
#        print(first, second, result)
        
        result_string = re.search(r':?(.*?),', result).group(1)
        result_list = result_string.split(':')
        return result_list
    else:
        if (first == ""):
            return [second]
        elif (second == ""):
            return [first]
        else:
            return []
            
def sandhi_join(first, second, internal):
    internal = True if ((not internal) and (first in list_of_preverbs)) else internal
    sandhied_word_list = get_sandhied_form(first, second, internal)

    if (len(sandhied_word_list) == 0):
        return (first + second)
    else:
        sandhied_word = ""
        if (first == "") or (second == ""):
            sandhied_word = sandhied_word_list[0]
        elif (first[-1],second[0]) in second_solution_pairs_wx:
            sandhied_word = sandhied_word_list[1]
        else:
            sandhied_word = sandhied_word_list[0]
        
        sandhied_word = sandhied_word.replace("><", "H")
        sandhied_word = sandhied_word.replace("  ", " ")
        
        return sandhied_word.strip()
    

