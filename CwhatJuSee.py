# -*- coding: UTF-8 -*-
import sys
import os
import glob
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import codecs
import sys



if len(sys.argv) != 3:
    sys.exit("Make sure you specified input file and output directory like:\npython  CwhatJuSee.py  ipynb_file  output_dir")
input_file = sys.argv[1]
output_dir = os.path.join(os.getcwd(), sys.argv[2])

print("input_file", input_file)
print("output_dir", output_dir)

def run(command):
    stdout, stderr = Popen(command.split(), stdout=PIPE,
                           stderr=PIPE, stdin=PIPE).communicate(input='a\n')
    print(stdout)
    print(stderr)

def remove_inputs_cell(output_dir):
    with open(output_dir, 'r') as f:
        html_source = f.read()
        soup = BeautifulSoup(html_source.replace(
            "class=\"container\"", ""), "html.parser")
    usless_clase = ["prompt input_prompt", "input_area", "prompt",
                    "output_subarea output_stream output_stderr output_text"]
    for ele in usless_clase:
        for div in soup.find_all('div', class_=(ele)):
            div.decompose()
    with codecs.open(output_dir, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


#-- too easy to be a class --    
print("converting ipynb file " + input_file)
run("""jupyter nbconvert --ExecutePreprocessor.timeout=3600 --to html --execute %s --output-dir %s""" % (input_file, output_dir))
# print "removing input cells of " + output_dir + os.path.basename(input_file)[:-5] + "html"
remove_inputs_cell(output_dir +"/"+os.path.basename(input_file)[:-5] + "html")
print("Done!!")
