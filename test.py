def applySymbolAlterationsTo(rootPassword):
    guessPassword = ""
    for character_index in xrange(0, len(rootPassword)):
       if character_index is len(rootPassword) - 1:
           guessPassword += rootPassword[character_index]
           break
       guessPassword += rootPassword[character_index] + "_"
    return guessPassword
    
print applySymbolAlterationsTo("thisisapassword")
