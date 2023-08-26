import pyglet

canvas = {}
window = None

try:
    config    = pyglet.gl.Config(double_buffer=True)
    window    = pyglet.window.Window(resizable=True, config=config)
    batch     = pyglet.graphics.Batch()
    canvas[1] = pyglet.text.Label("Moo", x=10, y=10, batch=batch)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    @window.event
    def on_key_press(_, _1):
        for index in list(canvas):
            canvas[index].delete()
            del(canvas[index])

    pyglet.app.run()

finally:
    if window and not window.close: window.close()