from PIL import Image
from numpy import fft, array, mean, zeros
from numpy.linalg import norm
from numpy.ma import conjugate
import os, json, math, numpy, random

# NB! this script assumes that the path ./data contains images from the MUCT dataset
# This dataset can be downloaded from here : https://github.com/StephenMilborrow/muct

# which type of filter to build
FOCUS = "left_eye"

# cropsize
width = 32
height = 32

points = {
    "left_eye" : [43, 34],
    "mouth" : [59, 66],
    "midpoint_between_eyes" : [58, 34],
    "right_eye" : [73, 33],
    "nose" : [59, 50]
}

x = points[FOCUS][0]
y = points[FOCUS][1]
x = round(x*0.6379)
y = round(y*0.6379)

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

images = []
targetImages = []
for files in os.listdir("./data"):
    im = Image.open("./data/"+files)
    im = im.convert("L")
    im = im.resize((74,64),Image.BILINEAR)
    
    #generate random offset to target
    xof = random.randint(-5,5)
    yof = random.randint(-5,5)
    left = x-((width)/2)-xof
    top = y-((height)/2)-yof
    nux = x-left
    nuy = y-top
    
    # crop
    im = im.crop((left,top,width+left,height+top))
    images.append(numpy.asarray(im))
    
    # create target images
    targetImage = array([0.]*(width*height)).reshape((height,width))
    for xr in range(0,width):
        for yr in range(0,height):
            targetImage[yr,xr] = math.exp(-(((xr-nux)*(xr-nux))+((yr-nuy)*(yr-nuy)))/(2*2))
    targetImages.append(targetImage)

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

fi = open("filter_%s.js" % FOCUS,"w")
fi.write("var filter = ")
fi.write(json.dumps(fo))
fi.write(";\n")
fi.close()

