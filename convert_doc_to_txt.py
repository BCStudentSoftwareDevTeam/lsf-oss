# import os
#
# input_word_file = "LeadStudentProgrammerWLS5.doc"
# output_text_file = "output_file.txt"
# os.system('antiword %s > %s' % (input_word_file, output_text_file))

f = open("output_file.txt", "r")
print(f.read())
