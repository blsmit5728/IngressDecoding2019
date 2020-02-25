A = "rTLLlqZAgNgnYxlFakrMkvDxugedRGbjUAFtyEgeZywqVXtzgEnRxanrAWfJqtKHxeUcwmTgyIaeVONgeAGlHgrTtpMxtyOmoPksyfxCQgaIZFbiQwpRialUMqseQtIkpheBNsNfcTNnMFmeUcgAwsPhkgDrSNQhoGOXjEwsxOQrgMVFrLAomFLSzDnlnOchGbfijvOTcePWIerXvhBsjvGDngeZyXybzsEPyXxzMFdAepIzdlvguWuneBnrCfxrRPtLuGQTeOksaNmmFgzstgUTyiGGVrbRbuTgzrUMcniWsGgnxrLJuAfqKCu:fz"
print "Input A : " + A
B = "StmjkLSrryIIZUEJDuUfsBFBCuEeqiBGwgHNqntTGYPuuECVcpdhNzVGIeCTRTmCXfzNsKrBsnnSutMELFqIqRsczUXBsLZVcxVsAoGCeAsjEtvYdIzuSNtnLOIdsjraPtBeaacvPAgVbNGiwtUgoJBMAdcenTtvYYunbnuIXestUIbNWKrEdeYiCpdYacBuatLXeSqczAQfTPjrrUduYGWqtBaytxAsQdhralsYewqplTAApKRmPIFBRIAgrnXKqbRZRMvCTbHTssJXGWrDuPUhVQlcDEidJXxYqRSrnRwbfqRsMTbnkmKdvjt:jk"
print "Input B : " + B
C = "ptslashsofourtwominushyphenzrotwohyphenaltwoothree"
print "Catalyst: " + C

CAT = C
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

def removethecatalyst(input):
    out = ""
    removed = ""
    input = input.lower()
    count = 0
    for inChar in input:
        if (count == 0) or (count == 1):
            out = out + inChar        
        elif (count == 2) or (count == 3):
            removed = removed + inChar
        count += 1
        if count > 3:
            count = 0
    return out, removed

    
def decodePoly(input):
    res = ""
    rows, cols = (5, 5) 
    POLY_SQUARE = [['-' for i in range(cols)] for j in range(rows)] 
    POLY_SQUARE[0][0] = 'A'
    POLY_SQUARE[0][1] = 'B'
    POLY_SQUARE[0][2] = 'C'
    POLY_SQUARE[0][3] = 'D'
    POLY_SQUARE[0][4] = 'E'
    POLY_SQUARE[1][0] = 'F'
    POLY_SQUARE[1][1] = 'G'
    POLY_SQUARE[1][2] = 'H'
    POLY_SQUARE[1][3] = 'I'
    POLY_SQUARE[1][4] = 'K'
    POLY_SQUARE[2][0] = 'L'
    POLY_SQUARE[2][1] = 'M'
    POLY_SQUARE[2][2] = 'N'
    POLY_SQUARE[2][3] = 'O'
    POLY_SQUARE[2][4] = 'P'
    POLY_SQUARE[3][0] = 'Q'
    POLY_SQUARE[3][1] = 'R'
    POLY_SQUARE[3][2] = 'S'
    POLY_SQUARE[3][3] = 'T'
    POLY_SQUARE[3][4] = 'U'
    POLY_SQUARE[4][0] = 'V'
    POLY_SQUARE[4][1] = 'W'
    POLY_SQUARE[4][2] = 'X'
    POLY_SQUARE[4][3] = 'Y'
    POLY_SQUARE[4][4] = 'Z'
    for a,b in zip(input[::2], input[1::2]):
        row = int(a)
        col = int(b)
        res = res + POLY_SQUARE[row-1][col-1]
    return res

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
   
def findLetters(input):
    LETS = []
    COUNTS = {}
    for letter in input:
        letter = letter.upper()
        if letter not in LETS:
            LETS.append(letter)
            COUNTS[letter] = 1
        else:
            COUNTS[letter] = COUNTS[letter] + 1
    return LETS, COUNTS
        
   
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
#print result
C = CAT +  result[:len(C)]
result = vin_cipher(A, C)
print "Result of decoding A with C reacting constantly."
print result
result = result.replace(':','')
resultB = vin_cipher(result, B.replace(':','')) 
print "Result of decoding above with B as key"
print resultB
#print len(resultB)
resultB = resultB[:len(resultB)-2]
#print resultB

#print findLetters(resultB)
#print ""
#print ""
resultBNorm = resultB.lower()
a = resultBNorm
print "Now we use the row placment of the Elements in the above to create numbers"
b = a.replace("h", "1")
#print b
c = b.replace("li","2")
#print c
d = c.replace("na","3")
#print d
e = d.replace("k","4")
#print e
f = e.replace("rb", "5")
print f
#print len(f)
#print resultBNorm

unpoly = decodePoly(f)
print "Poly Cipher: Result is:"
print unpoly

print "Removing the Catalyst:"
print removethecatalyst(unpoly)
