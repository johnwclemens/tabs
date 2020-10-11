import sys, math
import pyglet
#import pyglet.shapes# as pygshp
#import pyglet.text  # as pygtxt
#import pyglet.window# as pygwin

def fri(f): return int(math.floor(f+0.5))

class TestGui(pyglet.window.Window):
    def __init__(self):
        self.ww, self.wh = 1000, 600
        self.nc, self.nr = 20, 12
        self.w,  self.h  = self.ww/self.nc, self.wh/self.nr
        super(TestGui, self).__init__(width=self.ww, height=self.wh, resizable=True, visible=False)
        self.batch = pyglet.graphics.Batch()
        self._ww, self._wh = self.ww, self.wh
        self.COLORS=[(127, 127, 127, 195), (66, 60, 144, 195)]
        self.useSprites, self.useCBS = True, True
        if self.useCBS:     self._initCBS()
        if self.useSprites: self._initSprites()
        self.set_visible(True)

    def _initSprites(self):
        w, h = self.w, self.h
        ww, wh = self.ww, self.wh
        self.sprites, imgs, i = [], [], 0
        s = ['C:/Python36/my/tabs/apple_raw.png', 'C:/Python36/my/tabs/pyglet.png']
        self.SIM = []
        decoder = pyglet.image.codecs.png.PNGImageDecoder()
        print('_initSprites(BGN) ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(self.ww, self.wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for i, imgFileName in enumerate(s):
            tmp = pyglet.image.load(imgFileName, decoder=decoder)
            imgs.append(tmp)
            self.SIM.append([w/tmp.width, h/tmp.height])
            print('_initSprites() [{}] w={:5.1f} h={:5.1f} f={}'.format(i, w, h, imgFileName), file=DBG_FILE)
        for r in range(self.nr):
            tmp = []
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                sprite = pyglet.sprite.Sprite(imgs[(c+r)%(i+1)], x=x, y=y, batch=self.batch, subpixel=False)
                sw, sh = sprite.width, sprite.height
                sprite.scale_x, sprite.scale_y = w/sw, h/sh
                p, q = sprite.scale_x, sprite.scale_y
                tmp.append(sprite)
                if c == self.nc-1: print('_initSprites()     [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={} wh={}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
            self.sprites.append(tmp)

    def _initCBS(self):
        w, h = self.w, self.h
        ww, wh = self.ww, self.wh
        self.CBS, cbs = [], None
        print('_initCBS(BGN)     ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(self.ww, self.wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for r in range(self.nr):
            tmp=[]
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                cbp = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
                cbi = cbp.create_image(width=fri(w), height=fri(h))
                cbs = pyglet.sprite.Sprite(img=cbi, x=x, y=y, batch=self.batch, subpixel=False)
                sw, sh = cbs.width, cbs.height
                p, q = cbs.scale_x, cbs.scale_y
                tmp.append(cbs)
                if c == self.nc-1: print('  _initCBS()       [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={} wh={}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
            self.CBS.append(tmp)

    def on_resize(self, width, height):
        _ww, _wh = self._ww, self._wh
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w, self.h = self.ww/self.nc, self.wh/self.nr
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
#        print('on_resize(BGN) _p={:5.3f} _q={:5.3f} _ww={} _wh={} nc={} nr={} ww={} wh={} w={:5.1f} h={:5.1f}'.format(_p, _q, _ww, _wh, self.nc, self.nr, ww, wh, w, h), file=DBG_FILE)
        print('on_resize(BGN) _ww={} _wh={} nc={} nr={} ww={} wh={} w={:5.1f} h={:5.1f}'.format(_ww, _wh, self.nc, self.nr, ww, wh, w, h), file=DBG_FILE)
        for r in range(self.nr):
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                if self.useCBS:
                    self.CBS[r][c].update(x=x, y=y, scale_x=width/_ww, scale_y=height/_wh)
                    sw, sh = self.CBS[r][c].width, self.CBS[r][c].height
                    p, q = self.CBS[r][c].scale_x, self.CBS[r][c].scale_y
                    if c == self.nc-1: print('on_resize(CBS)     [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
                if self.useSprites:
                    self.sprites[r][c].update(x=x, y=y, scale_x=self.SIM[(r+c)%len(self.SIM)][0]*ww/_ww, scale_y=self.SIM[(r+c)%len(self.SIM)][0]*wh/_wh)
                    sw, sh = self.sprites[r][c].width, self.sprites[r][c].height
                    p, q = self.sprites[r][c].scale_x, self.sprites[r][c].scale_y
                    if c == self.nc-1: print('on_resize(sprites) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    test = TestGui()
    pyglet.app.run()
