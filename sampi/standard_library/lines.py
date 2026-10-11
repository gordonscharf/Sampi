import turtle

screen = None
pen = None

def setup_screen():
    global screen, pen

    if screen is None:
        screen = turtle.Screen()
        screen.tracer(0)
        screen.colormode(255)
        screen.title("lines")

        pen = turtle.Turtle()
        pen.speed(0)
        pen.hideturtle()

def draw_line(x1, y1, x2, y2):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y2)

def fill_tri(x1, y1, x2, y2, x3, y3):
    pen.begin_fill()
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)
    pen.end_fill()

def set_color(c):
    pen.color(c)
    pen.fillcolor(c)

def set_title(name):
    screen.title(name)

def set_width(w):
    pen.width(w)

def clear():
    pen.clear()

def update():
    screen.update()

def setup_screen(width, hight, bg):
    screen.screensize(width, hight, bg)
    
new_funcs = {func.__name__: (func, args) for func, args in [
    (draw_line, 4),
    (fill_tri, 6),
    (set_color, 1),
    (set_width, 1),
    (set_title, 1),
    (clear, 0),
    (update, 0),
    (setup_screen, 3)
    ]}

new_vars = {}