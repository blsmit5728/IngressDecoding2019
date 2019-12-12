from PIL import Image

sheep = Image.open("RECURSEDSHEEP.png")

color_pixel_count = 0
grey_pixel_count = 0

prev_pixel = "None"

prev_pix_blue = 120

barcode_list = []


barcode1 = Image.new('RGB',(572,600), 'grey')
barcode2 = Image.new('RGB',(600,600), 'grey')
image_pixel_counter_x = 0
image_pixel_counter_y = 0

def check_prev_pixel(cur, prev):
    if prev != cur:
        return False
    else:
        return True


def print_barcode(color, number, bcode):
    c = (0,0,0)
    global image_pixel_counter_x
    global image_pixel_counter_y
    global barcode_list
    print "BARCODE %s : %d" % ( color, (number / 4))
    for l in range(0,number/4):
        if color is 'black':        
            barcode_list.append(1)
        else:
            barcode_list.append(0)
    for j in range(0, number):
        if color is "black":
            c = (255,255,255)
        else:
            c = (0,0,0)
        #print "%d Inserting %d pixels of %s" % (image_pixel_counter_x, j, color)
        for y in range(0,600):
            bcode.putpixel((image_pixel_counter_x,y), c)
        image_pixel_counter_x += 1
        
def bits_to_int(bit_list):
    out = ""
    for b in bit_list:
        out = out + str(b)
    print out

grey_pixel_count = 0
color_pixel_count = 0

for pixel in range(330,906):
    r,g,b = sheep.getpixel((pixel, 207))
    #print "Blue: %d" % b
    if b < 20:
        color_pixel_count += 1
        if prev_pix_blue > 20:
            # first pixel of Color after grey
            #print "Grey: %d" % grey_pixel_count
            print_barcode("black", grey_pixel_count, barcode1)
            grey_pixel_count = 0
    else:
        grey_pixel_count += 1
        if prev_pix_blue < 20:
            # first pixel of Color after yellow
            #print "Yelo: %d" % color_pixel_count
            print_barcode("white", color_pixel_count,barcode1)
            color_pixel_count = 0
    prev_pix_blue = b
            
prev_pixel_red = 0

print ""
print ""

black_pixel_count = 0
white_pixel_count = 0
image_pixel_counter_x = 0

for pixel in range(782,204,-1):
#for pixel in range(208,783):
    print "X: 330 Y: %d" % pixel
    r,g,b = sheep.getpixel((330, pixel))
    #print "Red: %d" % r
    if r < 20:
        white_pixel_count += 1
        if prev_pixel_red > 20:
            # first pixel of Color after grey
            #print "Grey: %d" % grey_pixel_count
            print_barcode("white", black_pixel_count,barcode2)
            black_pixel_count = 0
    else:
        black_pixel_count += 1
        if prev_pixel_red < 20:
            # first pixel of Color after yellow
            #print "Yelo: %d" % color_pixel_count
            print_barcode("black", white_pixel_count,barcode2)
            white_pixel_count = 0
    prev_pixel_red = r            
            

barcode1.save('Barcode1-left-to-right.png')
barcode2.save('Barcode1-bottom-to-top.png')
print len(barcode_list)
print barcode_list

print "STARTC"
bits_to_int(barcode_list[0:11]   ) # STARTC
print "69"
bits_to_int(barcode_list[11:22]  ) # 69
print "87"
bits_to_int(barcode_list[22:33]  ) # 87
print "72"
bits_to_int(barcode_list[33:44]  ) # 72
print "84"
bits_to_int(barcode_list[44:55]  ) # 84
print "72"
bits_to_int(barcode_list[55:66]  ) # 72
print "82"
bits_to_int(barcode_list[66:77]  ) # 82
print "75"
bits_to_int(barcode_list[77:88]  ) # 
print "80"
bits_to_int(barcode_list[88:99] )  # 
print "79"
bits_to_int(barcode_list[99:110])  # 
print "78"
bits_to_int(barcode_list[110:121]) # 
print "69"
bits_to_int(barcode_list[121:132]) # 
print "73"
bits_to_int(barcode_list[132:143]) # 

print "\n\n83"
bits_to_int(barcode_list[143:154]) # 
print "65"
bits_to_int(barcode_list[154:165]) # 
print "71"
bits_to_int(barcode_list[165:176]) # 
print "92"
bits_to_int(barcode_list[176:187]) # 
bits_to_int(barcode_list[187:198]) # 
bits_to_int(barcode_list[209:220]) # 
bits_to_int(barcode_list[220:231]) # 
bits_to_int(barcode_list[231:242]) # 
bits_to_int(barcode_list[242:253]) # 
bits_to_int(barcode_list[253:264]) # 
bits_to_int(barcode_list[263:274]) # 
bits_to_int(barcode_list[274:]) # 

o = ""
for j in barcode_list:   
    o = o + str(j)
    
print o



'''
if check_prev_pixel("yellow", prev_pixel) and prev_pixel is not "None":
            print "Grey Pixel Count   : %d" % color_pixel_count
            color_pixel_count = 0
        prev_pixel = "yellow"
        '''