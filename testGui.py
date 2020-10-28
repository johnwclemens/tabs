import sys, math
import pyglet

def fri(f): return int(math.floor(f+0.5))

class TestGui(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nc, self.nr = 13, 9
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        super(TestGui, self).__init__(width=self.ww, height=self.wh, resizable=True, visible=False)
        pyglet.resource.path = ['res', 'res/images']
        pyglet.resource.reindex()
        self.batch = pyglet.graphics.Batch()
        self.COLORS=[(227, 147, 127, 255), (66, 60, 144, 255)]
        self.useSciSprts, self.useImgSprts, self.useOrderedGroup, self.useGridLines = True, True, True, True
        print('_init(BGN) useImgSprts={} useSciSprts={}, useOrderedGroup={} useGridLines={}'.format(self.useImgSprts, self.useSciSprts, self.useOrderedGroup, self.useGridLines), file=DBG_FILE)
        if self.useSciSprts:  self._initSciSprts(opq=True)
        if self.useImgSprts:  self._initImgSprts(opq=True)
        if self.useGridLines: self._initGrid()
        self.set_visible(True)

    def dumpGeom(self, reason):
        print('{:32} _ww={} nc={} w={:6.1f} ww-w={:6.1f} ww={}  :  _wh={} nr={} h={:6.1f} wh-h={:6.1f} wh={}'
              .format(reason, self._ww, self.nc, self.w, self.ww-self.w, self.ww, self._wh, self.nr, self.h, self.wh-self.h, self.wh), file=DBG_FILE)

    def getGeom(self):
        return self._ww, self._wh, self.ww, self.wh, self.w, self.h, self.nc, self.nr

    def _initGrid(self, dbg=1):
        if self.useOrderedGroup: self.lineGroup = pyglet.graphics.OrderedGroup(2)
        else:                    self.lineGroup = pyglet.graphics.Group()
        self.MIN, self.NOM, self.MAX = 0, 1, 2
        self.MESH       = [(255, 0, 0), (0, 255, 0), (255, 255, 255)]
        mesh, color   = [1, 5, 10], self.COLORS[0]
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
#        x, y  = 0, 0
        self.dumpGeom('_initGrid(BGN)')
        self.clines, self.rlines = [], []
        if nc % 2 == 0:
            p = fri(nc/2) % mesh[self.MAX]
            if dbg: print('_initGrid() nc={}=Even p={}'.format(nc, p), file=DBG_FILE)
            for c in range(nc+1):
                x1, y1 = c*w, 0
                x2, y2 = c*w, nr*h
                if   (c-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (c-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (c-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.clines.append(pyglet.shapes.Line(i*w+x, y, i*w+x, nr*h+y, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('i={:3} w={:6.2f} x={:6.2f} i*w={:6.2f} i*w+x={:6.2f}'.format(i, w, x, i*w, i*w+x), file=DBG_FILE)
                if dbg: print('c=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        else:
            p = fri(nc/2-1)
            if dbg: print('_initGrid() nc={}=Odd p={}'.format(nc, p), file=DBG_FILE)
            for c in range(fri(nc/2)):
                x1, y1 = c*w, 0
                x2, y2 = c*w, nr*h
                if   (c-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (c-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (c-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.clines.append(pyglet.shapes.Line(fri(i*w+x), fri(y), fri(i*w+x), fri(nr*h+y), width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE, end=' ')
                if dbg: print('c=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
            p = fri(nc/2)
            if dbg: print('_initGrid() nc={}=Odd p={}'.format(nc, p), file=DBG_FILE)
            for c in range(fri(nc/2), nc+1):
                x1, y1 = c*w, 0
                x2, y2 = c*w, nr*h
                if   (c-p) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(i-p)%{}={}'.format(mesh[self.MAX], (i-p) % mesh[self.MAX]), file=DBG_FILE)
                elif (c-p) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(i-p)%{}={}'.format(mesh[self.NOM], (i-p) % mesh[self.NOM]), file=DBG_FILE)
                elif (c-p) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(i-p)%{}={}'.format(mesh[self.MIN], (i-p) % mesh[self.MIN]), file=DBG_FILE)
                self.clines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.clines.append(pyglet.shapes.Line(fri(i*w+x), fri(y), fri(i*w+x), fri(nr*h+y), width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('i={:4} w={:6.2f} x={:6.2f} i*w={:7.2f} {:4} i*w+x={:7.2f} {:4}'.format(i, w, x, i*w, fri(i*w), i*w+x, fri(i*w+x)), file=DBG_FILE, end=' ')
                if dbg: print('c=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        if nr % 2 == 0:
            q = fri(nr/2) % mesh[self.MAX]
            if dbg: print('_initGrid() nr={}=Even q={}'.format(nr, q), file=DBG_FILE)
            for r in range(nr+1):
                x1, y1 = 0,    r*h
                x2, y2 = nc*w, r*h
                if   (r-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (r-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (r-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(nc*w+x), fri(j*h+y), width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
        else:
            q = fri(nr/2-1)
            if dbg: print('_initGrid() nr={}=Odd q={}'.format(nr, q), file=DBG_FILE)
            for r in range(fri(nr/2)):
                x1, y1 = 0,    r*h
                x2, y2 = nc*w, r*h
                if   (r-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (r-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (r-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(nc*w+x), fri(j*h+y), width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
            q = fri(nr/2)
            if dbg: print('_initGrid() nr={}=odd q={}'.format(nr, q), file=DBG_FILE)
            for r in range(fri(nr/2), nr+1):
                x1, y1 = 0,    r*h
                x2, y2 = nc*w, r*h
                if   (r-q) % mesh[self.MAX] == 0: color = self.MESH[self.MAX]; #print('(j-q)%{}={}'.format(mesh[self.MAX], (j-q) % mesh[self.MAX]), file=DBG_FILE)
                elif (r-q) % mesh[self.NOM] == 0: color = self.MESH[self.NOM]; #print('(j-q)%{}={}'.format(mesh[self.NOM], (j-q) % mesh[self.NOM]), file=DBG_FILE)
                elif (r-q) % mesh[self.MIN] == 0: color = self.MESH[self.MIN]; #print('(j-q)%{}={}'.format(mesh[self.MIN], (j-q) % mesh[self.MIN]), file=DBG_FILE)
                self.rlines.append(pyglet.shapes.Line(x=x1, y=y1, x2=x2, y2=y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
#                self.rlines.append(pyglet.shapes.Line(fri(x), fri(j*h+y), fri(nc*w+x), fri(j*h+y), width=1, color=color, batch=self.batch, group=self.lineGroup))
#                if dbg: print('j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE, end=' ')
                if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)

    def _initSciSprts(self, opq=True):
        if self.useOrderedGroup: self.sciGroup = pyglet.graphics.OrderedGroup(0)
        else:                    self.sciGroup = pyglet.graphics.Group()  #self.rootGroup)
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        self.sciSprts = []
        self.dumpGeom('_initSciSprts(BGN)')
        for r in range(nr):
            sciSprts = []
            for c in range(nc):
                scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                sci = scip.create_image(width=fri(w), height=fri(h))
                sci.anchor_x, sci.anchor_y = fri(w/2), fri(h/2)
                x, y = c*w, wh-h-r*h
                sciSprt = pyglet.sprite.Sprite(img=sci, x=x+sci.anchor_x, y=y+sci.anchor_y, batch=self.batch, group=self.sciGroup, subpixel=False)
                if opq: opacity = 255
                else:   opacity = fri(255*c/(nc-1))
                sciSprt.opacity = opacity
                sciSprts.append(sciSprt)
                if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                    self.dumpSprite('_initSciSprts() r=[{:2}] c=[{:2}] x=(c*w)={:6.1f} iax={:3} y=(wh-h-r*h)={:6.1f} iay={:3}'.format(r, c, x, sci.anchor_x, y, sci.anchor_y), sciSprt)
            self.sciSprts.append(sciSprts)

    def _initImgSprts(self, opq=True):
        if self.useOrderedGroup: self.imgGroup = pyglet.graphics.OrderedGroup(1)
        else:                    self.imgGroup = pyglet.graphics.Group() #self.rootGroup)
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        self.imgSprts, imgs, i = [], [], 0
        s = ['apple_raw.png', 'oriel.jpg', 'pyglet.png', 'jwc.jpg', 'asteroid.png']
        self.imgSprtScales = []
        self.dumpGeom('_initImgSprts(BGN)')
        for i, imageFileName in enumerate(s):
            decoder = None #pyglet.image.codecs.png.PNGImageDecoder()#            img = pyglet.image.load(imageFileName, decoder=decoder)
            img = pyglet.resource.image(imageFileName)
            imgs.append(img)
            self.imgSprtScales.append([w/img.width, h/img.height])
            img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
            print('_initImgSprts() i=[{:2}] iax={:4} iay={:4} w={:4} h={:4} imx={:5.3f} imy={:5.3f} {:6.1f} {:6.1f} decoder={} f={}'.format(i, img.anchor_x, img.anchor_y, img.width, img.height, self.imgSprtScales[i][0], self.imgSprtScales[i][1], img.width*self.imgSprtScales[i][0], img.height*self.imgSprtScales[i][1], decoder, imageFileName), file=DBG_FILE)
        for r in range(nr):
            imgSprts = []
            if opq: opacity = 255
            else:   opacity = fri(255*r/(nr-1))
            for c in range(nc):
                img = imgs[(c+r)%(i+1)]
                img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
                x, y = c*w, wh-h-r*h
                imgSprt = pyglet.sprite.Sprite(img, x=x, y=y, batch=self.batch, group=self.imgGroup, subpixel=False)
                imgSprt.opacity = opacity
#                imgSprt.scale_x, imgSprt.scale_y = w/sw, h/sh
                imgSprts.append(imgSprt)
                if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                    self.dumpSprite('_initImgSprts() r=[{:2}] c=[{:2}] x=(c*w)={:6.1f} iax={:3} y=(wh-h-r*h)={:6.1f} iay={:3}'.format(r, c, x, img.anchor_x, y, img.anchor_y), imgSprt)
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
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        x, y = 0, 0
        self.dumpGeom('on_resize(BGN)')
        for c in range(nc+1):
            x1, y1 = c*w, 0
            x2, y2 = c*w, nr*h
            self.clines[c].position = (x1, y1, x2, y2)
#            self.clines[i].position = (fri(i*w+x), fri(y), fri(i*w+x), fri(nr*h+y))
            if dbg: print('c=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        for r in range(nr+1):
            x1, y1 = 0,    r*h
            x2, y2 = nc*w, r*h
            self.rlines[r].position = (x1, y1, x2, y2)
#            self.rlines[j].position = (fri(x), fri(j*h+y), fri(nc*w+x), fri(j*h+y))
#            if dbg: print('on_resize(gridLines) j={:4} h={:6.2f} y={:6.2f} j*h={:7.2f} {:4} j*h+y={:7.2f} {:4}'.format(j, h, y, j*h, fri(j*h), j*h+y, fri(j*h+y)), file=DBG_FILE)
            if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
        for r in range(nr):
            for c in range(nc):
                x, y = c*w+w/2, wh-h-r*h+h/2
                if self.useSciSprts:
                    self.sciSprts[r][c].update(x=x, y=y, scale_x=ww/_ww, scale_y=wh/_wh)
                    self.sciSprts[r][c].rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('on_resize(sciSprts) r=[{:2}] c=[{:2}] c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(r, c, c*w, w/2, wh-h-r*h, h/2), self.sciSprts[r][c])
                if self.useImgSprts:
                    self.imgSprts[r][c].update(x=x, y=y, scale_x=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*ww/_ww, scale_y=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*wh/_wh)
                    self.imgSprts[r][c].rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('on_resize(imgSprts) r=[{:2}] c=[{:2}] c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(r, c, c*w, w/2, wh-h-r*h, h/2), self.imgSprts[r][c])

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    test = TestGui()
    pyglet.app.run()
