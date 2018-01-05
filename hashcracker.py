import hashlib
from time import time
import sys

NUMBER_OF_HASHES = 0L
NUMBER_OF_ROOTPASSWORDS_CHECKED = 0L
SYSTEM_START_TIME = 0
SYSTEM_CURRENT_TIME = 0

def printStatistics():
    global NUMBER_OF_HASHES
    global NUMBER_OF_ROOT_PASSWORDS_CHECKED
    hashesPerSecond = getHashesPerSecond()
    rootPasswordChecksPerSecond = getRootPasswordChecksPerSecond()
    statistics = "# Hashes: %0.f HPS: %0.f # Root Passwords Checked: %0.f RPCPS: %0.f" % (NUMBER_OF_HASHES, hashesPerSecond, NUMBER_OF_ROOTPASSWORDS_CHECKED, rootPasswordChecksPerSecond)
    print statistics,
    sys.stdout.flush()
    print '\r'*5*len(statistics),

def getRootPasswordChecksPerSecond():
    global NUMBER_OF_ROOTPASSWORDS_CHECKED
    global SYSTEM_CURRENT_TIME 
    global SYSTEM_START_TIME
    SYSTEM_CURRENT_TIME = time()
    try:
        return NUMBER_OF_ROOTPASSWORDS_CHECKED / (SYSTEM_CURRENT_TIME - SYSTEM_START_TIME)
    except ZeroDivisionError:
        return 0
    
def getHashesPerSecond():
    global NUMBER_OF_HASHES
    global SYSTEM_CURRENT_TIME 
    global SYSTEM_START_TIME
    SYSTEM_CURRENT_TIME = time()
    try:
        return NUMBER_OF_HASHES / (SYSTEM_CURRENT_TIME - SYSTEM_START_TIME)
    except ZeroDivisionError:
        return 0
    
def getWordlistFile():
    return open("wordlist_files/shorter_wordlist.txt", 'r')

def hashSHA256(string):
    global NUMBER_OF_HASHES
    NUMBER_OF_HASHES += 1
    return hashlib.sha256(string).hexdigest()

def isHashMatch(passwordHash, guessHash):
    if passwordHash == guessHash:
        return True
    return False
    
def generateNextOneWordRootPassword():
    wordlist = getWordlistFile()
    rootPassword = ""
    
    for first_word in wordlist:
        # [:-1] removes the trailing newline in the word
        rootPassword = first_word[:-1]
        yield rootPassword
        yield rootPassword.capitalize()
    wordlist.close()

def generateNextTwoWordRootPassword():
    rootPassword = ""
    
    first_wordlist = getWordlistFile()
    for first_word_with_newline in first_wordlist:
        first_word = first_word_with_newline[:-1]
        second_wordlist = getWordlistFile()
        for second_word_with_newline in second_wordlist:
            second_word = second_word_with_newline[:-1]
            rootPassword = first_word + second_word
            yield rootPassword
            yield rootPassword.capitalize()
        second_wordlist.close()
    first_wordlist.close()

def generateNextThreeWordRootPassword():
    rootPassword = ""

    first_wordlist = getWordlistFile()
    for first_word_with_newline in first_wordlist:
        first_word = first_word_with_newline[:-1]
        second_wordlist = getWordlistFile()
        for second_word_with_newline in second_wordlist:
            second_word = second_word_with_newline[:-1]
            third_wordlist = getWordlistFile()
            for third_word_with_newline in third_wordlist:
                third_word = third_word_with_newline[:-1]
                rootPassword = first_word + second_word + third_word
                yield rootPassword
                yield rootPassword.capitalize()
            third_wordlist.close()
        second_wordlist.close()
    first_wordlist.close()
    
def applyNumberAlterationsTo(rootPassword):   
    for appendableNumber in xrange(1, 100):
        yield rootPassword + str(appendableNumber)
    
    for appendableNumber in xrange(1, 21):
        yield rootPassword + "#" + str(appendableNumber)
    
def applySymbolAlterationsTo(rootPassword):
    # Yields all various combinations of the following substituions:
    # e -> 3
    # o -> 0
    # s -> $
    if rootPassword.count("e") is not 0:   
        yield rootPassword.replace("e", "3")
        if rootPassword.count("o") is not 0:
            yield rootPassword.replace("e", "3").replace("o", "0")
            if rootPassword.count("s") is not 0:
                yield rootPassword.replace("e", "3").replace("o", "0").replace("s", "$")
    if rootPassword.count("o") is not 0:
        yield rootPassword.replace("o", "0")
        if rootPassword.count("s") is not 0:
            yield rootPassword.replace("o", "0").replace("s", "$")
            if rootPassword.count("e") is not 0:
                yield rootPassword.replace("e", "3").replace("o", "0").replace("s", "$")
    if rootPassword.count("s") is not 0:
        yield rootPassword.replace("s", "$")
        if rootPassword.count("e") is not 0:
            yield rootPassword.replace("s", "$").replace("e", "3")
            if rootPassword.count("o") is not 0:
                yield rootPassword.replace("e", "3").replace("o", "0").replace("s", "$")
    
def crack(passwordHash, wordLength):
    global SYSTEM_START_TIME
    global NUMBER_OF_ROOTPASSWORDS_CHECKED
    
    rootPasswordGenerator = None
    
    if wordLength is 1:
        rootPasswordGenerator = generateNextOneWordRootPassword()
    elif wordLength is 2:
        rootPasswordGenerator = generateNextTwoWordRootPassword()
    elif wordLength is 3:
        rootPasswordGenerator = generateNextThreeWordRootPassword()
    else:
        return "Please enter a word length between 1 and 3, inclusively!"
    
    print "START %d WORD PASSWORDS" % wordLength
    SYSTEM_START_TIME = time()
    for rootPassword in rootPasswordGenerator:
        rootPassword
        if isHashMatch(passwordHash, hashSHA256(rootPassword)):
             return rootPassword
                      
        # Just number alterations
        for numberAlteredPassword in applyNumberAlterationsTo(rootPassword):
            if isHashMatch(passwordHash, hashSHA256(numberAlteredPassword)):
                return numberAlteredPassword
                
        # Just symbol alterations
        for symbolAlteredPassword in applySymbolAlterationsTo(rootPassword):
            if isHashMatch(passwordHash, hashSHA256(symbolAlteredPassword)):
                 return symbolAlteredPassword
        
        # Number and symbol alterations
        for numberAlteredPassword in applyNumberAlterationsTo(rootPassword):
            for numberAndSymbolAlteredPassword in applySymbolAlterationsTo(numberAlteredPassword):
                if isHashMatch(passwordHash, hashSHA256(numberAndSymbolAlteredPassword)):
                    return numberAndLetterSymbolPassword
                               
        NUMBER_OF_ROOTPASSWORDS_CHECKED += 1
        printStatistics()
    print "\nFINISHED %d WORD PASSWORDS" % wordLength
    NUMBER_OF_HASHES = 0L
    NUMBER_OF_ROOTPASSWORDS_CHECKED = 0L
    
    return None
    
def crackAgainstMostCommonPasswords(passwordHash):
    global NUMBER_OF_ROOTPASSWORDS_CHECKED
    global NUMBER_OF_HASHES
    
    commonPasswordFile = open("wordlist_files/10_million_password_list_top_100000.txt", 'r')
    
    SYSTEM_START_TIME = time()
    for password in commonPasswordFile:
        passwordWithoutNewline = password[:-1]
        if isHashMatch(passwordHash, hashSHA256(passwordWithoutNewline)):
            return passwordWithoutNewline
        NUMBER_OF_ROOTPASSWORDS_CHECKED += 1
        NUMBER_OF_HASHES += 1
        if password[0] == 'a':
            printStatistics()
    
    NUMBER_OF_ROOTPASSWORDS_CHECKED = 0
    NUMBER_OF_HASHES = 0
    return None

def getSymbolGenerator():
    symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-+={}[]|\\:;'\"<,>.?/"
    for character in symbols:
        yield character

def replace(string, replacement, index):
    return text[:index] + replacement + text[index+1:]
    
def bruteForce(passwordHash):
    global NUMBER_OF_ROOTPASSWORDS_CHECKED
    global NUMBER_OF_HASHES
    
    for passwordLength in xrange(1, 9):
        characterGenerators = []
        for character_index in xrange(0, passwordLength):
            characterGenerator = getSymbolGenerator()
            characterGenerators.append(characterGenerator)
    
        guessPassword = " " * passwordLength
        
        for character_index in xrange(0, passwordLength):
            guessPassword = replace(guessPassword, characterGenerators[character_index].next(), character_index)
            if isHashMatch(passwordHash, hashSHA256(guessPassword)):
                    return guessPassword
    return None

test_hash = hashSHA256("theofficers#13")
print test_hash
print crackAgainstMostCommonPasswords(test_hash)
rootPasswordLength = 1
print crack(test_hash, rootPasswordLength)
rootPasswordLength = 2
print crack(test_hash, rootPasswordLength)
