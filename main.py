from PIL import Image
import os
import math

# Specifications
print("Animations to SpriteSheet - 1.0v\n")
print("by Astro_815\n")

name = input("Name: ")
columns = 10

frameWidth = 0
frameHeight = 0
frameCount = 0

inputSprites = list(map(lambda s: "./input/%s" % s, os.listdir("./input")))

xmlContent = '<TextureAtlas imagePath="%s.png">\n' % name

# Calculate Total Frames

def countAllFrames():
    global frameCount, frameWidth, frameHeight
    frameCount = 0
    for sptLink in inputSprites:
        if os.path.isdir(sptLink):
            fdir = os.listdir(sptLink)
            spt = Image.open(sptLink + "/" + fdir[0])
            frameCount += len(fdir)
        else:
            spt = Image.open(sptLink)
            frameCount += spt.n_frames
        frameWidth = spt.size[0]
        frameHeight = spt.size[1]

print("Calculating Total Frames")

countAllFrames()

# Creating a frame base

print("Frame Dimensions: ", frameWidth, frameHeight)

print("Creating BASE Frame")

fb_width = frameWidth * columns
fb_height = math.ceil(frameCount / columns) * frameHeight

fb = Image.new("RGBA", (fb_width, fb_height))

frameSeek = 0

# Pasteing Frames to FrameBase - fb

for sptLink in inputSprites:
    print("Scanning sprite \"%s\"" % sptLink)
    frames = []
    szAnim = -1
    if os.path.isdir(sptLink):
        fdir = os.listdir(sptLink)
        szAnim = len(fdir)
        for frame in fdir:
            frames.append(Image.open(sptLink + "/" + frame))            
    else:
        fgif = Image.open(sptLink)
        szAnim = fgif.n_frames
        for frame in range(fgif.n_frames):
            fgif.seek(frame)
            minFrame = Image.new("RGBA", (fb_width, fb_height))
            minFrame.paste(fgif, (0,0))
            frames.append(minFrame)
    
    for frame in range(szAnim):
        spx = (frameSeek - (math.floor(frameSeek / columns) * columns)) * frameWidth
        spy = math.floor(frameSeek / columns) * frameHeight
        
        spt = frames[frame]
        fb.paste(spt, (spx, spy))

        nameFile = sptLink.split("/")[len(sptLink.split("/")) - 1]
        nameFile = nameFile.split(".")[0]

        # Name - x - y - width - height
        xmlContent += '<SubTexture name="%s %s%s" x="%s" y="%s" width="%s" height="%s"/>\n' % ( name , nameFile, str(frame).zfill(4) , spx , spy , frameWidth , frameHeight )

        frameSeek += 1

xmlContent += "</TextureAtlas>"

# Saving

print("Saving...")

xmlFile = open("./output/%s.xml" % name, "w")
xmlFile.write(xmlContent)
xmlFile.close()

fb.save("./output/%s.png" % name)

print("Saved!")