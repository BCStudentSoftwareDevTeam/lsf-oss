import os
import docx2txt

positionPath = 'positions/chemistry' #TODO

for root, dirs, files in os.walk(positionPath, topdown=False):

    for name in files:
        joined = os.path.join(root, name)
        input_word_file = str(joined)
        output_text_file = input_word_file.split(".", 1)[0] + ".txt"
        type_word_file = input_word_file.split(".", 1)[1]

        if type_word_file == "doc":
            os.system('antiword %s > %s' % (input_word_file, output_text_file))

        elif type_word_file == "docx":
            input_docx = docx2txt.process(input_word_file)
            with open(output_text_file, "w") as text_file:
                print(input_docx, file=text_file)
