import sys
import os
import json
from tqdm import tqdm

import devtrans as dt

from sandhi import transliteration as tl
from sandhi import sandhi_words as sw

import handle_terminal as ht

script, dict_, cl, out_ = sys.argv

def open_contents(file_n):
    
    file_ = open(file_n, "r", encoding="utf-8")
    text = file_.read()
    file_.close()
    lines = list(filter(None, text.split("\n")))
    
    return lines
    

def handle_terminal_sandhis(word):
    
    slp_word = dt.dev2slp(word)
    new_word = ht.handle_terminal_sandhis(slp_word)
    new_word_dev = dt.slp2dev(new_word)
    
    return new_word_dev


def get_dict(file_n):
    
    lines = open_contents(file_n)
    
    w_dict = {}
    
    print("Generating Mapping Dictionary...")
    for i in tqdm(range(len(lines))):
        item = lines[i]
        split_item = item.split("\t")
        word = split_item[0]
        new_word = handle_terminal_sandhis(word)
        w_dict[word] = split_item[1]
        if new_word not in w_dict:
            w_dict[new_word] = split_item[1]
    
    return w_dict


def process_wrds(wrd, words_dict):
    
    new_dict = {}
    
    if wrd in words_dict:
        status = "success"
        new_dict = json.loads(words_dict[wrd])
    else:
        status = "unrecognized"
        new_dict["input"] = wrd
        new_dict["status"] = status
    
    return wrd, new_dict, status
    

def process_morph(morph_dict_list):
    """ """

    new_morph_dict_list = []

    for item in morph_dict_list:
        word = item["word"]
        
        processed_dict = item.copy()
        processed_dict["word"] = word if "-" in word else (word + "-")

        new_morph_dict_list.append(processed_dict)

    return new_morph_dict_list
    


def process_compositional(wrd, words_dict):
    
    components = wrd.split("-")
    
    new_mrph_lst = []
    
    comp_len = len(components)
    for comp in components:
        if comp in words_dict:
            comp_len = comp_len - 1
            tmp_dict = json.loads(words_dict[comp])
            if comp_len == 0:
                processed_dict_list = tmp_dict["morph"]
            else:
                processed_dict_list = process_morph(tmp_dict["morph"])
            
            new_mrph_lst = new_mrph_lst + processed_dict_list
        else:
            break
        
    if comp_len == 0:
        status = "success"
    else:
        status = "unrecognized"
    
    return wrd, new_mrph_lst, status


def process_non_compositional(wrd, words_dict):
    
    components = wrd.split("-")
    
    new_mrph_lst = []
    
    sandhied_compound = ""
    for comp in components:
        comp = tl.input_transliteration(comp.strip(), "DN")[0]
        sandhied_compound = sw.sandhi_join(sandhied_compound, comp, False)
    
    sandhied_compound_dev = tl.output_transliteration(sandhied_compound, "deva")[0]
    
    if sandhied_compound_dev in words_dict:
        tmp_dict = json.loads(words_dict[sandhied_compound_dev])
        new_mrph_lst = tmp_dict["morph"]
        status = "success"
        word = sandhied_compound_dev
    else:
        status = "unrecognized"
        word = wrd
    
    return word, new_mrph_lst, status


def process_cpds(wrd, words_dict):
    
    new_word, new_mrph_lst, status = process_compositional(wrd, words_dict)
    if (status == "unrecognized") and ("-इव" not in wrd):
        new_word, new_mrph_lst, status = process_non_compositional(wrd, words_dict)
    
    new_dict = {}
    
    new_dict["input"] = new_word
    new_dict["status"] = status
    
    if status == "success":
        new_dict["segmentation"] = [ new_word ]
        new_dict["morph"] = new_mrph_lst
    
    return new_word, new_dict, status
    

def process_terms(wrd, words_dict):
    """ """
    
    if " " in wrd:
        new_dict = {}
        new_dict["input"] = wrd
        new_dict["status"] = "error"
        status = "error"
        new_word = wrd
    elif "-" in wrd:
        new_word, new_dict, status = process_cpds(wrd, words_dict)
    else:
        new_word, new_dict, status = process_wrds(wrd, words_dict)
    
    return new_word, new_dict, status


cl_lines = open_contents(cl)
words_dict = get_dict(dict_)

new_analysis_lst = []

print("Fetching Analysis...")
for i in tqdm(range(len(cl_lines))):

    ln = cl_lines[i]
    
    wrd_lst = ln.split("\t")
    
    status = "unrecognized"
    
    wrd_done = []
    for wrd in wrd_lst:
        if (wrd == "") or (wrd in wrd_done) or (not (status == "unrecognized")):
            continue
        new_word, new_dict, status = process_terms(wrd, words_dict)
        wrd_done.append(wrd)
    
    # Not using the word and status separately temporarily
#    new_analysis = "\t".join((new_word, str(new_dict), status))
    new_analysis = json.dumps(new_dict, ensure_ascii=False)
        
    new_analysis_lst.append(new_analysis)

new_prt_str = "\n".join((new_analysis_lst))
output_file = open(out_, "w", encoding="utf-8")
output_file.write(new_prt_str)
output_file.close()

