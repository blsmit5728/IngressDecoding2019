from PIL import Image
import sys

def makeImageStenoReady(filename, saveFilename):
    steno = Image.open(filename)
    decoded_w, decoded_l = steno.size
    decodedImg = Image.new('RGB',(decoded_w,decoded_l), 'grey')
    for pixel_x in range(0, decoded_w):
        for pixel_y in range(0, decoded_l):
            r,g,b = steno.getpixel((pixel_x, pixel_y))
            #print steno.getpixel((pixel_x, pixel_y))
            if (r % 2):
            # odd
            # make it even.
                decodedImg.putpixel((pixel_x,pixel_y), (r-1,g-1,b-1))
            else:
                decodedImg.putpixel((pixel_x,pixel_y), (r,g,b))    
    decodedImg.save(saveFilename)      


def encodeImageIntoBWPic(imageFN, encodeFN, outputFN):
    regularImage = Image.open(imageFN)
    encodeImage = Image.open(encodeFN)
    width, length = regularImage.size
    outputImage =  Image.new('RGB',(width, length), 'grey')

    for pixel_x in range(0, width):
        for pixel_y in range(0, length):
            enr, eng, enb, s = encodeImage.getpixel((pixel_x, pixel_y))
            #print("EEE: %d,%d,%d,%d" %( enr, eng, enb,s))
            r,g,b = regularImage.getpixel((pixel_x,pixel_y))
            if (enr == 0) and (eng == 0) and (enb == 0):
                #print("[%d,%d](%d,%d,%d)" % (pixel_x,pixel_y,r,g,b))
                r+=1
                g+=1
                b+=1
                #print("[%d,%d](%d,%d,%d)" % (pixel_x,pixel_y,r,g,b))
            outputImage.putpixel((pixel_x,pixel_y),(r,g,b)) 
    outputImage.save(outputFN)

def decodeImage(inputFN, outputFN):
    inputImage = Image.open(inputFN)
    width, length = inputImage.size
    outputImage =  Image.new('RGB',(width, length), 'grey')
    for pixel_x in range(0, width):
        for pixel_y in range(0, length):
            r,g,b = inputImage.getpixel((pixel_x,pixel_y))
            color = (-1,-1,-1)
            if (r % 2):
                # ODD
                color = (0,0,0)
            else:
                color = (255,255,255)
            outputImage.putpixel((pixel_x,pixel_y),color)
    outputImage.save(outputFN)

print("Taking Input Image: %s and making it all Even" % sys.argv[1])
makeImageStenoReady(sys.argv[1], sys.argv[2])
print("Now taking the output of that and encoding my message into it...")
encodeImageIntoBWPic(sys.argv[2],sys.argv[3],sys.argv[4])
print("Testing that the decoding works as expected...")
decodeImage(sys.argv[4], "TEST.png")
print("Done!")
