AZ26_CIPHER_LOWER = {
            'a' : 1,
            'b' : 2,
            'c' : 3,
            'd' : 4,
            'e' : 5,
            'f' : 6,
            'g' : 7,
            'h' : 8,
            'i' : 9,
            'j' : 10,
            'k' : 11,
            'l' : 12,
            'm' : 13,
            'n' : 14,
            'o' : 15,
            'p' : 16,
            'q' : 17,
            'r' : 18,
            's' : 19,
            't' : 20,
            'u' : 21,
            'v' : 22,
            'w' : 23,
            'x' : 24,
            'y' : 25,
            'z' : 26
            }
AZ26_CIPHER_UPPER = {
            'A' : 1,
            'B' : 2,
            'C' : 3,
            'D' : 4,
            'E' : 5,
            'F' : 6,
            'G' : 7,
            'H' : 8,
            'I' : 9,
            'J' : 10,
            'K' : 11,
            'L' : 12,
            'M' : 13,
            'N' : 14,
            'O' : 15,
            'P' : 16,
            'Q' : 17,
            'R' : 18,
            'S' : 19,
            'T' : 20,
            'U' : 21,
            'V' : 22,
            'W' : 23,
            'X' : 24,
            'Y' : 25,
            'Z' : 26
            }         

def getLetterFromValue(value, upper):
    if upper:
        for key in AZ26_CIPHER_UPPER:
            if AZ26_CIPHER_UPPER[key] == value:
                return True, key
        return False,'-'
    else:
        for key in AZ26_CIPHER_LOWER:
            if AZ26_CIPHER_LOWER[key] == value:
                return True, key
        return False,'-'

def beaufort_vin_cipher(encoded, keyword):
    return vin_cipher(keyword, encoded)

def vin_cipher(encoded, keyword):
    keyword_len = len(keyword)
    keyword_counter = 0
    decoded_word = ""
    
    for letter in encoded:
        dec = ord(letter)
        isUpperCase = letter.isupper()        
        if (dec >= 65) and (dec <= 122):
            if isUpperCase:                
                cipher_text_letter_value = AZ26_CIPHER_UPPER[letter]
                keyword_text_letter_value = AZ26_CIPHER_UPPER[keyword[keyword_counter].upper()]        
                new_value = cipher_text_letter_value - keyword_text_letter_value
            else:
                cipher_text_letter_value = AZ26_CIPHER_LOWER[letter]
                keyword_text_letter_value = AZ26_CIPHER_LOWER[keyword[keyword_counter].lower()]        
                new_value = cipher_text_letter_value - keyword_text_letter_value
            if new_value < 0:
                new_value = new_value + 26
            #print "C: %d K: %d N: %d" % (cipher_text_letter_value,keyword_text_letter_value, new_value)
            success, new_letter = getLetterFromValue(new_value+1, isUpperCase)
            if success:
                nl = new_letter
                if isUpperCase:
                    nl = nl.upper()
                else:
                    nl = nl.lower()
                decoded_word = decoded_word + new_letter
            keyword_counter += 1
            if keyword_counter >= keyword_len:
                keyword_counter = 0
        else:
            decoded_word = decoded_word + letter
    return decoded_word
    
    
print beaufort_vin_cipher("TCAMNTDRUENFRMXMOWLYBBHM".lower(),"zwzkuasljtrydmpfsnzluihd")

