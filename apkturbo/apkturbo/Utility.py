import os
def concaturl():
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'keywords.txt')),'r');
    f_contents = f.read();
    f_contents = f_contents.rstrip();
    list_keywords = f_contents.split('|');
    return list_keywords;


