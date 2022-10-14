from glob import glob
import pygame as pg

CENTER = 'center'
CORNER = 'corner'
PI = 3.141592653589793
TWO_PI = PI * 2
HALF_PI = PI / 2


looping = True
pg.init()
pg.display.set_caption("Jam-Burger")
scr = pg.display.set_mode((400, 300))
clock = pg.time.Clock()

fill_color = (255, 255, 255)
stroke_color = (0, 0, 0)
sw = 1

rectMode = CORNER
ellipseMode = CENTER
imageMode = CORNER
fill_shape = True
stroke_shape = True
shape = []
running = True
frame_rate = 60
tk_root = None
# font = pg.font.Font('Sans serif', 32)

font_style = pg.font.SysFont('roboto', 20)


def test():
    return 'success'


def size(w, h):
    global scr
    scr = pg.display.set_mode((w, h))


def title(title):
    pg.display.set_caption(title)


def none():
    pass


def no_loop():
    global looping
    looping = False


def framerate(f):
    global frame_rate
    frame_rate = f


def set_tk_root(r):
    global tk_root
    tk_root = r


def close_screen():
    global running
    running = False


def run(setup=none, draw=none, mouse_pressed=none, mouse_released=none, mouse_dragged=none, key_pressed=none):
    global mouseX, mouseY, running
    setup()
    while running:
        if tk_root:
            try:
                tk_root.update()
            except:
                print("tk root error!")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_screen()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pressed()
            elif event.type == pg.MOUSEMOTION and mouse_is_pressed():
                mouse_dragged()
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_released()
            if event.type == pg.KEYDOWN:
                key_pressed()

        if looping:
            draw()
            pg.display.flip()
            clock.tick(frame_rate)

    if tk_root:
        tk_root.destroy()


def color(lst):
    if len(lst) == 0:
        t = (0, 0, 0)
    elif len(lst) == 1:
        t = (lst[0], lst[0], lst[0]) if (type(lst[0]) == type(0)) else lst[0]
    elif len(lst) == 2:
        t = (lst[0], lst[0], lst[0])
    else:
        t = lst

    return t


def background(*lst, img=None):
    if img is None:
        scr.fill(color(lst))
    else:
        width, height = get_size()
        img = pg.transform.scale(img, (width, height))
        scr.blit(img, (0, 0))


def fill(*lst):
    global fill_shape, fill_color
    fill_shape = True
    fill_color = color(lst)


def stroke(*lst):
    global stroke_shape, stroke_color
    stroke_shape = True
    stroke_color = color(lst)


def rect_mode(mode):
    global rectMode
    rectMode = mode


def ellipse_mode(mode):
    global ellipseMode
    ellipseMode = mode


def image_mode(mode):
    global imageMode
    imageMode = mode


def no_fill():
    global fill_shape
    fill_shape = False


def no_stroke():
    global stroke_shape
    stroke_shape = False


def stroke_weight(s):
    global sw
    sw = int(s)


def font_size(fs):
    global font_style
    font_style = pg.font.SysFont('roboto', fs)


def mouse(): return pg.mouse.get_pos()
def get_size(): return scr.get_size()


def rect(pos, w, h, br=-1):
    x, y = pos
    if rectMode == CENTER:
        x -= w/2
        y -= h/2
    if fill_shape:
        pg.draw.rect(scr, fill_color, (x, y, w, h), 0, br)
    if stroke_shape:
        pg.draw.rect(scr, stroke_color, (x, y, w, h), sw, br)


def square(pos, w, br=-1):
    rect(pos, w, w, br)


def ellipse(pos, w, h):
    x, y = pos
    if ellipseMode == CENTER:
        x -= w/2
        y -= h/2
    if fill_shape:
        pg.draw.ellipse(scr, fill_color, (x, y, w, h))
    if stroke_shape:
        pg.draw.ellipse(scr, stroke_color, (x, y, w, h), sw)


def circle(pos, r):
    ellipse(pos, r*2, r*2)


def arc(pos, w, h, sa, ea):
    x, y = pos
    if ellipseMode == CENTER:
        x -= w/2
        y -= h/2
    if stroke_shape:
        pg.draw.arc(scr, stroke_color, (x, y, w, h), sa, ea, sw)


def line(x1, y1, x2, y2):
    if stroke_shape:
        pg.draw.line(scr, stroke_color, (x1, y1), (x2, y2), sw)


def triangle(pos1, pos2, pos3):
    if fill_shape:
        pg.draw.polygon(scr, fill_color, (pos1, pos2, pos3))
    if stroke_shape:
        pg.draw.polygon(scr, stroke_color, (pos1, pos2, pos3), sw)


def text(txt, pos, w, h):
    x, y = pos
    if rectMode == CENTER:
        x -= w/2
        y -= h/2
    txt = font_style.render(txt, True, fill_color, 'white')
    scr.blit(txt, [x, y, w, h])


def begin_shape():
    global shape
    shape = []


def vertex(x, y):
    shape.append((x, y))


def end_shape():
    if fill_shape:
        pg.draw.polygon(scr, fill_color, shape)
    if stroke_shape:
        pg.draw.polygon(scr, stroke_color, shape, sw)


def load_image(path):
    return pg.image.load(path)


def image(img, pos, size=None):
    x, y = pos
    if size is not None:
        img = pg.transform.smoothscale(img, size)

    w, h = img.get_size()
    if imageMode == CENTER:
        x -= w/2
        y -= h/2

    scr.blit(img, (x, y))


def key_is_pressed(key):
    return pg.key.get_pressed()[key]


def mouse_is_pressed(btn=0):
    return pg.mouse.get_pressed()[btn]
