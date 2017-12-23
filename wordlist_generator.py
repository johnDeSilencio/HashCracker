import os
import re

def getListOfTextFiles():
    list_of_files = []
    for file in os.listdir("books/"):
        if file.endswith(".txt"):
            list_of_files.append(os.path.join("books/", file))
    return list_of_files

def generateWordlistFrom(filename):
    wordlist = dict()
    with open(filename,'r') as file:
        for line in file:
            for word in line.split():
                word_without_symbols = re.sub(r"[^A-Za-z]+", '', word)
                word_without_symbols = word_without_symbols.lower()
                if word_without_symbols not in wordlist:
                    wordlist[word_without_symbols] = 1
                else:
                    wordlist[word_without_symbols] += 1
    return wordlist

def sort(wordlist):
    # Need a way to sort the wordlist based upon the number of word occurrences.
    # This is my algorithm for now, but the sorting could be made a lot more efficient.
    ordered_wordlist = []
    
    for current_word in wordlist:
        for checking_word_index in xrange(0, len(ordered_wordlist)):
            checking_word = ordered_wordlist[checking_word_index]
            if current_word[1] > checking_word[1]:
                ordered_wordlist.insert(checking_word_index, current_word)
                break
            if checking_word_index is len(ordered_wordlist) - 1:
                ordered_wordlist.append(current_word)
        if len(ordered_wordlist) is 0:
            ordered_wordlist.append(current_word)
    return ordered_wordlist

def write(list):
    with open('wordlist.txt', 'a') as file:
        file.write("WORD -- OCCURENCES\n")
        for key_value_pair in list: 
            file.write("%s %d\n" % (key_value_pair[0], key_value_pair[1]))
    
ordered_wordlist = []
key_value_pairs = generateWordlistFrom("books/thejungle.txt").items()
ordered_wordlist = sort(key_value_pairs)
write(ordered_wordlist)