from PIL import Image
import colorsys

def GetLuminance(pixel):
    b, g, r = pixel
    return .3*r+.59*g+.11*b


print "Putting pixels on the palette..."
#Open up the image and get all of the pixels out of it. (Memory intensive!)
palette = Image.open("1.png")
pixels = []
pixelsL = []
width,height = palette.size
for y in range(height):
    for x in range(width):
        curpixel = palette.getpixel((x,y))
        pixelsL.append((GetLuminance(curpixel),curpixel))


#sort the pixels
pixelsL.sort()
pallen = len(pixelsL)

print "Painting new picture..."
source = Image.open("2.png")
width,height = source.size
for y in range(height):
    print str(y) + " of " + str(height)
    try:
        source.save("o.png","PNG")
    except:
        pass
    for x in range(width):
        l = GetLuminance(source.getpixel((x,y)))
        bestdist = 256*256
        best = 0
        for pos in range(pallen):
            pl,pixel = pixelsL[pos]
            dist = (l-pl)
            dist = dist*dist
            if dist<bestdist:
                    bestdist = dist
                    bestpixel = pixel
                    best = pos
                    
        source.putpixel((x,y),bestpixel)
        pixelsL = pixelsL[0:best]+pixelsL[best+1:]
        pallen = pallen-1

print "Applying fixative..."
source.save("o.png","PNG")
print "Done!"

