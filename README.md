# Morphological Analysis from Digital Corpus of Sanskrit (DCS)

DCS ([Digital Corpus of Sanskrit](http://www.sanskrit-linguistics.org/dcs/)) hosts more than 650,000 sentences with lexical and morphological annotations. This package provides the morphological analyses of given word(s). These have already been extracted from DCS' repository and converted to the format identical to [Sanskrit Heritage Platform's analysis](www.sanskrit.inria.fr/DICO/reader.fr.html).

The following are the contents of the package:

1. rv\_analysis\_map.tsv &rarr; contains a list of tuples with word and its DCS analysis, where the words are from rigveda
2. av\_analysis\_map.tsv &rarr; contains a list of tuples with word and its DCS analysis, where the words are from atharvaveda
3. get\_dcs\_sh\_morph.py &rarr; compares the given word(s) with the available list of words for getting the morphological analysis
4. handle\_terminal.py &rarr; DCS does not handle terminal sandhis for certain words. In such cases, the mapping might be missed out and hence this script helps in handling the terminal sandhis
5. input\_words.tsc &rarr; A sample list of words for testing
6. sandhi &rarr; contains files from the [sandhi-joiner package](https://github.com/SriramKrishnan8/scl_sandhi_interface.git) that perform sandhi operation over the components of compounds or words separated by a hyphen ("-"). This helps in handling words from the Vedic pada-patha.

<!--In addition to these, the [sandhi-joiner package](https://github.com/SriramKrishnan8/scl_sandhi_interface.git) has to be fed to the script to perform sandhi operation over the components of compounds or words separated by a hyphen ("-"). This helps in handling words from the Vedic pada-patha.-->


## The Process

DCS stores its analyses in CoNLL-U format. These are converted to the Sanskrit Heritage's representation of morphological analyses. And then this package helps in checking the analysis of words.

1. Extracting morphological analyses from DCS by parsing the CoNLL-U files &rarr; list of words and their morphological analyses
2. Conversion of morphological analyses from CoNLL-U format to SH representation &rarr; mapping file
3. Lookup of the given word(s) in the mapping file

## Pre-requisites

1. devtrans
2. tqdm
```
pip3 install devtrans tqdm
```

## Execution

```
python3 get_dcs_sh_morph.py rv_analysis_map.tsv input_words.tsv dcs_sh_output.tsv
```

### Input / Output

Input:

1. rv\_analysis\_map.tsv &rarr; the mapping file extracted from DCS and generated from its analyses
2. input\_words.tsv &rarr; newline separated words
3. dcs\_sh\_output.tsv &rarr; resultant list of JSON entries corresponding to the words

(NOTE: the scripts for parsing the CoNLL-U format and extracting the morphological analyses will be added soon.)
