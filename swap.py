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
        pixels.append(curpixel)
        pixelsL.append(GetLuminance(curpixel))

print "Painting new picture..."
source = Image.open("2.png")
width,height = source.size
for y in range(height):
    print str(y) + " of " + str(height)
    source.save("o.png","PNG")
    for x in range(width):
        l = GetLuminance(source.getpixel((x,y)))
        bestdist = 256*256
        for p in range(len(pixelsL)):
            dist = (pixelsL[p]-l)
            dist = dist*dist
            if dist<bestdist:
                bestdist = dist
                best = p
                    
        source.putpixel((x,y),pixels[best])
        pixels = pixels[0:best]+pixels[best+1:]
        pixelsL = pixelsL[0:best]+pixelsL[best+1:]

print "Applying fixative..."
source.save("o.png","PNG")
print "Done!"

