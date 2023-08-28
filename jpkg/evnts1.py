import pyglet
import pyglet.text         as text
import pyglet.window       as window
import pyglet.window.event as pygwevnt
#import pyglet.event        as pygevnt
import pyglet.window.key   as pygwink
from   tpkg import utl     as utl

slog = utl.slog

class EventLogFilter(pygwevnt.WindowEventLogger):
#class EventLogFilter(pyglet.window.event.WindowEventLogger):
    def __init__(self, etypes):
        super().__init__()
        self.etypes = etypes

    def log(self, msg, etype=None, f=-1):
#        etype = msg.split('='[1].strip())
        if   etype and etype not in self.etypes:
            slog(msg, f=f)
        elif not etype:
            slog(msg, f=f)
#        else:
#            slog(f'FILTERED {msg}', f=f)

flist   = ['on_draw', 'on_move', 'on_text', 'on_text_motion', 'on_mouse_motion'] # 'on_draw', 'on_move', 'on_text', 'on_text_motion', 'on_mouse_motion'
wnd     = window.Window()
evntLog = EventLogFilter(flist)
wnd.push_handlers(evntLog)
lbl     = text.Label('Hello, world', font_name='Times New Roman', font_size=36, x=wnd.width//2, y=wnd.height//2, anchor_x='center', anchor_y='center')
elog    = evntLog.log
W, Y, Z = utl.W, utl.Y, utl.Z
####################################################################################################################################################################################################
def fmtEvntTxt(symb, mods=0, why=Z):   return f'{symb=} {mods=} {why}'
#def fmtEvntTxt(symb, mods, why=Z):   why = why if why else W*4   ;   return f'<{why}> <{symb=:8}> <{pygwink.symbol_string(symb)=:16}> <{mods=:2}> <{pygwink.modifiers_string(mods)=:16}>'
####################################################################################################################################################################################################
@wnd.event
def on_draw():
    elog('', etype='on_draw')
    wnd.clear()
    lbl.draw()

@wnd.event
def on_move(x, y):
    retv = True
    elog(f'{x=} {y=}', etype='on_move')
    return retv

@wnd.event
def on_text(txt):
    retv = True
    evntTxt = fmtEvntTxt(txt)
    elog(f'{txt=} {evntTxt=}', etype='on_text')
    return retv

@wnd.event
def on_text_motion(motion):
    retv = True
    evntTxt = fmtEvntTxt(motion)
    elog(f'{motion=} {evntTxt=}', etype='on_text_motion')
    return retv

@wnd.event
def on_mouse_motion(x, y, dx, dy):
    retv = True
    elog(f'{x=} {y=} {dx=} {dy=}', etype='on_mouse_motion')
    return retv

@wnd.event
def on_key_press(symb, mods):
    retv    = False
    evntTxt = fmtEvntTxt(symb, mods)
    if   symb == 'C' and isCtlSft(mods):    elog(f'@^C  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'C' and isCtl(   mods):    elog(f'@ C  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'C':                       elog(f'  C  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'D' and isCtlSft(mods):    elog(f'@^D  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'D' and isCtl(   mods):    elog(f'@ D  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'V' and isCtlSft(mods):    elog(f'@^V  {evntTxt}', etype='on_key_press')  ;  retv = True
    elif symb == 'V' and isCtl(   mods):    elog(f'@ V  {evntTxt}', etype='on_key_press')  ;  retv = True
    # if   symb == 'C' and isCtrlShift(mods):   elog(f'@^C  {evntTxt}')
    # elif symb == 'C' and isCtrl(     mods):   elog(f'@ C  {evntTxt}')
    # elif symb == 'D' and isCtrlShift(mods):   elog(f'@^D  {evntTxt}')
    # elif symb == 'D' and isCtrl(     mods):   elog(f'@ D  {evntTxt}')
    # elif symb == 'V' and isCtrlShift(mods):   elog(f'@^V  {evntTxt}')
    # elif symb == 'V' and isCtrl(     mods):   elog(f'@ V  {evntTxt}')
####################################################################################################################################################################################################
    # elif kbk == 'B' and self.isAltShift(mods):     self.setFontParam(BOLD,      not self.fontBold,                           'fontBold')
    # elif kbk == 'B' and self.isAlt(     mods):     self.setFontParam(BOLD,      not self.fontBold,                           'fontBold')
    # elif kbk == 'C' and self.isAltShift(mods):     self.setFontParam(COLOR,         1,                                       'clrIdx')
    # elif kbk == 'C' and self.isAlt(     mods):     self.setFontParam(COLOR,        -1,                                       'clrIdx')
    # elif kbk == 'I' and self.isAltShift(mods):     self.setFontParam(ITALIC,    not self.fontItalic,                         'fontItalic')
    # elif kbk == 'I' and self.isAlt(     mods):     self.setFontParam(ITALIC,    not self.fontItalic,                         'fontItalic')
    # elif kbk == 'A' and self.isAltShift(mods):     self.setFontParam(FONT_NAME,     1,                                       'fontNameIdx')
    # elif kbk == 'A' and self.isAlt(     mods):     self.setFontParam(FONT_NAME,    -1,                                       'fontNameIdx')
    # elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam(FONT_SIZE,     33 / 32,                                 'fontSize')
    # elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam(FONT_SIZE,     32 / 33,                                 'fontSize')
#    else:                                   elog(f'UNH  {evntTxt} Unhandled', f=-1)
    return retv
####################################################################################################################################################################################################
@wnd.event
def on_key_release(symb, mods):
    retv    = 0
    evntTxt = fmtEvntTxt(symb, mods)
    if   symb == 'C' and isCtlSft(mods):    elog(f'@^C  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'C' and isCtl(   mods):    elog(f'@ C  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'C':                       elog(f'  C  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'D' and isCtlSft(mods):    elog(f'@^D  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'D' and isCtl(   mods):    elog(f'@ D  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'V' and isCtlSft(mods):    elog(f'@^V  {evntTxt}', etype='on_key_release')  ;  retv = True
    elif symb == 'V' and isCtl(   mods):    elog(f'@ V  {evntTxt}', etype='on_key_release')  ;  retv = True
#    else:                                   elog(f'UNH  {evntTxt} Unhandled', f=-1)
    return retv

def isSft(      mods): return mods & pygwink.MOD_SHIFT
def isCtl(      mods): return mods & pygwink.MOD_CTRL
def isAlt(      mods): return mods & pygwink.MOD_ALT
def isCtlSft(   mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_SHIFT
def isAltSft(   mods): return mods & pygwink.MOD_ALT     and mods & pygwink.MOD_SHIFT
def isCtlAlt(   mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_ALT
def isCtlAltSft(mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_ALT   and mods & pygwink.MOD_SHIFT
def isNumLck(   mods): return mods & pygwink.MOD_NUMLOCK
# def isShift(       mods): return mods & pygwink.MOD_SHIFT
# def isCtrl(        mods): return mods & pygwink.MOD_CTRL
# def isAlt(         mods): return mods & pygwink.MOD_ALT
# def isCtrlShift(   mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_SHIFT
# def isAltShift(    mods): return mods & pygwink.MOD_ALT     and mods & pygwink.MOD_SHIFT
# def isCtrlAlt(     mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_ALT
# def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL    and mods & pygwink.MOD_ALT   and mods & pygwink.MOD_SHIFT
# def isNumLock(     mods): return mods & pygwink.MOD_NUMLOCK

def main():
#    elog('Call pyglet.app.run()')
    pyglet.app.run()
#    elog('Exit pyglet.app.run()')

if __name__ == '__main__':
    main()
