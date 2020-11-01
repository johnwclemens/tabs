import sys, math
import pyglet

def fri(f): return int(math.floor(f+0.5))

class TestGui(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nc, self.nr = 21, 13# 17, 11
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

    def _initGeom(self):
        return self._ww, self._wh, self.ww, self.wh, self.w, self.h, self.nc, self.nr

    def _initGroup(self, order=0, parent=None):
        if self.useOrderedGroup: return pyglet.graphics.OrderedGroup(order, parent)
        else:                    return pyglet.graphics.Group(parent)

    def _initGrid(self, dbg=1):
        self.lineGroup = self._initGroup(2)
        mesh, color    = [1, 5, 10], self.COLORS[0]
        _ww, _wh, ww, wh, w, h, nc, nr = self._initGeom()
        self.dumpGeom('_initGrid(BGN)')
        self.clines, self.rlines = [], []
        if nc % 2 == 0:
            p = fri(nc/2) % mesh[len(mesh)]
            if dbg: print('_initGrid() nc={}=Even p={}'.format(nc, p), file=DBG_FILE)
            for c in range(nc+1):
                x1, x2, y1, y2 = c*w, c*w, 0, nr*h
                color = self.getMeshColor(c, p, mesh)
                self.clines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('c=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        else:
            p = fri(nc/2-1)
            if dbg: print('_initGrid() nc={}=Odd p={}'.format(nc, p), file=DBG_FILE)
            for c in range(fri(nc/2)):
                x1, x2, y1, y2 = c*w, c*w, 0, nr*h
                color = self.getMeshColor(c, p, mesh)
                self.clines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('c=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
            p = fri(nc/2)
            if dbg: print('_initGrid() nc={}=Odd p={}'.format(nc, p), file=DBG_FILE)
            for c in range(fri(nc/2), nc+1):
                x1, x2, y1, y2 = c*w, c*w, 0, nr*h
                color = self.getMeshColor(c, p, mesh)
                self.clines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('c=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        if nr % 2 == 0:
            q = fri(nr/2) % mesh[len(mesh)]
            if dbg: print('_initGrid() nr={}=Even q={}'.format(nr, q), file=DBG_FILE)
            for r in range(nr+1):
                x1, x2, y1, y2 = 0, nc*w, r*h, r*h
                color = self.getMeshColor(r, q, mesh)
                self.rlines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('r=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
        else:
            q = fri(nr/2-1)
            if dbg: print('_initGrid() nr={}=Odd q={}'.format(nr, q), file=DBG_FILE)
            for r in range(fri(nr/2)):
                x1, x2, y1, y2 = 0, nc*w, r*h, r*h
                color = self.getMeshColor(r, q, mesh)
                self.rlines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('r=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
            q = fri(nr/2)
            if dbg: print('_initGrid() nr={}=odd q={}'.format(nr, q), file=DBG_FILE)
            for r in range(fri(nr/2), nr+1):
                x1, x2, y1, y2 = 0, nc*w, r*h, r*h
                color = self.getMeshColor(r, q, mesh)
                self.rlines.append(pyglet.shapes.Line(x1, y1, x2, y2, width=1, color=color, batch=self.batch, group=self.lineGroup))
                if dbg: print('r=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)

    def _initImgSprts(self):
        self.imgGroup = self._initGroup(1)
        _ww, _wh, ww, wh, w, h, nc, nr = self._initGeom()
        iss, self.imgSprts, imgs, i = [], [], [], 0
        s = ['apple_raw.png', 'oriel.jpg']#, 'pyglet.png', 'jwc.jpg', 'asteroid.png']
        self.dumpGeom('_initImgSprts(BGN)')
        for i, imageFileName in enumerate(s):
            img = pyglet.resource.image(imageFileName)
            imgs.append(img)
            img.width, img.height = w, h
            iss.append([w/img.width, h/img.height])
            img.anchor_x, img.anchor_y = fri(img.width/2), fri(img.height/2)
            print('_initImgSprts() i=[{:2}] iax={:4} iay={:4} w={:8.2f} h={:8.2f} imx={:5.3f} imy={:5.3f} {:6.1f} {:6.1f} f={}'.format(i, img.anchor_x, img.anchor_y, img.width, img.height, iss[i][0], iss[i][1], img.width*iss[i][0], img.height*iss[i][1], imageFileName), file=DBG_FILE)
        self.dumpSprite(None)
        for r in range(nr):
            imgSprts = []
            for c in range(nc):
                img = imgs[(c+r)%(i+1)]
                imgSprt = self.createSprite('_initImgSprts()', img, self.imgGroup, c, r, w, h, r, 0)#nr)
                imgSprts.append(imgSprt)
            self.imgSprts.append(imgSprts)
        self.iss = iss

    def _initSciSprts(self):
        self.sciGroup = self._initGroup(0)
        _ww, _wh, ww, wh, w, h, nc, nr = self._initGeom()
        self.sciSprts = []
        self.dumpGeom('_initSciSprts(BGN)')
        self.dumpSprite(None)
        for r in range(nr):
            sciSprts = []
            for c in range(nc):
                scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                sci = scip.create_image(width=fri(w), height=fri(h))
                sciSprt = self.createSprite('_initSciSprts()', sci, self.sciGroup, c, r, w, h, c, 0)#nc)
                sciSprts.append(sciSprt)
            self.sciSprts.append(sciSprts)

    def createSprite(self, reason, img, grp, c, r, w, h, i, ni):
        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        x, y = c*w+w/2, self.wh-h-r*h+h/2
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        s.opacity = self.getOpacity(OPC, i, ni)
        if c==0 or r==0 or c==self.nc-1 or r==self.nr-1:
            self.dumpSprite('{:20} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format(reason, r, c, x, y, img.anchor_x, img.anchor_y), s)
        return s

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('     x        y        w        h    iax  iay    m      mx     my      rot   opacity    color      visible      reason          r     c        x        y    iax  iay', file=DBG_FILE); return
        f = '{:8.2f} {:8.2f} {:8.2f} {:8.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:8.2f}  {:4}  {}  {}'
        fs = f.format(s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, s.opacity, s.color, s.visible)
        print('{} {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    @staticmethod
    def getMeshColor(i, j, mesh):
        MIN, NOM, MAX = 0, 1, 2
        MESH          = [(255, 0, 0), (0, 255, 0), (255, 255, 255)]
        if   (i-j) % mesh[MAX]==0: return MESH[MAX]
        elif (i-j) % mesh[NOM]==0: return MESH[NOM]
        elif (i-j) % mesh[MIN]==0: return MESH[MIN]

    @staticmethod
    def getOpacity(opacity=255, i=0, ni=0):
        if ni <= 0: return opacity
        else:       return fri(opacity*((i+1) % (ni+1))/ni)

    def dumpGeom(self, reason):
        print('{:32} _ww={} nc={} w={:7.2f} ww-w={:7.2f} ww-w/2={:7.2f} ww={}    _wh={} nr={} h={:7.2f} wh-h={:7.2f} wh-h/2={:7.2f} wh={}'
              .format(reason, self._ww, self.nc, self.w, self.ww-self.w, self.ww-self.w/2, self.ww, self._wh, self.nr, self.h, self.wh-self.h, self.wh-self.h/2, self.wh), file=DBG_FILE)

    def on_resize(self, width, height, dbg=1):
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        _ww, _wh, ww, wh, w, h, nc, nr = self._initGeom()
        self.dumpGeom('\non_resize(BGN)')
        for c in range(nc+1):
            x1, x2, y1, y2 = c*w, c*w, 0, nr*h
            self.clines[c].position = (x1, y1, x2, y2)
            if dbg: print('c=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(c, x1, y1, x2, y2), file=DBG_FILE)
        for r in range(nr+1):
            x1, x2, y1, y2 = 0, nc*w, r*h, r*h
            self.rlines[r].position = (x1, y1, x2, y2)
            if dbg: print('r=[{:3}] x1={:7.2f} y1={:7.2f} x2={:7.2f} y2={:7.2f}'.format(r, x1, y1, x2, y2), file=DBG_FILE)
        if self.useSciSprts:
            self.dumpSprite(None)
            for r in range(nr):
                for c in range(nc):
                    x, y = c*w+w/2, wh-h-r*h+h/2
                    s = self.sciSprts[r][c]
                    s.update(x, y, scale_x=ww/_ww, scale_y=wh/_wh)
                    s.rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('{:20} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format('on_resize(sciSprts)', r, c, x, y, s.image.anchor_x, s.image.anchor_y), s)
        if self.useImgSprts:
            self.dumpSprite(None)
            for r in range(nr):
                for c in range(nc):
                    x, y = c*w+w/2, wh-h-r*h+h/2
                    s = self.imgSprts[r][c]
                    s.update(x, y, scale_x=self.iss[(r+c)%len(self.iss)][0]*ww/_ww, scale_y=self.iss[(r+c)%len(self.iss)][0]*wh/_wh)
                    s.rotation = 22.5 * c
                    if c == 0 or r == 0 or c == nc-1 or r == nr-1:
                        self.dumpSprite('{:20} [{:3}] [{:3}] {:8.2f} {:8.2f} {:4} {:4}'.format('on_resize(imgSprts)', r, c, x, y, s.image.anchor_x, s.image.anchor_y), s)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    OPC, SUBPIX = 255, True
    SFX = '.log.SPX.txt' if SUBPIX else '.log.txt'
    DBG_FILE = open(sys.argv[0] + SFX, 'w')
    test = TestGui()
    pyglet.app.run()
