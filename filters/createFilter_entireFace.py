from PIL import Image
from numpy import fft, array, mean, zeros
from numpy.linalg import norm
from numpy.ma import conjugate
import os, json, math, numpy, random

# cropsize
width = 32
height = 32

# midpoint between eyes
#x = 58
#y = 34

# left eye
#x = 43
#y = 34

# right eye
#x = 73
#y = 33

x_i = 27+32
y_i = 15+32

def cosine_window(ar):
    halfWidth = (width)/2.
    halfHeight = (height)/2.
    newArray = zeros(ar.shape)
    for i in range(0, width):
        for j in range(0, height):
            x = i-halfWidth
            y = j-halfHeight
            cww = math.sin((math.pi*i)/(width-1))
            cwh = math.sin((math.pi*j)/(height-1))
            min(cww,cwh)
            newArray[j,i] = min(cww,cwh)*ar[j,i]
    return newArray

# we assume faces are scaled

# load images and coordinate of point
#images = {}
#fi = open("./data/coordinates.csv")
#for lines in fi:
#    li = lines.split(";")
#    coord = li[1].split(",")
#    images[li[0]] = [int(coord[0]), int(coord[1])]
#fi.close()

#imagedata = []
#targetdata = []

# for each image
#for k,v in images.iterval():
images = []
targetImages = []
for files in os.listdir("./data"):
    im = Image.open("./data/"+files)
    im = im.convert("L")
    
    #generate random offset to target
    xof = random.randint(-5,5)
    yof = random.randint(-5,5)
    left = x_i-(64/2)-(xof*2)
    top = y_i-(64/2)-(yof*2)
    #top = 23
    nux = 16+xof
    nuy = 16+yof
    
    # crop
    im = im.crop((left,top,64+left,64+top))
    im = im.resize((width,height),Image.BILINEAR)
    #Image.fromarray(numpy.asarray(im).astype('int')).convert("L").save("test.bmp")
    images.append(numpy.asarray(im))
    
    # create target images
    targetImage = array([0.]*(width*height)).reshape((height,width))
    for xr in range(0,width):
        for yr in range(0,height):
            targetImage[yr,xr] = math.exp(-(((xr-nux)*(xr-nux))+((yr-nuy)*(yr-nuy)))/(2*2))
    #Image.fromarray((targetImage*255).astype('int')).convert("L").save("test_target.bmp")
    targetImages.append(targetImage)
    #import pdb;pdb.set_trace()

print "preprocessing"
# preprocess all images (not targets)
images = [numpy.log(im+1) for im in images]

# normalize
images = [im-mean(im) for im in images]
images = [im/norm(im) for im in images]
# cosine window
images = [cosine_window(im) for im in images]

# fft of images
images = [fft.fft2(im) for im in images]
targetImages = [fft.fft2(ti) for ti in targetImages]

print "calculating filter"
# calculate filter
top = numpy.zeros((height, width))
top = top.astype('complex')
bottom = numpy.zeros((height, width))
bottom = bottom.astype('complex')
for r in range(len(images)):
    top += targetImages[r]*conjugate(images[r])
    bottom += images[r]*conjugate(images[r])
    
filter = top/bottom

filres = fft.ifft2(filter)
fil = filres.real
minf = numpy.min(fil)
fil -= minf
maxf = numpy.max(fil)
fil *= (255/maxf)
fil = numpy.floor(fil)
Image.fromarray(fil.astype('int')).convert("L").save("example.bmp")

# write out to javascript file
fo = {}
fo['width'] = width
fo['height'] = height
fo['real'] = []
fo['imag'] = []
fo['top'] = {'real':[],'imag':[]}
fo['bottom'] = {'real':[],'imag':[]}
for f in filter.flatten():
    fo['real'].append(f.real)
    fo['imag'].append(f.imag)
for f in top.flatten():
    fo['top']['real'].append(f.real)
    fo['top']['imag'].append(f.imag)
for f in bottom.flatten():
    fo['bottom']['real'].append(f.real)
    fo['bottom']['imag'].append(f.imag)

fi = open("face_filter.js","w")
fi.write("var face_filter = ")
fi.write(json.dumps(fo))
fi.write(";\n")
fi.close()

