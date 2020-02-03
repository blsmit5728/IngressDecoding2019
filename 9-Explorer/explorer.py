#!/usr/bin/python

COORDS = ["zqq.vorntuvr,oso.npvwuvup" ,
     "rv.vwvwwrts,p.qqqrvruv"    ,
     "pt.otrrnqus,zvn.outrnovw"  ,
     "sq.spsqoruw,zp.pounnpvs"   ,
     "qu.swvoopun,opt.wpwwnwuw"  ,
     "rp.wvsttuvp,zvv.nvrnnnvr"  ,
     "sp.srqtsovp,oq.qrtqusvw"   ,
     "sq.ownrwnuq,s.wqnpvsuv"    ,
     "sq.swqrrwuo,w.wvnrqtvr"    ,
     "qr.ouqsvsup,zoou.vvrrvtuq" ,
     "ro.swnoopvq,zwq.tpuoppvn"  ,
     "so.rowrrqvs,zn.ovsrntwn"   ,
     "zqv.nurtrnwn,orp.pwvuouut" ,
     "ss.tvrtwutw,op.sotousqq"    ]
     
LUT = {
        'n' : 0, 
        'o' : 1,
        'p' : 2,
        'q' : 3,
        'r' : 4,
        's' : 5,
        't' : 6, 
        'u' : 7,
        'v' : 8,
        'w' : 9
    }

AZ26_CIPHER = {
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
    
for c in COORDS:
    str = ""
    for letter in c:
        if letter == '.' or letter == ',':
            str = str + letter
        elif letter == 'z':
            str = str + '-'
        else:
            str = "%s%d" % (str, LUT[letter])
    print str
    
encoded = "glyiuajjpbnjjcviwydarpbeilrygstmfmednfrhtu"

def getLetterFromValue(value):
    for key in AZ26_CIPHER:
        if AZ26_CIPHER[key] == value:
            return True, key
    return False,'-'

def vin_cipher(encoded, keyword):
    keyword = keyword.lower()
    keyword_len = len(keyword)
    keyword_counter = 0
    decoded_word = ""
    for letter in encoded:
        cipher_text_letter_value = AZ26_CIPHER[letter]
        keyword_text_letter_value = AZ26_CIPHER[keyword[keyword_counter]]        
        new_value = cipher_text_letter_value - keyword_text_letter_value
        if new_value < 0:
            new_value = new_value + 26
        #print "C: %d K: %d N: %d" % (cipher_text_letter_value,keyword_text_letter_value, new_value)
        success, new_letter = getLetterFromValue(new_value+1)
        if success:
            #print "Found: %s" % new_letter
            decoded_word = decoded_word + new_letter
        keyword_counter += 1
        if keyword_counter >= keyword_len:
            keyword_counter = 0
    return decoded_word
        
print "Encoded Word: %s " % encoded
print "Decoded Word: %s " % (vin_cipher(encoded, "ISHUMINANTATHU"))
