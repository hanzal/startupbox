#Compare two images

import matplotlib.pyplot as plt
import cv2
import sys
import os
import shutil
import requests


url1, url2 = sys.argv[1:]

print "Downloading image 1"
response = requests.get(url1, stream=True)
with open('img1', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)
del response

print "Downloading image 2"
response = requests.get(url2, stream=True)
with open('img2', 'wb') as out_file:
   shutil.copyfileobj(response.raw, out_file)
del response

#load the images
image1 = cv2.imread('img1')
image2 = cv2.imread('img2')


mimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
mimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

#compute color histogram and normalise
hist1 = cv2.calcHist([mimage1], [0, 1, 2], None, [8, 8, 8],
	[0, 256, 0, 256, 0, 256])
hist1 = cv2.normalize(hist1).flatten()
hist2 = cv2.calcHist([mimage2], [0, 1, 2], None, [8, 8, 8],
	[0, 256, 0, 256, 0, 256])
hist2 = cv2.normalize(hist2).flatten()

# compute the distance between the two histograms
# using the correlation method 
d = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)

#printing similarity in percentage
if d < 0:
	d = 0
print "Similarity  = %.2f%%" %(d*100)

#show the query images
fig = plt.figure("Image1")
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mimage1)
plt.axis("off")
fig = plt.figure("Image2")
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mimage2)
plt.axis("off")


plt.show()


os.remove('img1')
os.remove('img2')
