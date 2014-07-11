from PIL import Image
import os
import sys

# ***********************
# This code segment abducted from image_rarranger.py. I've also mangled it to take the mappings from an external source.
# Algorithim abducted from Calvin's Hobbies (http://codegolf.stackexchange.com/users/26997/calvins-hobbies)
# I've mangled it a TON to make it show the real rearrangement of the pixels and to speak in the same fluff
# as the rest of my prompts.

def check(palette, copy):
    palette = sorted(palette.getdata())
    copy = sorted(copy.getdata())
    print "Master says it's good!" if copy == palette else "The master disapproves."

def getCanvasDims(src, dst, inPlace):
	w = max(src.size[0], dst.size[0])
	h = max(src.size[1], dst.size[1])
	offset = lambda dim, canvasDim: int(0.5 * (canvasDim - dim))
	srcPos = offset(src.size[0], w), offset(src.size[1], h)
	dstPos = offset(dst.size[0], w), offset(dst.size[1], h)
	if not inPlace:
		dstPos = dstPos[0] + w, dstPos[1]
		w *= 2
	return (w, h), srcPos, dstPos

def makeLinearMapper(steps):
	def linearMapper(startLoc, stopLoc, step):
		m = lambda start, stop: (stop - start) * step / steps + start
		return (m(startLoc[0], stopLoc[0]), m(startLoc[1], stopLoc[1]))
	return linearMapper

#src is the filename of the palette image that will be rearranged
#dst if the filename of the final rearranged palette
#steps is the number of increments between src and dst, steps + 1 images are generated in total
#folder is the location all intermediate images will save to
#bg is the background of the intermediate images
#when cycle is true a duplicate set of images will be made with higher numbers in reverse order, useful for making continuous looking gifs
#when inPlace is true the transforming images are drawn on top of one another
#when drawSrc is true the src image is drawn below the moving pixels
#when drawDst is true the dst image is drawn below the moving pixels
def go(src, dst, steps, inputmappings, folder='output', bg='black', cycle=False, inPlace=True, drawSrc=False, drawDst=False):
	print 'STARTING'

	def saveImg(img, number):
		img.save('%s/img_%04d.png' % (folder, number))

	if not os.path.exists(folder):
		os.makedirs(folder)

	canvasDims = getCanvasDims(src, dst, inPlace)
        # Apply the offsets to the mappings
	mappings= []
	for mapping in inputmappings:
	    mappings.append(((mapping[0][0] + canvasDims[1][0],mapping[0][1] + canvasDims[1][1]),(mapping[1][0] + canvasDims[2][0],mapping[1][1] + canvasDims[2][1]),mapping[2]))

	mapper = makeLinearMapper(steps)

	for step in range(steps + 1):
		print 'Generating image %d of %d' % (step + 1, steps + 1)

		img = Image.new('RGB', canvasDims[0], bg)
		if drawSrc:
			img.paste(src, canvasDims[1])
		if drawDst:
			img.paste(dst, canvasDims[2])
		data = img.load()
		for startLoc, stopLoc, color in mappings:
			x, y = mapper(startLoc, stopLoc, step)
			data[x, y] = color
		saveImg(img, step)

		if cycle and step != 0 and step != steps:
			saveImg(img, 2 * steps - step)

	print 'DONE'

# End abduction
# ***********************

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
        pixelsP.append((GetLuminance(curpixel),curpixel,(x,y))) # and add a (luminance, color) tuple to the array.


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
mappings = []
for p in range(len(pixelsP)): # For each pixel in the palette
    pl,pixel,coordp = pixelsP[p] # Grab the pixel from the palette
    l,coord = pixelsR[p] # Grab the location from the reference
    source.putpixel(coord,pixel) # and assign the pallet pixel to the refrence pixels place
    mappings.append((coordp,coord,pixel))

print "Handing it to the master to see if he approves..."
check(palette, source)

print "Applying fixative..."
# save out the result.
source.save("o.png","PNG")

print "Showing our work..."
go(palette, source, 19,mappings)

print "Done!"


