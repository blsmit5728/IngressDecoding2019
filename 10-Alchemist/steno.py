from PIL import Image
import sys

steno = Image.open(sys.argv[1])
decoded_w, decoded_l = steno.size
decodedImg = Image.new('RGB',(decoded_w,decoded_l), 'grey')

for pixel_x in range(0, decoded_w):
    for pixel_y in range(0, decoded_l):
        r,g,b, n = steno.getpixel((pixel_x, pixel_y))
        #print steno.getpixel((pixel_x, pixel_y))
        if (r % 2):
            # odd
            decodedImg.putpixel((pixel_x,pixel_y), (255,255,255))
        else:
            decodedImg.putpixel((pixel_x,pixel_y), (0,0,0))
        
decodedImg.save('decoded.png')      