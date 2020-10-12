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
        self.nc, self.nr = 20, 12
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        super(TestGui, self).__init__(width=self.ww, height=self.wh, resizable=True, visible=False)
        self.batch = pyglet.graphics.Batch()
        self.COLORS=[(227, 147, 127, 255), (66, 60, 144, 255)]
        self.useSciSprts, self.useImgSprts = True, True
        if self.useSciSprts: self._initSciSprts(opq=False)
        if self.useImgSprts: self._initImgSprts(opq=False)
        self.set_visible(True)

    def _initImgSprts(self, opq=True):
        w, h = self.w, self.h
        ww, wh = self.ww, self.wh
        self.imgSprts, imgs, i = [], [], 0
        s = ['C:/Python36/my/tabs/apple_raw.png', 'C:/Python36/my/tabs/pyglet.png', 'C:/Python36/my/tabs/asteroid.png']
        self.imgSprtScales = []
        decoder = pyglet.image.codecs.png.PNGImageDecoder()
        print('_initImgSprts(BGN) ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(self.ww, self.wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for i, imageFileName in enumerate(s):
            img = pyglet.image.load(imageFileName, decoder=decoder)
            imgs.append(img)
            self.imgSprtScales.append([w/img.width, h/img.height])
            print('_initImgSprts()      [{}] w={:5.1f} h={:5.1f} f={}'.format(i, w, h, imageFileName), file=DBG_FILE)
        for r in range(self.nr):
            imgSprts = []
            if opq: opacity = 255
            else:   opacity = fri(255*r/(self.nr-1))
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                imgSprt = pyglet.sprite.Sprite(imgs[(c+r)%(i+1)], x=x, y=y, batch=self.batch, subpixel=False)
                imgSprt.opacity = opacity
                sw, sh = imgSprt.width, imgSprt.height
                imgSprt.scale_x, imgSprt.scale_y = w/sw, h/sh
                p, q = imgSprt.scale_x, imgSprt.scale_y
                imgSprts.append(imgSprt)
                if c == self.nc-1: print('_initImgSprts()     [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={} wh={} opacity={}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh, opacity), file=DBG_FILE)
            self.imgSprts.append(imgSprts)

    def _initSciSprts(self, opq=True):
        w, h = self.w, self.h
        ww, wh = self.ww, self.wh
        self.sciSprts = []
        print('_initSciSprts(BGN) ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(self.ww, self.wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for r in range(self.nr):
            sciSprts=[]
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                sci = scip.create_image(width=fri(w), height=fri(h))
                sciSprt = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, subpixel=False)
                if opq: opacity = 255
                else:   opacity = fri(255*c/(self.nc-1))
                sciSprt.opacity = opacity
                sw, sh = sciSprt.width, sciSprt.height
                p, q = sciSprt.scale_x, sciSprt.scale_y
                sciSprts.append(sciSprt)
                if r == self.nr-1: print('_initSciSprts()     [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={} wh={} opacity={}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh, opacity), file=DBG_FILE)
            self.sciSprts.append(sciSprts)

    def on_resize(self, width, height):
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
                    self.sciSprts[r][c].update(x=x, y=y, scale_x=width/_ww, scale_y=height/_wh)
                    sw, sh = self.sciSprts[r][c].width, self.sciSprts[r][c].height
                    p, q = self.sciSprts[r][c].scale_x, self.sciSprts[r][c].scale_y
                    if c == self.nc-1: print('on_resize(sciSprts) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
                if self.useImgSprts:
                    self.imgSprts[r][c].update(x=x, y=y, scale_x=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*ww/_ww, scale_y=self.imgSprtScales[(r+c)%len(self.imgSprtScales)][0]*wh/_wh)
                    sw, sh = self.imgSprts[r][c].width, self.imgSprts[r][c].height
                    p, q = self.imgSprts[r][c].scale_x, self.imgSprts[r][c].scale_y
                    if c == self.nc-1: print('on_resize(imgSprts) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    test = TestGui()
    pyglet.app.run()
