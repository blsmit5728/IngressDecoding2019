def print7segment(input):
    a = input
    for i in(0,6,3):
        print' .. '*a[i]+('\n'+' .'[a[5-i/6]]+'  '+' .'[a[1+i/6]])*(2*(i!=3))


lookup = {
    "HG" : "1",
    "SN" : "_2",
    "PB" : "__3",
    "AG" : "___4",
    "AU" : "____5",
    "CU" : "_____6",
    "FE" : "______7"
    }

lookup_char = {
    "HG" : "A",
    "SN" : "B",
    "PB" : "C",
    "AG" : "D",
    "AU" : "E",
    "CU" : "F",
    "FE" : "G"
    }

seven_segment_display = {
        "0" : "ABCDEF",
        "1" : "AB",
        "2" : "ABGED",
        "3" : "ABGCD",
        "4" : "BCFG",
        "5" : "ACDFG",
        "6" : "ACDEFG",
        "7" : "ABC",
        "8" : "ABCDEFG",
        "9" : "ABCFG"
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
chars = ["HG","AG","AU","CU","PB","AU","CU","FE","AU","FE","SN","PB","AG","CU","FE","HG","PB","AG","CU","FE","PB","AG","AU","FE","HG","SN","AU","CU","FE","PB","AG","AU","FE","HG","AG","AU","CU","FE","SN","PB","HG","SN","PB","AU","CU","FE","SN","PB","HG","SN","PB","AG","FE"]

addition = 0
intlist = []
charsstr = ""
charlist = []
begin = 0
prev = 0
print "-------------------------------"
for c in chars:
    istr = lookup[c].replace("_","")
    char = lookup_char[c]
    iint = int(istr)
    if (iint > begin) and (iint > prev):
        #print "Adding: %d" % iint
        addition += iint
        charsstr = charsstr + char
        prev = iint
    elif (iint < prev):
        intlist.append(addition)
        charlist.append(charsstr)
        addition = 0
        begin = 0
        charsstr = ""
        print "-------------------------------"
        #print "Adding: %d" % iint
        addition += iint
        charsstr = charsstr + char
        prev = iint
    print lookup[c]
intlist.append(addition)   
charlist.append(charsstr)     
print intlist
print charlist
code = "http://tiny.cc/"
for i in intlist:
    for letter in AZ26_CIPHER:
        if AZ26_CIPHER[letter] == i:
            code = code + letter
            
print code
    
for entry in charlist:
    
        
    