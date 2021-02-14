import os


from ankigenlib import txt2anki


input_path = os.path.join('txt', 'txt2anki_input.txt')
txt2anki.ankify(
    input_txt_file_name=input_path,
    target_deck='IT',
)
