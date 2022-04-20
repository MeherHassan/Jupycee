from IPython.core.ultratb import AutoFormattedTB
from IPython.core.display import display, HTML
import re
import requests
from sty import fg, bg, ef, rs
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


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
    json1 = make_request(elist[0],fullSentence)

    if(json1 !="NA"):
        
        url,que,ans = get_urls(json1)
        printext = bg.yellow + "Answer Found" + bg.rs
        print(printext)
        print("Url is "+url[0])
        print("Que id is "+str(que[0]))
        print("Ans id is "+str(ans[0]))

        x=str(que[0])
        z=ans[0]
        y=make_request_ques(x)
        for i in y['items']:
            if(i['answer_id']==z):
                printext = bg.yellow + "Un-summarised Answer is" + bg.rs
                print(printext)
                display(HTML(i['body']))
                a=re.split(r'[.!?]+', i['body'])
                if(len(a)>5):
                    printext = bg.yellow + "Summarised Answer is" + bg.rs
                    print(printext)
                    # For Strings
                    stopWords = set(stopwords.words("english"))
                    words = word_tokenize(i['body'])
                    freqTable = dict()
                    for word in words:
                        word = word.lower()
                        if word in stopWords:
                            continue
                        if word in freqTable:
                            freqTable[word] += 1
                        else:
                            freqTable[word] = 1
                    sentences = sent_tokenize(i['body'])
                    sentenceValue = dict()

                    for sentence in sentences:
                        for word, freq in freqTable.items():
                            if word in sentence.lower():
                                if sentence in sentenceValue:
                                    sentenceValue[sentence] += freq
                                else:
                                    sentenceValue[sentence] = freq
                    sumValues = 0
                    for sentence in sentenceValue:
                        sumValues += sentenceValue[sentence]

                    # Average value of a sentence from the original text

                    average = int(sumValues / len(sentenceValue))

                    # Storing sentences into our summary.
                    summary = ''
                    for sentence in sentences:
                        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                            summary += " " + sentence
             
                    display(HTML(summary))
                else:
                    printext = bg.green + "No Summarisation needed due to less sentences found in the answer" + bg.rs
                    print(printext)
                    
    else:
        print("No Answer Found In stackOverFlow For This Erorr")
        
    
    
    stb = itb.structured_traceback(etype, evalue, tb)
    sstb = itb.stb2text(stb) 
    errorName = str(etype)
    fullSentence = str(evalue)
    elist = re.findall("\'(.*?)\'",errorName)
    print("----------------------------------------------------------------------")
    print("----------------------------------------------------------------------")
    print("2. Result Obtained from Official Python Documentation Using JUPYCEEDOC\n")
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

def make_request(name,fullS):
    
    allQuery = name + ": " + fullS
    #print(name)
    #print(fullS)
    print("---------------------------------------")
    print("Combined results obtained using EJUPYCEE\n")
    print("---------------------------------------------------")
    print("---------------------------------------------------")
    print("1. Result Obtained from StackOverflow Using JUPYCEE\n")
    print("--------------------------------------------------")
    printext = fg.green + "Searching for "+allQuery+ fg.rs
    print(printext)
    resp  = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=votes&tagged=python&intitle={}&site=stackoverflow".format(allQuery))
    respJson = resp.json()
    if(len(respJson['items'])==0):
        
        printext = fg.red + "No search result found for"+ allQuery + fg.rs
        print(printext)
        printext = fg.green + "Searching for "+fullS + fg.rs
        print(printext)
        resp  = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=votes&tagged=python&intitle={}&site=stackoverflow".format(fullS))
        respJson = resp.json()
        
    if(len(respJson['items'])==0):
        printext = fg.red + "No search result found for: "+fullS + fg.rs
        print(printext)
        printext = fg.green + "Searching for: "+name + fg.rs
        print(printext)
        resp  = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=votes&tagged=python&intitle={}&site=stackoverflow".format(name))
        respJson = resp.json()
        
    if(len(respJson['items'])==0):
        printext = fg.red + "No search result found for: "+name + fg.rs
        print(printext)
        print("Ending Search")
        print(respJson)
        respJson = "NA"
        
    return respJson

def make_request_ques(idq):
    resp  = requests.get("https://api.stackexchange.com/"+"/2.2/questions/{}/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody".format(idq))
    return resp.json()


def get_urls(json_dict):
    url_list = []
    ans_list = []
    que_list = []
    count = 0
    
    for i in json_dict['items']:
        if("accepted_answer_id" in i):
            url_list.append(i["link"])
            ans_list.append(i["accepted_answer_id"])
            que_list.append(i["question_id"])
            count+=1
        if count == len(i) or count == 100:
            break
    return url_list,que_list,ans_list



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