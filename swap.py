from PIL import Image
import colorsys

def GetLuminance(pixel):
    b, g, r = pixel
    return .3*r+.59*g+.11*b

print "Putting pixels on the palette..."
#Open up the image and get all of the pixels out of it. (Memory intensive!)
palette = Image.open("6.png")
pixelsP = []
width,height = palette.size
for y in range(height):
    for x in range(width):
        curpixel = palette.getpixel((x,y))
        pixelsP.append((GetLuminance(curpixel),curpixel))


#sort the pixels
pixelsP.sort()

print "Getting the reference Picture"
source = Image.open("2.png")
pixelsR = []
width,height = source.size
for y in range(height):
    for x in range(width):
        curpixel = source.getpixel((x,y))
        pixelsR.append((GetLuminance(curpixel),(x,y),curpixel))

#Sort the Reference pixels
pixelsR.sort()

for p in range(len(pixelsR)):
    l,cord,dummy = pixelsR[p]
    pl,pixel = pixelsP[p]
    source.putpixel(cord,pixel)

print "Applying fixative..."
source.save("o.png","PNG")
print "Done!"

