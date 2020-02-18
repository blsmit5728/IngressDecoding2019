from PIL import Image

encoded = Image.open("mistyhannah_50dcb5e8-2e94-533b-8dd5-936ddba8392d.png")

width, height = encoded.size

decoded = Image.new('RGB',(width,height),'white')

width_range = range(0,width)
height_range = range(0,height)

for w_pixel in width_range:
    for h_pixel in height_range:
        r,g,b = encoded.getpixel((w_pixel, h_pixel))
        #print "R: %d G: %d B: %d" %(r,g,b)
        new_r = (r-g)
        new_g = (g-b)
        new_b = (b-r)
        if new_r > 0 or new_g > 0 or new_b > 0:
            if r < g:
                new_r = 125
                new_g = 125
                new_b = 125
            else:
                new_r = 255
                new_g = 255
                new_b = 255
            c = (new_r,new_g,new_b)
            print c
        else:
            c = (new_r,new_g,new_b)
        
        decoded.putpixel((w_pixel,h_pixel), c)
        
decoded.save('decoded.png', 'PNG')
