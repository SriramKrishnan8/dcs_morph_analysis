# To fetch the analyses of words

echo "Extracting DCS Rigveda Analysis..."
python3 get_dcs_sh_morph.py rv_analysis_map.tsv input_words.tsv output_rv.tsv

echo "Extracting DCS Atharvaveda Analysis..."
python3 get_dcs_sh_morph.py av_analysis_map.tsv input_words.tsv output_av.tsv

echo "Done."