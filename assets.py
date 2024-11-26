from turtle import Turtle


class Keeper(Turtle):
    """Keeper class draws any required lines around the screen for cosmetic purposes & contains border data"""
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.teleport(x=-(width/2), y=-(height/2)+(height/15))
        self.seth(90)
        self.ht()
        self.pen({
            "pencolor": "gold",
            "pensize": 5,
            "outline": 1,
        })
        self.draw_line()

    def draw_line(self):
        self.pendown()
        self.goto(x=(self.width/2), y=-(self.height/2) + (self.height/15))

    def write_text_old(self, text, xcor, ycor):
        self.penup()
        self.goto(x=xcor, y=ycor)
        self.write(text, align="center", font=('Oswald', 36, 'normal'))

    def write_text(self, text, position, font=("Oswald", 36, "normal"),
                   padding=10, bg_color="white", text_color="gold"):
        """
        Write text with a background color that appears and disappears together.

        Args:
            self: The turtle instance used for drawing.
            text: The string to write.
            position: A tuple (x, y) for the text position.
            font: The font specification for the text.
            padding: The padding around the text for the background.
            bg_color: The background color.
            text_color: The text color.
        """
        # Save the turtle's initial state
        self.penup()
        self.goto(position)

        # Calculate the size of the text's bounding box
        width = self.width
        height = font[1]  # Use the font size as the height approximation
        y_pos = 45

        # Draw the rectangle (background)
        self.fillcolor(bg_color)
        self.begin_fill()
        self.goto(-(width/2) - padding, y_pos - height - padding)
        self.goto(-(width/2) + width + padding, y_pos - height - padding)
        self.goto(-(width/2) + width + padding, y_pos + padding)
        self.goto(-(width/2) - padding, y_pos + padding)
        self.goto(-(width/2) - padding, y_pos - height - padding)
        self.end_fill()

        # Write the text
        self.goto(position)
        self.color(text_color)
        self.write(text, align="center", font=font)


class Ship(Turtle):
    """Creates a player ship class, gives it the indicated shape and places it at given x, y coordinates.
    Also includes ship movement(left & right) & player ship deletion methods."""
    def __init__(self, shape, x_pos, y_pos, width, height, ship_type="alien"):
        super().__init__()
        self.width = width
        self.height = height
        self.shape(shape)
        self.penup()
        self.teleport(x_pos, y_pos)
        self.shapesize(0.1, 0.1)
        self.seth(0)
        self.player_turtle = self
        self.name = f"{ship_type} ship"

    def at_left_border(self, collision_distance=40):
        distance_from_left_border = self.distance((-(self.width / 2), self.ycor()))
        return distance_from_left_border <= collision_distance

    def at_right_border(self, collision_distance=40):
        distance_from_right_border = self.distance(((self.width / 2), self.ycor()))
        return distance_from_right_border <= collision_distance

    def move_left(self, distance):
        if not self.at_left_border():
            self.backward(distance)

    def move_right(self, distance):
        if not self.at_right_border():
            self.forward(distance)

    def delete(self):
        self.hideturtle()
        self.clear()
        del self


class Projectile(Turtle):
    """Creates a projectile that appears at the given x, y coordinates and travels towards the indicated heading.
    Also contains movement and projectile deletion methods"""
    def __init__(self, shape, x_pos, y_pos, heading, projectile_type="Alien"):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.teleport(x_pos, y_pos)
        self.seth(heading)
        self.name = f"{projectile_type} projectile"

    def move(self, speed):
        self.forward(speed)

    def delete(self):
        self.hideturtle()
        self.clear()
        del self


class Score(Turtle):
    """Creates a text score and places it at the given x, y coordinates. The class also contains an update method."""
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.teleport(x_pos, y_pos)
        self.count = 0
        self.pen({
            "pencolor": "gold",
            "pensize": 5,
            "outline": 1,
        })
        self.write(f"Score: {self.count}", align="center", font=('Oswald', 18, 'normal'))

    def update(self):
        self.clear()
        self.write(f"Score: {self.count}", align="center", font=('Oswald', 18, 'normal'))


class Lives(Turtle):
    """Creates a text of remaining lives and places it at the given x, y coordinates.
    The class also contains an update method."""
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.count = 3
        self.pen({
            "pencolor": "gold",
            "pensize": 5,
            "outline": 1,
        })
        self.teleport(x_pos, y_pos)
        self.write(f"Lives: {self.count}", align="center", font=('Oswald', 18, 'normal'))

    def update(self):
        self.clear()
        self.write(f"Lives: {self.count}", align="center", font=('Oswald', 18, 'normal'))


class Shield(Turtle):
    """Creates a shield that protects player ship and places it at x, y coordinates.
    The class also contains a shield deletion method."""
    def __init__(self, shape, x_cor, y_cor):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.teleport(x_cor, y_cor)
        self.name = "Shield"

    def delete(self):
        self.hideturtle()
        self.clear()
        del self
