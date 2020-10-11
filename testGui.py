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
#        self.useCells, self.useLabels,
        self.useSprites, self.useCBS = True, True
#        if self.useCells:   self._initCells()
#        if self.useLabels:  self._initLabels()
        if self.useCBS:     self._initCBS()
        if self.useSprites: self._initSprites()
#        if self.useCells:  self.cells = [[pyglet.shapes.Rectangle(c*w, self.wh-h-r*h, w, h, color=COLORS[(c+r)%2], batch=self.batch) for c in range(self.nc)] for r in range(self.nr)]
#        if self.useLabels: self.labels = [[pyglet.text.Label('Ab', font_name='Lucida Console', font_size=16, x=c*w, y=self.wh-h-r*h, width=w, height=h, anchor_x='left', anchor_y='center', align='left', batch=self.batch) for c in range(self.nc)] for r in range(self.nr)]
        self.set_visible(True)

    '''
    def _initCells(self):
        w, h = self.w, self.h
        self.cells = []
        for r in range(self.nr):
            tmp = []
            for c in range(self.nc):
                x, y = (self.ww+c*w)/2, self.wh-h-r*h
                tmp.append(pyglet.shapes.Rectangle(x, y, w/2, h, color=self.COLORS[(c+r)%2], batch=self.batch))
            self.cells.append(tmp)

    def _initLabels(self):
        w, h = self.w, self.h
        self.labels, f, s, n, b = [], 'Lucida Console', 10, 12, self.batch
        for r in range(self.nr):
            tmp = []
            for c in range(self.nc):
                x, y, C = c*w/2, self.wh-h-r*h, (255, 255-20*r, 15+10*c, 255)
                if   c%n==0:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='left',   anchor_y='top',      align='left',   color=C, batch=b))
                elif c%n==1:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='center', anchor_y='top',      align='left',   color=C, batch=b))
                elif c%n==2:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='right',  anchor_y='top',      align='left',   color=C, batch=b))
                elif c%n==3:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='left',   anchor_y='center',   align='center', color=C, batch=b))
                elif c%n==4:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='center', anchor_y='center',   align='center', color=C, batch=b))
                elif c%n==5:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='right',  anchor_y='center',   align='center', color=C, batch=b))
                elif c%n==6:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='left',   anchor_y='bottom',   align='right',  color=C, batch=b))
                elif c%n==7:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='center', anchor_y='bottom',   align='right',  color=C, batch=b))
                elif c%n==8:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='right',  anchor_y='bottom',   align='right',  color=C, batch=b))
                elif c%n==9:  tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='left',   anchor_y='baseline', align='center', color=C, batch=b))
                elif c%n==10: tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='center', anchor_y='baseline', align='center', color=C, batch=b))
                elif c%n==11: tmp.append(pyglet.text.Label('Ab', font_name=f, font_size=s, x=x, y=y, width=w/2, height=h, anchor_x='right',  anchor_y='baseline', align='center', color=C, batch=b))
                else:         print('ERROR: c={} n={} c%%n={}'.format(c, n, c%n), file=DBG_FILE); exit(1)
                print('[{}][{}]{:6.1f},{:6.1f} '.format(r, c, tmp[c].x, tmp[c].y), file=DBG_FILE, end='')
            print(file=DBG_FILE)
            self.labels.append(tmp)
    '''
    def _initSprites(self):
        w, h = self.w, self.h
        ww, wh = self.ww, self.wh
        self.sprites, imgs, i = [], [], 0
        s = ['C:/Python36/my/tabs/apple_raw.png'] #['C:/Python36/my/tabs/pyglet.png', 'C:/Python36/my/tabs/apple_raw.png']
        decoder = pyglet.image.codecs.png.PNGImageDecoder()
        print('_initSprites(BGN) ww={} wh={} nc={} nr={} w={:5.1f} h={:5.1f}'.format(self.ww, self.wh, self.nc, self.nr, w, h), file=DBG_FILE)
        for i, imgFileName in enumerate(s):
            tmp = pyglet.image.load(imgFileName, decoder=decoder)
            imgs.append(tmp)
            print('_initSprites() [{}] w={:5.1f} h={:5.1f} f={}'.format(i, w, h, imgFileName), file=DBG_FILE)
        for r in range(self.nr):
            tmp = []
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                sprite = pyglet.sprite.Sprite(imgs[(c+r)%(i+1)], x=x, y=y, batch=self.batch, subpixel=False)
                sw, sh = sprite.width, sprite.height
                sprite.scale_x, sprite.scale_y = w/sw, h/sh
                p, q = sprite.scale_x, sprite.scale_y
                self._p, self._q = p, q
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
        _p, _q = self._p, self._q
        super().on_resize(width, height)
        self.ww, self.wh = width, height
        self.w, self.h = self.ww/self.nc, self.wh/self.nr
        ww, wh = self.ww, self.wh
        w, h = self.w, self.h
        print('on_resize(BGN) _p={:5.3f} _q={:5.3f} _ww={} _wh={} nc={} nr={} ww={} wh={} w={:5.1f} h={:5.1f}'.format(_p, _q, _ww, _wh, self.nc, self.nr, ww, wh, w, h), file=DBG_FILE)
        for r in range(self.nr):
            for c in range(self.nc):
                x, y = c*w, self.wh-h-r*h
                if self.useCBS:
                    self.CBS[r][c].update(x=x, y=y, scale_x=width/_ww, scale_y=height/_wh)
                    sw, sh = self.CBS[r][c].width, self.CBS[r][c].height
                    p, q = self.CBS[r][c].scale_x, self.CBS[r][c].scale_y
                    if c == self.nc-1: print('on_resize(CBS)     [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
                if self.useSprites:
                    self.sprites[r][c].update(x=x, y=y, scale_x=_p*ww/_ww, scale_y=_q*wh/_wh)
                    sw, sh = self.sprites[r][c].width, self.sprites[r][c].height
                    p, q = self.sprites[r][c].scale_x, self.sprites[r][c].scale_y
                    if c == self.nc-1: print('on_resize(sprites) [{:2}][{:2}] x={:6.1f} y={:6.1f} sw={:3} sh={:3} p={:5.3f} q={:5.3f} w={:5.1f} h={:5.1f} ww={:4} wh={:4}'.format(r, c, x, y, sw, sh, p, q, w, h, ww, wh), file=DBG_FILE)
#                if self.useLabels:
#                    self.labels[r][c].x,     self.labels[r][c].y      = c*w/2,           self.wh-h-r*h
#                    self.labels[r][c].width, self.labels[r][c].height = w/2,             h
#                if self.useCells:
#                    self.cells[r][c].x,      self.cells[r][c].y       = (self.ww+c*w)/2, self.wh-h-r*h
#                    self.cells[r][c].width,  self.cells[r][c].height  = w/2,             h

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    test = TestGui()
    pyglet.app.run()
