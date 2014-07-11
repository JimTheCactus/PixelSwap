from PIL import Image

def GetLuminance(pixel):
    # Extract the pixel channel data
    b, g, r = pixel
    # and used the standard luminance curve to get luminance.
    return .3*r+.59*g+.11*b

print "Putting pixels on the palette..."
# Open up the image and get all of the pixels out of it. (Memory intensive!)
palette = Image.open("3.png").convert(mode="RGB")

pixelsP = [] # Allocate the array
width,height = palette.size # Unpack the image size
for y in range(height): # Scan the lines
    for x in range(width): # within the line, scan the pixels
        curpixel = palette.getpixel((x,y)) # get the pixel
        pixelsP.append((GetLuminance(curpixel),curpixel)) # and add a (luminance, color) tuple to the array.


# sort the pixels by the calculated luminescence
pixelsP.sort()

print "Getting the reference picture..."
# Open up the image and get all of the pixels out of it. (Memory intensive!)
source = Image.open("2.png").convert(mode="RGB")
pixelsR = [] # Allocate the array
width,height = source.size # Unpack the image size
for y in range(height): # Scan the lines
    for x in range(width): # within the line, scan the pixels
        curpixel = source.getpixel((x,y)) # get the pixel
        pixelsR.append((GetLuminance(curpixel),(x,y))) # and add a (luminance, position) tuple

# Sort the Reference pixels by luminance too
pixelsR.sort()

# Now for the neat observation. Luminance matters more to humans than chromanance,
# given this then we want to match luminance as well as we can. However, we have
# a finite luminance distribution to work with. Since we can't change that, it's best
# just to line the two images up, sorted by luminance, and just simply assign the
# luminance directly. The chrominance will be all kinds of whack, but fixing that
# by way of loose sorting possible chrominance errors takes this algorithm from O(n)
# to O(n^2), which just takes forever (trust me, I've tried it.)

print "Painting reference with palette..."
for p in range(len(pixelsP)): # For each pixel in the palette
    pl,pixel = pixelsP[p] # Grab the pixel from the palette
    l,cord = pixelsR[p] # Grab the location from the reference
    source.putpixel(cord,pixel) # and assign the pallet pixel to the refrence pixels place

print "Applying fixative..."
# save out the result.
source.save("o.png","PNG")
print "Done!"

