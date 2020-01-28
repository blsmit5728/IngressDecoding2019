import Levenshtein as lev

# x#xxxxKEYWORD##xx

LUT = ['1','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
str01 = "a"
str02 = "valued"
str03 = "walked"
str04 = "unproductive"
str05 = "productive"
str06 = "zombie"
str07 = "decentralisationist"
str08 = "abaddon"
str09 = "inexpressive"
str10 = "unexpressive"
str11 = "traditionalists"
str12 = "rationalises"
str13 = "rationalised"
str14 = "nationalism"
str15 = "nationalist"
str16 = "hypercholesterolaemia"

s1 = [str01,str02,str03,str04,str05,str06,str07,str08,str09,str10,str11,str12,str13,str14,str15]
s2 = [str02,str03,str04,str05,str06,str07,str08,str09,str10,str11,str12,str13,str14,str15,str16]

code = ""

for i in range(0,len(s1)):
    if i == 1 or i == 11 or i == 12:
        code = code + str(lev.distance(s1[i], s2[i]))
    else:
        code = code + str(LUT[lev.distance(s1[i], s2[i])])

print code
