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
    print (b'\x08').decode()*5*len(statistics),

def getRootPasswordChecksPerSecond():
    global NUMBER_OF_ROOTPASSWORDS_CHECKED
    global SYSTEM_CURRENT_TIME 
    global SYSTEM_START_TIME
    SYSTEM_CURRENT_TIME = time()
    return NUMBER_OF_ROOTPASSWORDS_CHECKED / (SYSTEM_CURRENT_TIME - SYSTEM_START_TIME)
    
def getHashesPerSecond():
    global NUMBER_OF_HASHES
    global SYSTEM_CURRENT_TIME 
    global SYSTEM_START_TIME
    SYSTEM_CURRENT_TIME = time()
    return NUMBER_OF_HASHES / (SYSTEM_CURRENT_TIME - SYSTEM_START_TIME)

def getWordlistFile():
    return open("shorter_wordlist.txt", 'r')

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
    wordlist = getWordlistFile()
    rootPassword = ""
    
    for second_word in wordlist:
        for first_word in wordlist:
            # [:-1] removes the trailing newline in the word
            rootPassword = first_word[:-1] + second_word[:-1]
            yield rootPassword
            # [:-1] removes the trailing newline in the word
            rootPassword = first_word[:-1].capitalize() + second_word[:-1].capitalize()
            yield rootPassword
            # [:-1] removes the trailing newline in the word
            rootPassword = first_word[:-1] + "_" + second_word[:-1]
            yield rootPassword
    wordlist.close()

def generateNextThreeWordRootPassword():
    wordlist = getWordlistFile()
    rootPassword = ""

    for third_word in wordlist:
        for second_word in wordlist:
            for first_word in wordlist:
                # [:-1] removes the trailing newline in the word
                rootPassword = first_word[:-1] + second_word[:-1] + third_word[:-1]
                yield rootPassword
                # [:-1] removes the trailing newline in the word
                rootPassword = first_word[:-1].capitalize() + second_word[:-1].capitalize() + third_word[:-1].capitalize()
                yield rootPassword
                # [:-1] removes the trailing newline in the word
                rootPassword = first_word[:-1] + "_" + second_word[:-1] + "_" + third_word[:-1]
                yield rootPassword
    wordlist.close()
    
def applyNumberAlterationsTo(rootPassword):   
    for appendableNumber in xrange(1, 100):
        yield rootPassword + str(appendableNumber)
    
    for appendableNumber in xrange(1, 21):
        yield rootPassword + "#" + str(appendableNumber)
    
    for appendableYear in xrange(1900, 2018):
        yield rootPassword + str(appendableYear)
    
def applySymbolAlterationsTo(rootPassword):
    # Yields all various combinations of:
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
        guessPassword = rootPassword
        NUMBER_OF_ROOTPASSWORDS_CHECKED += 1
        if isHashMatch(passwordHash, hashSHA256(guessPassword)):
             return guessPassword
                      
        # Just number alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            if isHashMatch(passwordHash, hashSHA256(numberAlteredPassword)):
                return numberAlteredPassword
                
        # Just symbol alterations
        for symbolAlteredPassword in applySymbolAlterationsTo(guessPassword):
            if isHashMatch(passwordHash, hashSHA256(symbolAlteredPassword)):
                 return symbolAlteredPassword
        
        # Number and symbol alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            for numberAndSymbolAlteredPassword in applySymbolAlterationsTo(numberAlteredPassword):
                if isHashMatch(passwordHash, hashSHA256(numberAndSymbolAlteredPassword)):
                    return numberAndLetterSymbolPassword
                    
        NUMBER_OF_ROOTPASSWORDS_CHECKED += 1
        printStatistics()
    print "\nFINISHED %d WORD PASSWORDS" % wordLength
    
    return None
    
    
test_hash = hashSHA256("aardvarkabandon11")
print test_hash
rootPasswordLength = 1
print crack(test_hash, rootPasswordLength)
rootPasswordLength = 2
print crack(test_hash, rootPasswordLength)
