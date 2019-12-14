from PIL import Image
import sys

sheep = Image.open(sys.argv[1])
print sheep.size
color_pixel_count = 0
grey_pixel_count = 0

prev_pixel = "None"

prev_pix_blue = 120

barcode_list = []


barcode = Image.new('RGB',(1200,600), 'grey')
image_pixel_counter_x = 0
image_pixel_counter_y = 0

def check_prev_pixel(cur, prev):
    if prev != cur:
        return False
    else:
        return True


def print_barcode(color, number):
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
            barcode.putpixel((image_pixel_counter_x,y), c)
        image_pixel_counter_x += 1

def bits_to_int(bit_list):
    out = ""
    for b in bit_list:
        out = out + str(b)
    print out

grey_pixel_count = 0
color_pixel_count = 0

for pixel in range(0,572):
    #print sheep.getpixel((pixel, 0))
    r,g,b = sheep.getpixel((pixel, 0))
    #print "R: %d G: %d B: %d" % (r,g,b)    
    if b == 0:
        color_pixel_count += 1
        if (prev_pix_blue == 255) and (pixel != 0):
            print_barcode("white", grey_pixel_count)
            grey_pixel_count = 0
    elif b == 255:
        grey_pixel_count += 1
        if (prev_pix_blue == 0) and (pixel != 0):
            # first pixel of Color after yellow
            print_barcode("black", color_pixel_count)
            color_pixel_count = 0
    prev_pix_blue = b        

print barcode_list