import os

import card_generation


# read texts
input_text = open(os.path.join('..', 'input.txt'), 'r', encoding='utf-8').read()
non_empty_lines = [parag for line in input_text.split('\n') if (parag := line.strip())]

# print(get_sentences(input_text))
card_generation.make_cards(input_text, prefix='UIMA')
