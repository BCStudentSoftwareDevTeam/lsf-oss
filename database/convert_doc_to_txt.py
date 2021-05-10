import os

positionPath = 'positions/chemistry'

for root, dirs, files in os.walk(positionPath, topdown=False):

    for name in files:
        joined = os.path.join(root, name)
        input_word_file = str(joined)
        output_text_file = input_word_file.split(".", 1)[0] + ".txt"
        os.system('antiword %s > %s' % (input_word_file, output_text_file))
