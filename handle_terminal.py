import sys
import itertools
import collections

import re

#script, rcnn_inp, new_rcnn_out = sys.argv

def handle_terminal_sandhis(text):
    """ """
    
    updated_text = re.sub(r'(a|i|u|E)s( |-|\n|$)', r'\1H\2', text)
    updated_text = re.sub(r'ns( |-|\n|$)', r'n\1', updated_text)
    updated_text = re.sub(r'(a|u)r( |-|\n|$)', r'\1r\2', updated_text)
    
    updated_text = re.sub(r'M( |-|\n|$)', r'm\1', updated_text)
    updated_text = re.sub(r'[KgG]( |-|\n|$)', r'k\1', updated_text)
    updated_text = re.sub(r'c( |-|\n|$)', r'k\1', updated_text)
    updated_text = re.sub(r'rAj( |-|\n|$)', r'rAw\1', updated_text)
    updated_text = re.sub(r'j( |-|\n|$)', r'k\1', updated_text)
    updated_text = re.sub(r'[qQ]( |-|\n|$)', r'w\1', updated_text)
    updated_text = re.sub(r'[dD]( |-|\n|$)', r't\1', updated_text)
    updated_text = re.sub(r'[bB]( |-|\n|$)', r'p\1', updated_text)
    updated_text = re.sub(r'viS( |-|\n|$)', r'viw\1', updated_text)
    updated_text = re.sub(r'S( |-|\n|$)', r'k\1', updated_text)
    updated_text = re.sub(r'z( |-|\n|$)', r'w\1', updated_text)
    updated_text = re.sub(r'uznih( |-|\n|$)', r'uznik\1', updated_text)
    updated_text = re.sub(r'snuh( |-|\n|$)', r'snuk\1', updated_text)
    updated_text = re.sub(r'h( |-|\n|$)', r'w\1', updated_text)
    updated_text = re.sub(r'=-', r' ', updated_text)
    updated_text = re.sub(r'-$', r'', updated_text)
    
    return updated_text


def handle_anusvara(text):
    """ """
    
    updated_text = re.sub(r'M([kKgGN])', r'N\1', text)
    updated_text = re.sub(r'M([cCjJY])', r'Y\1', updated_text)
    updated_text = re.sub(r'M([wWqQR])', r'R\1', updated_text)
    updated_text = re.sub(r'M([tTdDn])', r'n\1', updated_text)
    updated_text = re.sub(r'M([pPbBm])', r'm\1', updated_text)
    
    return updated_text


def handle_sa(text):
    """ """
    
    updated_text = re.sub(r'^sa ', 'saH ', text)
    updated_text = re.sub(r';sa ', ';saH ', updated_text)
    updated_text = re.sub(r' sa ', ' saH ', updated_text)
    updated_text = re.sub(r'^eza ', 'ezaH ', updated_text)
    updated_text = re.sub(r';eza ', ';ezaH ', updated_text)
    updated_text = re.sub(r' eza ', ' ezaH ', updated_text)
    
    return updated_text

