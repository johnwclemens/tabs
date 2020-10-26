import sys, math
import pyglet
#import pyglet.shapes# as pygshp
#import pyglet.text  # as pygtxt
#import pyglet.window# as pygwin

def fri(f): return int(math.floor(f+0.5))

class TestGui(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nc, self.nr = 13, 8
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        super(TestGui, self).__init__(width=self.ww, height=self.wh, resizable=True, visible=False)
        pyglet.resource.path = ['res', 'res/images']
        pyglet.resource.reindex()
        self.batch = pyglet.graphics.Batch()
        self.COLORS=[(227, 147, 127, 255), (66, 60, 144, 255)]
        self.useSciSprts, self.useImgSprts, self.useOrderedGroup, self.useGridLines = True, True, True, True
        print('_init(BGN) useImgSprts={} useSciSprts={}, useOrderedGroup)={} useGridLines={}'.format(self.useImgSprts, self.useSciSprts, self.useOrderedGroup, self.useGridLines), file=DBG_FILE)
        if self.useSciSprts:  self._initSciSprts(opq=True)
        if self.useImgSprts:  self._initImgSprts(opq=True)
        if self.useGridLines: self._initGrid()
        self.set_visible(True)

    def _initGrid(self, dbg=1):
        self.MIN, self.NOM, self.MAX = 0, 1, 2
        self.MESH       = [(127, 191, 255), (255,   0,   0), (255, 255, 255)]
        mesh, color   = [1, 5, 25], self.COLORS[0]
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        c, r = self.nc, self.nr
        x, y  = 0, 0
        self.clines, self.rlines = [], []
        if c % 2 == 0:
            p = fri(c/2) % mesh[self.MAX]
            if dbg: print('addGrid() c={}=Even p={}'.format(c, p), file=DBG_FILE)
            for i in range(c+1):
                if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE, end=' ')
                if   (i-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (i-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (i-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(fri(i*w+x), fri(y), fri(i*w+x), fri(r*h+y), width=1, color=color, batch=self.batch))
        else:
            p = fri(c/2-1)
            if dbg: print('addGrid() c={}=Odd p={}'.format(c, p), file=DBG_FILE)
            for i in range(fri(c/2)):
                if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE, end=' ')
                if   (i-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (i-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (i-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(fri(i*w+x), fri(y), fri(i*w+x), fri(r*h+y), width=1, color=color, batch=self.batch))
            p = fri(c/2)
            if dbg: print('addGrid() c={}=Odd p={}'.format(c, p), file=DBG_FILE)
            for i in range(fri(c/2), c+1):
                if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE, end=' ')
                if   (i-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (i-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (i-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(fri(i*w+x), fri(y), fri(i*w+x), fri(r*h+y), width=1, color=color, batch=self.batch))
        if r % 2 == 0:
            q = fri(r / 2) % mesh[self.MAX]
            if dbg: print('addGrid() r={}=Even q={}'.format(r, q), file=DBG_FILE)
            for j in range(r+1):
                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if   (j-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (j-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (j-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(c*w+x), fri(j*h+y), width=1, color=color, batch=self.batch))
        else:
            q = fri(r/2-1)
            if dbg: print('addGrid() r={}=Odd q={}'.format(r, q), file=DBG_FILE)
            for j in range(fri(r/2)):
                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if   (j-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (j-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (j-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(c*w+x), fri(j*h+y), width=1, color=color, batch=self.batch))
            q = fri(r/2)
            if dbg: print('addGrid() r={}=odd q={}'.format(r, q), file=DBG_FILE)
            for j in range(fri(r/2), r+1):
                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if   (j-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (j-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (j-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(c*w+x), fri(j*h+y), width=1, color=color, batch=self.batch))

    def _initSciSprts(self, opq=True):
        if self.useOrderedGroup: self.sciGroup = pyglet.graphics.OrderedGroup(0)
        else:                    self.sciGroup = pyglet.graphics.Group()  #self.rootGroup)
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        _ww, _wh = self._ww, self._wh
        self.sciSprts = []
        print('_initSciSprts(BGN) _ww={} nc={} w={:6.1f} ww-w={:6.1f} ww={}  :  _wh={} nr={} h={:6.1f} wh-h={:6.1f} wh={}'.format(_ww, self.nc, w, ww-w, ww, _wh, self.nr, h, wh-h, wh), file=DBG_FILE)
        for r in range(self.nr):
            sciSprts = []
            for c in range(self.nc):
                scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                sci = scip.create_image(width=fri(w), height=fri(h))
                sci.anchor_x, sci.anchor_y = fri(sci.width/2), fri(sci.height/2)
                x, y = c*w, wh-h-r*h
#                x, y = c*w+w/2, wh-h-r*h+h/2
#                sciSprt = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.sciGroup, subpixel=False)
                sciSprt = pyglet.sprite.Sprite(img=sci, x=x+sci.anchor_x, y=y+sci.anchor_y, batch=self.batch, group=self.sciGroup, subpixel=False)
                if opq: opacity = 255
                else:   opacity = fri(255*c/(self.nc-1))
                sciSprt.opacity = opacity
                sciSprts.append(sciSprt)
                self.dumpSprite('_initSciSprts() c={:2} r={:2} c*w={:6.1f} sci.ax={} wh-h-r*h={:6.1f} sci.ay={}'.format(c, r, x, sci.anchor_x, y, sci.anchor_y), sciSprt)
#                self.dumpSprite('_initSciSprts() c={:2} r={:2} x={:6.1f}=c*w+w/2={:6.1f} y={:6.1f}=wh-h-r*h+h/2={:6.1f}'.format(c, r, x, y, c*w+w/2, wh-h-r*h+h/2), sciSprt)
            self.sciSprts.append(sciSprts)

    def _initImgSprts(self, opq=True):
        if self.useOrderedGroup: self.imgGroup = pyglet.graphics.OrderedGroup(1)
        else:                    self.imgGroup = pyglet.graphics.Group() #self.rootGroup)
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        self.imgSprts, imgs, i = [], [], 0
        s = ['apple_raw.png', 'oriel.jpg', 'pyglet.png', 'jwc.jpg', 'asteroid.png']
        self.imgSprtScales = []
        print('_initImgSprts(BGN) ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(ww, wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for i, imageFileName in enumerate(s):
            decoder = None #pyglet.image.codecs.png.PNGImageDecoder()
#            img = pyglet.image.load(imageFileName, decoder=decoder)
            img = pyglet.resource.image(imageFileName)
            imgs.append(img)
            self.imgSprtScales.append([w/img.width, h/img.height])
            img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
            print('_initImgSprts()      [{}] img.anchor_x={:4} img.anchor_y={:4} img.width={:4} img,height={:4} imgSprtScalesX={:5.3f} imgSprtScalesY={:5.3f} decoder={} f={}'.format(i, img.anchor_x, img.anchor_y, img.width, img.height, self.imgSprtScales[i][0], self.imgSprtScales[i][1], decoder, imageFileName), file=DBG_FILE)
        for r in range(self.nr):
            imgSprts = []
            if opq: opacity = 255
            else:   opacity = fri(255*r/(self.nr-1))
            for c in range(self.nc):
                img = imgs[(c+r)%(i+1)]
                img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
                x, y = c*w, self.wh-h-r*h
                imgSprt = pyglet.sprite.Sprite(img, x=x, y=y, batch=self.batch, group=self.imgGroup, subpixel=False)
                imgSprt.opacity = opacity
#                imgSprt.scale_x, imgSprt.scale_y = w/sw, h/sh
                imgSprts.append(imgSprt)
                if c == r: self.dumpSprite('_initImgSprts() {:2} {:2}'.format(r, c), imgSprt)
            self.imgSprts.append(imgSprts)

    @staticmethod
    def dumpSprite(reason, s):
        f = 'x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} m={:5.3f} mx={:5.3f} my={:5.3f} rot={:5.1f} iax={:3} iay={:3} {} {} {}'
        fs = f.format(s.x, s.y, s.width, s.height, s.scale, s.scale_x, s.scale_y, s.rotation, s.image.anchor_x, s.image.anchor_y, s.opacity, s.color, s.visible)
        print('{} : {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    def on_resize(self, width, height, dbg=1):
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        _ww, _wh = self._ww, self._wh
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        x, y, c, r = 0, 0, self.nc, self.nr
        print('on_resize(BGN) _ww={} nc={} w={:6.1f} ww-w={:6.1f} ww={}  :  _wh={} nr={} h={:6.1f} wh-h={:6.1f} wh={}'.format(_ww, self.nc, w, ww-w, ww, _wh, self.nr, h, wh-h, wh), file=DBG_FILE)
#        print('on_resize(BGN)     _ww={} _wh={} nc={} nr={} ww={} wh={} w={:5.1f} h={:5.1f}'.format(_ww, _wh, self.nc, self.nr, ww, wh, w, h), file=DBG_FILE)
        for i in range(c+1):  # len(self.clines)):
            self.clines[i].position = (fri(i*w+x), fri(y), fri(i*w+x), fri(r*h+y))
            if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE)
        if dbg: print(file=DBG_FILE)
        for j in range(r+1):  # len(self.rlines)):
            self.rlines[j].position = (fri(x), fri(j*h+y), fri(c*w+x), fri(j*h+y))
            if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE)
#        if dbg: self.printGeom('on_resize(END)', 'x={:6.2f} y={:6.2f}'.format(x, y))
        for r in range(self.nr):
            for c in range(self.nc):
                x, y = c*w+w/2, wh-h-r*h+h/2
                if self.useSciSprts:
#                    ax, ay = fri(self.sciSprts[r][c].width/2), fri(self.sciSprts[r][c].height/2)
                    self.sciSprts[r][c].update(x=x, y=y, scale_x=ww/_ww, scale_y=wh/_wh)
#                    self.sciSprts[r][c].anchor_x, self.sciSprts[r][c].anchor_y = ax, ay
                    self.sciSprts[r][c].rotation = 22.5 * c
                    self.dumpSprite('on_resize(sciSprts) c={:2} r={:2} c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(c, r, c*w, w/2, wh-h-r*h, h/2), self.sciSprts[r][c])
                if self.useImgSprts:
#                    ax, ay = fri(self.imgSprts[r][c].width/2), fri(self.imgSprts[r][c].height/2)
                    self.imgSprts[r][c].update(x=x, y=y, scale_x=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*ww/_ww, scale_y=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*wh/_wh)
#                    self.imgSprts[r][c].anchor_x, self.imgSprts[r][c].anchor_y = ax, ay
                    self.imgSprts[r][c].rotation = 22.5 * c
                    self.dumpSprite('on_resize(imgSprts) c={:2} r={:2} c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(c, r, c*w, w/2, wh-h-r*h, h/2), self.imgSprts[r][c])

    def on_resize_OLD(self, width, height):
        _ww, _wh = self._ww, self._wh
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w, self.h = self.ww/self.nc, self.wh/self.nr
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        print('on_resize(BGN)     _ww={} _wh={} nc={} nr={} ww={} wh={} w={:5.1f} h={:5.1f}'.format(_ww, _wh, self.nc, self.nr, ww, wh, w, h), file=DBG_FILE)
        for r in range(self.nr):
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                if self.useSciSprts:
                    ax, ay = fri(self.sciSprts[r][c].width/2), fri(self.sciSprts[r][c].height/2)
                    self.sciSprts[r][c].update(x=x+ax, y=y+ay, scale_x=width/_ww, scale_y=height/_wh)
                    self.sciSprts[r][c].anchor_x, self.sciSprts[r][c].anchor_y = ax, ay
#                    self.sciSprts[r][c].rotation = 90 * c
                    if c == r: self.dumpSprite('on_resize(sciSprts) {:2} {:2}'.format(r, c), self.sciSprts[r][c])
#                    print('on_resize(sciSprts) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
                if self.useImgSprts:
                    ax, ay = fri(self.imgSprts[r][c].width/2), fri(self.imgSprts[r][c].height/2)
                    self.imgSprts[r][c].update(x=x+ax, y=y+ay, scale_x=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*ww/_ww, scale_y=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*wh/_wh)
                    self.imgSprts[r][c].anchor_x, self.imgSprts[r][c].anchor_y = ax, ay
#                    self.imgSprts[r][c].rotation = 90 * c
                    sw, sh = self.imgSprts[r][c].width, self.imgSprts[r][c].height
                    p, q = self.imgSprts[r][c].scale_x, self.imgSprts[r][c].scale_y
                    if c == r: self.dumpSprite('on_resize(imgSprts) {:2} {:2}'.format(r, c), self.imgSprts[r][c])
#                    print('on_resize(imgSprts) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    test = TestGui()
    pyglet.app.run()
