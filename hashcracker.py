import hashlib

def hashSHA256(string):
    return hashlib.sha256(string).hexdigest()

def isHashMatch(passwordHash, guessHash):
    if passwordHash is guessHash:
        return True
    return False

def getWordlist():

def generateNextRootPassword():
    wordlist = getWordlist()
    rootPassword = ""
    
    # One word passwords
    for first_word in wordlist:
        rootPassword = first_word
        yield rootPassword
    
    # Two word passwords
    for second_word in wordlist:
        for first_word in wordlist:
            rootPassword = first_word + second_word
            yield rootPassword
    
    # Three word passwords
    for third_word in wordlist:
        for second_word in wordlist:
            for first_word in wordlist:
                rootPassword = first_word + second_word + third_word
                yield rootPassword
    
def applyNumberAlterationsTo(rootPassword):

def applyLetterAlterationsTo(rootPassword):
    
def applySymbolAlterationsTo(rootPassword):
    
def crack(passwordHash):
    rootPasswordGenerator = generateNextRootPassword()
    for rootPassword in roodPasswordGenerator:
        guessPassword = rootPassword
        if isHashMatch(passwordHash, hashSHA256(guessPassword)):
             return guessPassword
                 
                         
        # Just number alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            if isHashMatch(passwordHash, hashSHA256(numberAlteredPassword)):
                return numberAlteredPassword
                     
        # Just letter alterations
        for letterAlteredPassword in applyLetterAlterationsTo(guessPassword):
            if isHashMatch(passwordHash, hashSHA256(letterAlteredPassword)):
                return letterAlteredPassword
             
        # Just symbol alterations
        for symbolAlteredPassword in applySymbolAlterationsTo(guessPassword):
            if isHashMatch(passwordHash, hashSHA256(symbolAlteredPassword)):
                 return symbolAlteredPassword
             
        # Number and letter alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            for numberAndLetterAlteredPassword in applyLetterAlterationsTo(numberAlteredPassword):
                 if isHashMatch(passwordHash, hashSHA256(numberAndLetterAlteredPassword)):
                     return numberAndLetterAlteredPassword
             
        # Number and symbol alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            for numberAndSymbolAlteredPassword in applySymbolAlterationsTo(numberAlteredPassword):
                if isHashMatch(passwordHash, hashSHA256(numberAndSymbolAlteredPassword)):
                    return numberAndLetterSymbolPassword
             
        # Letter and symbol alterations
        for letterAlteredPassword in applyLetterAlterationsTo(guessPassword):
            for letterAndSymbolAlteredPassword in applySymbolAlterationsTo(letterAlteredPassword):
                if isHashMatch(passwordHash, hashSHA256(letterAndSymbolAlteredPassword)):
                    return numberAndLetterAlteredPassword
             
        # Number, letter, and symbol alterations
        for numberAlteredPassword in applyNumberAlterationsTo(guessPassword):
            for numberAndLetterAlteredPassword in applyLetterAlterationsTo(numberAlteredPassword):
                for numberLetterAndSymbolAlteredPassword in applySymbolAlterationsTo(numberAndLetterAlteredPassword):
                    if isHashMatch(passwordHash, hashSHA256(numberLetterAndSymbolAlteredPassword)):
                        return numberLetterAndSymbolAlteredPassword
                         
    return guessPassword
