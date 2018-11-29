### Meta Novitia
### Project 0  : Physics-based tracking of moving and growing cells in a colony
### Start Date : November 27, 2018

from imgpy import Img

# format image to take right side of gif, and simplify colors
def formatImage(gifname,fname):
    with Img(fp=gifname) as im:
        im.crop(box=(im.width / 2, 0, im.width, im.height))
        
        colors = sorted(im.frames[0].getcolors())
        for frame in im.frames:
            for x in range(im.width):
                for y in range(im.height):
                    if frame.getpixel((x,y))==colors[0][1]:
                        frame.putpixel((x,y),colors[1][1])
                    if frame.getpixel((x,y))!=colors[1][1] and frame.getpixel((x,y))!=colors[2][1]:
                        frame.putpixel((x,y),colors[-1][1])                        
        im.save(fp=fname)

# Iterate each frame and use bfs to eliminate one cell at a time.
# The number of cells will be the number of isolated shapes in the frame
# with a gray area greater than about 40
def start(fname, output):
    file = open(output,"w")
    with Img(fp=fname) as im:
        f = im.frames
        for index in range(len(f)):
            frame = f[index]
            ct = 0
            for x in range(1,frame.width-1):
                for y in range(1,frame.height-1):
                    if frame.getpixel((x,y))==2 and (frame.getpixel((x+1,y))==1 or frame.getpixel((x-1,y))==1 or frame.getpixel((x,y+1))==1 or frame.getpixel((x,y-1))==1):
                        # bfs
                        area = 1
                        queue = [(x,y)]
                        while queue!=[]:
                            a,b = queue.pop(0)
                            for i in range(-1,2):
                                for j in range(-1,2):
                                    if (i==0 or j==0) and frame.getpixel((a+i,b+j))!=0:
                                        if frame.getpixel((a+i,b+j))==2:
                                            area+=1
                                            queue.append((a+i,b+j))                                          
                                        frame.putpixel((a+i,b+j),0)
                        if area > 40:ct+=1
            file.write(str(ct)+'\n')
    file.close()


gifname = 'bacteria-animation.gif' # original gif
fname = 'crop.gif'
output = 'output.txt'

formatImage(gifname,fname)   
start(fname, output)         
