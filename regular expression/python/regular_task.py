import sys
import os
import re
import pprint
import pandas as pd



# Handling email expression
first_regular = '(\w+\s?([.]\w+)?(at|WHERE|@|&#x40;)\s?\w+\.?( DOM | dot |;)?\w+\.?( dot | DOM | dt|;)?\w+)'
second_regular = '(([\w\.-]+)\s?(@|%20at%20| at | where )\s?(stanford|-s-t-a-n-f-o-r-d-|gradiance)(\.|%20dot%20| dot | dom | dt )(edu|-e-d-u|com))'
third_regular = '(([\w\.]+)\s?\(followed? ?by? ?(\"|&ldquo;)@(cs\.)?stanford.edu?(\"|&rdquo;)\))'
fourth_regular = '((obfuscate|pal) ?(\(\')?\w+\.? ?\w+(\',\')? ?\w+ ?\w+(\'\);)?)'


# Handling phone expression
fifth_regular = '[\d]{3}-[\d]{3}-[\d]{4}'
six_regular = '[(][\d]{3}[)] ?[\d]{3}-[\d]{4}'
seven_regular = '[+][0-9] ?[(]?[\d]{3}[)]? [\d]{3}[-| ][\d]{4}'




'''
    phone numbers functions
'''
def clean_number(m):
    '''
        A function used to clean the numbers to be in form of 123-123-1234
        it is take a number in string way convert it to be a list
        then work on and return as string using join built-in function
    '''
    m = list(m)
    m.reverse()
    strs  = ""
    for indx, c in enumerate(m):
        if c == '-' or c == ' ' or c == '(' or c == ')'  or c == '+':
            continue 
        if int(m[indx]) >=0 and int(m[indx]) <= 9:
            strs = strs + m[indx]
        if len(strs) == 4 or len(strs) == 8:
            strs +='-'
        if len(strs) == 12:
            break
    return strs[::-1]



# mail funcitons 
def common_cases(m):
    '''
        This function is helful to dealing with some casses of has more spaces or taps between  words of mail
        like abdo   @ yahoo.
        com
        also some cases has a ; at end of the word like .edu; others like - or "
        other wise we git the char of th word
        return string at end of the function
    '''
    ret = ''
    spaces = ' \t\n-%'
    for indx, c in enumerate(m):
        if c ==' ' or c == '-' or c == '"' or c in spaces:
            ret+=''
        elif c == '(' or c== ')':
            ret +=''
        elif c == ';':
            ret +='.'
        else:
            ret +=c
    return ret


def clean_at_again(text):
    '''
        this function is general handle of different cases of words like dot, 
        DOM  and other like &#x40; and others
        return at the to another function that handle spaces and small things
    '''
    if "%20at%20" in text:
        text = text.split('%20')
    elif ' at ' in text:
        text = text.split(' ')
    elif ' WHERE ' in text:
        text = text.split(' ')
    elif ' WHERE ' in text:
        text = text.split(' ')
    elif '-@-' in text:
        text = text.split('-')
    elif '&#x40;' in text:
        text = text.partition('&#x40;')
    '''
        a partition is a function that search for something 
        and return with a tuple of 3 element 
        1 - everything before the "match" 
        2 - the "match" 
        3 - everything after the "match"
    '''
    ret = ''
    for word in text:
        if word == "dot" or word == "dt" or word == "DOM":
            ret +='.'
        elif word == "at" or word == "WHERE" or word == "&#x40;":
            ret +='@'
        else: ret +=str(word)
    return common_cases(ret)


def handle_stanford_without_dots(text):
    '''
        this function handle some cases of stanfordedu to be stanford.edu and cs
        so cases need to add . to be as formed e-mail we saw in general
    '''
    if 'cs' in text:
        if not 'cs.' in text:
            text = text.replace('cs', 'cs.')
    if 'stanford' in text:
        if not 'stanford.' in text:
            text = text.replace('stanford', 'stanford.')
    return text



def followed_by_handle(text):
    '''
        this function handle some cases of differnt cases like below we need to handle it
        to be as a genral mail at the end
    '''
    text = common_cases(text)
    if "followedby" in text or "&ldquo." in text  or "&rdquo." in text or 'obfuscate\'' in text:
        text = text.replace("followedby", '')
        text = text.replace("&ldquo.", '')
        text = text.replace("&rdquo.", '')
        text = text.replace("obfuscate\'", '')
        text.replace('at', '@')
    if 'jurafsky' in text:
        text = 'jurafsky@' + text.replace('jurafsky', 'stanford.edu')
    if 'at' in text:
        text = text.replace('at', '@')
    text = text.partition('\'')
    text = text[0]
    text = handle_stanford_without_dots(text)
    return text





def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        matches = re.findall(first_regular,line)
        for m in matches:
            m = clean_at_again(m[0])
            if len(m) > 0 and '.' in m and m.count('@') == 1:
                res.append((name, 'e', m))

        matches = re.findall(second_regular,line)
        for m in matches:
            m = clean_at_again(m[0])
            res.append((name, 'e', m))

        matches = re.findall(third_regular,line)
        for m in matches:
            m = followed_by_handle(m[0])
            res.append((name, 'e', m))

        matches = re.findall(fourth_regular,line)
        for m in matches:
            m = followed_by_handle(m[0])
            if len(m) > 0 and '.' in m and m.count('@') == 1:
                res.append((name, 'e', m))
        '''
            numbers handling process
        '''
        matches = re.findall(fifth_regular,line)
        matches.extend(re.findall(six_regular,line))
        matches.extend(re.findall(seven_regular,line))
        for m in matches:
            m = clean_number(m)
            res.append((name,'p',m))
    return res

