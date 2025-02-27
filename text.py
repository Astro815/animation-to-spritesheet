from PIL import Image
import os
import math

# Especifications

print("Animations SpriteSheet - 1.3v\n")
print("by Astro_815\n")

name = input("Name: ")
columns = 10

sizeFrame = 0
sizeFrame_height = 0
totalFrame = 0

inputSprites = list(map(lambda s: "./input/%s" % s, os.listdir("./input")))

xmlContent = '<TextureAtlas imagePath="%s.png">\n' % name

# Calculador de Total de Frames

def countAllFrames():
    global totalFrame, sizeFrame, sizeFrame_height
    totalFrame = 0
    for sptLink in inputSprites:
        if os.path.isdir(sptLink):
            fdir = os.listdir(sptLink)
            spt = Image.open(sptLink + "/" + fdir[0])
            totalFrame += len(fdir)
        else:
            spt = Image.open(sptLink)
            totalFrame += spt.n_frames
        sizeFrame = spt.size[0]
        sizeFrame_height = spt.size[1]

print("Calculando o Total de Frames")

countAllFrames()

# Creating a frame base

print(sizeFrame, sizeFrame_height)

print("Criando Frame BASE")

fb_width = sizeFrame * columns
fb_height = math.ceil(totalFrame / columns) * sizeFrame_height

fb = Image.new("RGBA", (fb_width, fb_height))

frameSeek = 0

# Pasteing Frames to FrameBase - fb

for sptLink in inputSprites:
    print("Escaneando o sprite \"%s\"" % sptLink)
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
        spx = (frameSeek - (math.floor(frameSeek / columns) * columns)) * sizeFrame
        spy = math.floor(frameSeek / columns) * sizeFrame_height
        
        spt = frames[frame]

        fb.paste(spt, (spx, spy))

        nameFile = sptLink.split("/")[len(sptLink.split("/")) - 1]
        nameFile = nameFile.split(".")[0]

        # Name - x - y - width - height
        xmlContent += '<SubTexture name="%s %s%s" x="%s" y="%s" width="%s" height="%s"/>\n' % ( name , nameFile, str(frame).zfill(4) , spx , spy , sizeFrame , sizeFrame_height )

        frameSeek += 1

xmlContent += "</TextureAtlas>"

# Saving

print("Salvando")

xmlFile = open("./output/%s.xml" % name, "w")
xmlFile.write(xmlContent)
xmlFile.close()

fb.save("./output/%s.png" % name)