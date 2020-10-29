import sys, math
import pyglet

def fri(f): return int(math.floor(f+0.5))

class TestGui(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nc, self.nr = 19, 7# 17, 11
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        super(TestGui, self).__init__(width=self.ww, height=self.wh, resizable=True, visible=False)
        pyglet.resource.path = ['res', 'res/images']
        pyglet.resource.reindex()
        self.batch = pyglet.graphics.Batch()
        self.COLORS=[(227, 147, 127, 255), (66, 60, 144, 255)]
        self.useSciSprts, self.useImgSprts, self.useOrderedGroup, self.useGridLines = True, True, True, True
        print('_init(BGN) useImgSprts={} useSciSprts={}, useOrderedGroup={} useGridLines={}'.format(self.useImgSprts, self.useSciSprts, self.useOrderedGroup, self.useGridLines), file=DBG_FILE)
        if self.useSciSprts:  self._initSciSprts()
        if self.useImgSprts:  self._initImgSprts()
        if self.useGridLines: self._initGrid()
        self.set_visible(True)

    def dumpGeom(self, reason):
        print('{:32} _ww={} nc={} w={:6.1f} ww-w={:6.1f} ww={}  :  _wh={} nr={} h={:6.1f} wh-h={:6.1f} wh={}'
              .format(reason, self._ww, self.nc, self.w, self.ww-self.w, self.ww, self._wh, self.nr, self.h, self.wh-self.h, self.wh), file=DBG_FILE)

    def getGeom(self):
        return self._ww, self._wh, self.ww, self.wh, self.w, self.h, self.nc, self.nr

    def _initGroup(self, order=0, parent=None):
        if self.useOrderedGroup: return pyglet.graphics.OrderedGroup(order, parent)
        else:                    return pyglet.graphics.Group(parent)

    def _initGrid(self, dbg=1):
        self.lineGroup = self._initGroup(2)
        self.MIN, self.NOM, self.MAX = 0, 1, 2
        self.MESH      = [(255, 0, 0), (0, 255, 0), (255, 255, 255)]
        mesh, color    = [1, 5, 10], self.COLORS[0]
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
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
                if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)

    def _initImgSprts(self):
        self.imgGroup = self._initGroup(1)
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        iss, self.imgSprts, imgs, i = [], [], [], 0
        s = ['apple_raw.png', 'oriel.jpg']#, 'pyglet.png', 'jwc.jpg', 'asteroid.png']
        self.dumpGeom('_initImgSprts(BGN)')
        for i, imageFileName in enumerate(s):
            img = pyglet.resource.image(imageFileName)
            imgs.append(img)
            img.width, img.height = w, h
            iss.append([w/img.width, h/img.height])
            img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
            print('_initImgSprts() i=[{:2}] iax={:4} iay={:4} w={:4} h={:4} imx={:5.3f} imy={:5.3f} {:6.1f} {:6.1f} f={}'.format(i, img.anchor_x, img.anchor_y, img.width, img.height, iss[i][0], iss[i][1], img.width*iss[i][0], img.height*iss[i][1], imageFileName), file=DBG_FILE)
        self.dumpSprite(None)
        for r in range(nr):
            imgSprts = []
            for c in range(nc):
                img = imgs[(c+r)%(i+1)]
                imgSprt = self.createSprite('_initImgSprts()', img, self.imgGroup, c, r, w, h, r, 0)#nr)
#                img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
#                imgSprt = pyglet.sprite.Sprite(img, x=x, y=y, batch=self.batch, group=self.imgGroup, subpixel=False)
#                imgSprt.scale_x, imgSprt.scale_y = w/sw, h/sh
                imgSprts.append(imgSprt)
            self.imgSprts.append(imgSprts)
        self.iss = iss

    def _initSciSprts(self):
        self.sciGroup = self._initGroup(0)
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        self.sciSprts = []
        self.dumpGeom('_initSciSprts(BGN)')
        self.dumpSprite(None)
        for r in range(nr):
            sciSprts = []
            for c in range(nc):
                scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                sci = scip.create_image(width=fri(w), height=fri(h))
                sciSprt = self.createSprite('_initSciSprts()', sci, self.sciGroup, c, r, w, h, c, 0)#nc)
#                sci.anchor_x, sci.anchor_y = fri(w/2), fri(h/2)
#                sciSprt = pyglet.sprite.Sprite(img=sci, x=x+sci.anchor_x, y=y+sci.anchor_y, batch=self.batch, group=self.sciGroup, subpixel=False)
                sciSprts.append(sciSprt)
            self.sciSprts.append(sciSprts)

    def createSprite(self, reason, img, grp, c, r, w, h, i, ni):
        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        x, y = c*w+w/2, self.wh-h-r*h+h/2
        s = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=self.batch, group=grp, subpixel=True)
        s.opacity = self.getOpacity(203, i, ni)
        if c==0 or r==0 or c==self.nc-1 or r==self.nr-1:
            self.dumpSprite('{:24} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format(reason, r, c, x, y, img.anchor_x, img.anchor_y), s)
        return s

    @staticmethod
    def getOpacity(opacity=255, i=0, ni=0):
        if ni <= 0: return opacity
        else:       return fri(opacity*((i+1) % (ni+1))/ni)

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('     x        y        w        h    iax  iay    m      mx     my      rot   opacity    color      visible      reason                r     c        x        y    iax  iay', file=DBG_FILE); return
        f = '{:8.2f} {:8.2f} {:8.2f} {:8.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:8.2f}  {:4}  {}  {}'
        fs = f.format(s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, s.opacity, s.color, s.visible)
        print('{} : {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    def on_resize(self, width, height, dbg=1):
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        _ww, _wh, ww, wh, w, h, nc, nr = self.getGeom()
        self.dumpGeom('\non_resize(BGN)')
        for c in range(nc+1):
            x1, y1 = c*w, 0
            x2, y2 = c*w, nr*h
            self.clines[c].position = (x1, y1, x2, y2)
            if dbg: print('c=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        for r in range(nr+1):
            x1, y1 = 0,    r*h
            x2, y2 = nc*w, r*h
            self.rlines[r].position = (x1, y1, x2, y2)
            if dbg: print('r=[{:3}] x1={:6.1f} y1={:6.1f} x2={:6.1f} y2={:6.1f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
        if self.useSciSprts:
            self.dumpSprite(None)
            for r in range(nr):
                for c in range(nc):
                    x, y = c*w+w/2, wh-h-r*h+h/2
                    s = self.sciSprts[r][c]
                    s.update(x=x, y=y, scale_x=ww/_ww, scale_y=wh/_wh)
                    s.rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('{:24} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format('on_resize(sciSprts)', r, c, x, y, s.image.anchor_x, s.image.anchor_y), s)
#                        self.dumpSprite('on_resize(sciSprts) [{:3}] [{:3}] c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(r, c, c*w, w/2, wh-h-r*h, h/2), s)
        if self.useImgSprts:
            self.dumpSprite(None)
            for r in range(nr):
                for c in range(nc):
                    x, y = c*w+w/2, wh-h-r*h+h/2
                    s = self.imgSprts[r][c]
                    s.update(x=x, y=y, scale_x=self.iss[(r+c)%len(self.iss)][0]*ww/_ww, scale_y=self.iss[(r+c)%len(self.iss)][0]*wh/_wh)
                    s.rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('{:24} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format('on_resize(imgSprts)', r, c, x, y, s.image.anchor_x, s.image.anchor_y), s)
#                        self.dumpSprite('on_resize(imgSprts) [{:3}] [{:3}] c*w={:6.1f} w/2={:6.1f} wh-h-r*h={:6.1f} h/2={:6.1f}'.format(r, c, c*w, w/2, wh-h-r*h, h/2), self.imgSprts[r][c])

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE, OPC = open(sys.argv[0] + ".log.txt", 'w'), 255
    test = TestGui()
    pyglet.app.run()
