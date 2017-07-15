import pyglet
window = pyglet.window.Window()
text = "1234"
fSize = 16
label = pyglet.text.Label(text,
                          font_name='Times New Roman',
                          font_size=fSize,
                          x=-80, y=-80,
                          anchor_x='left', anchor_y='bottom')

@window.event
def on_draw():
    window.clear()
    label.draw()
    
pyglet.app.run()
