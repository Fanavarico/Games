import turtle

# --------------------
# Setup
# --------------------
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("midnightblue")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# --------------------
# Helper
# --------------------
def filled_circle(x, y, r, color):
    t.penup()
    t.goto(x, y - r)
    t.setheading(0)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.circle(r)
    t.end_fill()

# --------------------
# Santa (FIXED)
# --------------------
def draw_santa(x, y):
    # Body
    filled_circle(x, y, 65, "red")

    # Belt
    t.penup()
    t.goto(x - 65, y - 5)
    t.setheading(0)
    t.pendown()
    t.color("black")
    t.begin_fill()
    for _ in range(2):
        t.forward(130)
        t.right(90)
        t.forward(15)
        t.right(90)
    t.end_fill()

    # Buckle
    t.penup()
    t.goto(x - 10, y - 5)
    t.pendown()
    t.color("gold")
    t.begin_fill()
    for _ in range(2):
        t.forward(20)
        t.right(90)
        t.forward(15)
        t.right(90)
    t.end_fill()

    # Head
    filled_circle(x, y + 95, 35, "peachpuff")

    # Beard
    filled_circle(x, y + 65, 40, "white")

    # Eyes
    filled_circle(x - 10, y + 105, 4, "black")
    filled_circle(x + 10, y + 105, 4, "black")

    # Nose
    filled_circle(x, y + 95, 5, "pink")

    # Smile
    t.penup()
    t.goto(x - 12, y + 90)
    t.pendown()
    t.color("deeppink") # Slightly darker for visibility
    t.setheading(-60)
    t.circle(14, 120)

    # Hat brim (Centered and lowered to touch the head)
    t.penup()
    t.goto(x - 40, y + 128)
    t.setheading(0)
    t.pendown()
    t.color("white")
    t.begin_fill()
    for _ in range(2):
        t.forward(80)
        t.right(90)
        t.forward(15)
        t.right(90)
    t.end_fill()

    # Hat Triangle (Centered equilateral-style triangle)
    t.penup()
    t.goto(x - 35, y + 128)
    t.pendown()
    t.color("red")
    t.begin_fill()
    t.goto(x + 35, y + 128) # Right base
    t.goto(x, y + 195)      # Top peak (centered at x)
    t.goto(x - 35, y + 128) # Back to left base
    t.end_fill()

    # Pom-pom (Centered on the peak)
    filled_circle(x, y + 200, 8, "white")

# --------------------
# Tree (UNCHANGED)
# --------------------
def draw_tree(x, y):
    # Trunk
    t.penup()
    t.goto(x - 15, y)
    t.setheading(0)
    t.pendown()
    t.color("saddlebrown")
    t.begin_fill()
    for _ in range(2):
        t.forward(30)
        t.right(90)
        t.forward(40)
        t.right(90)
    t.end_fill()

    t.color("darkgreen")
    layers = [(150, 0, 70), (110, 40, 60), (70, 80, 50)]
    for width, offset, height in layers:
        t.penup()
        t.goto(x - width // 2, y + offset)
        t.pendown()
        t.begin_fill()
        t.goto(x + width // 2, y + offset)
        t.goto(x, y + offset + height)
        t.goto(x - width // 2, y + offset)
        t.end_fill()

    ornaments = [(-35, 20, "red"), (35, 20, "blue"), (-20, 60, "gold"), (20, 60, "red"), (0, 95, "blue")]
    for dx, dy, c in ornaments:
        filled_circle(x + dx, y + dy, 6, c)

    t.penup()
    t.goto(x - 10, y + 130)
    t.setheading(0)
    t.pendown()
    t.color("gold")
    t.begin_fill()
    for _ in range(5):
        t.forward(20)
        t.right(144)
    t.end_fill()

# --------------------
# Draw Scene
# --------------------
# Grounded Tree
draw_tree(-100, -150)

# Santa moved closer (X: 60) and lower (Y: -125) to align with tree base
draw_santa(60, -125)

screen.mainloop()
