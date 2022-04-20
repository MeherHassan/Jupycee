from IPython.core.ultratb import AutoFormattedTB
from IPython.core.display import display, HTML
import re
import requests
from sty import fg, bg, ef, rs
from bs4 import BeautifulSoup

itb = AutoFormattedTB(mode = 'Plain', tb_offset = 1)


def custom_exc(shell, etype, evalue, tb, tb_offset=None):
    

    # Default msg
    #shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

    
    stb = itb.structured_traceback(etype, evalue, tb)
    sstb = itb.stb2text(stb)
   
    print (sstb) 
    errorName = str(etype)
    fullSentence = str(evalue)
    elist = re.findall("\'(.*?)\'",errorName)
    print("-------------------------------------------------------------------")
    print("Result Obtained from Official Python Documentation Using JUPYCEEDOC\n")
    print("-------------------------------------------------------------------")
    print(elist[0])  
    
    textMsg = souper(elist[0])
    display(HTML(textMsg))
    substring = "subclass of"
    if substring in textMsg:
        mainclass = textMsg.split(substring,1)[1].split()[0]
        mainclass = mainclass.replace(" ","")
        mainclass = mainclass.replace(".","")
        print(mainclass)
        textMsg = souper(mainclass)
        display(HTML(textMsg))
    
    check,texted = hints(elist[0])
    
    if(check):
        printext = bg.yellow + "You may also check this Hint" + bg.rs
        print(printext)
        fullTexts = str(sstb)
        lineNum = fullTexts.split("line",1)
        elist = re.findall("\,(.*?)\,",fullTexts)
        quoted = re.findall("\'(.*?)\'",fullSentence) 
        if(len(quoted)>0):
            printext = bg.yellow + quoted[0] + bg.rs
            texted=texted.replace("<missing>",printext)
            
        printexts = bg.yellow + elist[0] + bg.rs
        texted = texted.replace("<line>", printexts)
        print(texted)
        
    
    
    
get_ipython().set_custom_exc((Exception,), custom_exc)

def souper(error):
    with open('exceptions.html', 'r', encoding='utf-8') as f:
        contents = f.read()
  
    soup = BeautifulSoup(contents, 'html.parser')
    
    allSoup = soup.find("dt", {"id": error})
    
    texts = allSoup.findParent().text
    
    return texts

def hints(error):
    
    
    HINT_MESSAGES = {
        "KeyError": (
            " KeyError exceptions are raised to the user when a key is not found in a dictionary."
            "\nTo solve this error you may want to define a key with value <missing> in the dictionary."
            "\nOr you may want to use the method .get() of a dictionary which can retrieve the value associated"
            "\nto a key even when the key is missing by passing a default value."
            "\nExample:\n\nfoo = your_dict.get('missing_key', default='bar')"
        ),
        "NameError": (
            "A variable named '<missing>' is missing."
            "\nMaybe you forget to define this variable or even you accidentally misspelled its actual name?"
        ),
        "ModuleNotFoundError": (
            "A module (library) named '<missing>' is missing."
            "\nYou might want to check if this is a valid module name or"
            "\nif this module can be installed using pip like: 'pip install <missing>'"
        ),
        "IndexError": (
            "You tried to access an index that does not exist in a sequence at <line>."
            "\nAn IndexError happens when asking for non existing indexes values of sequences."
            "\nSequences can be lists, tuples and range objects."
            "\nTo fix this make sure that the index value is valid."
        ),
        "SyntaxError": (
            "You have a syntax error somewhere around line <line>"
            "\nGenerally, syntax errors occurs when multiple code statements are interpreted as if they were one."
            "\nThis may be caused by several simple issues, below is a list of them."
            "\nYou should check if your code contains any of these issues."
            "\n"
            "\n1- Make sure that any strings in the code have matching quotation marks."
            "\n2- An unclosed bracket – (, {, or [ – makes Python continue with the next line as part of the current statement."
            "\n   Generally, an error occurs almost immediately in the next line."
            "\n3- Make sure you are not using a Python keyword for a variable name."
            "\n4- Check that you have a colon at the end of the header of every compound statement,"
            "\n   including for, while, if, and def statements."
            "\n5- Check for the classic '=' instead of '==' in a conditional statement."
            "\nSource: https://www.openbookproject.net/thinkcs/python/english2e/app_a.html"
        ),
        "ZeroDivisionError": (
            "You have tried to divide a number by zero around line <line>"
            "\nCheck the division operation to find the error."
            "\nDivision operations where the divisor is generate by a range() can throw this error if the range() starts "
            "at 0. "
        ),
    }
    
    if(error in HINT_MESSAGES):
        
        return True, HINT_MESSAGES[error]
    else:
        em = ""
        return True, em