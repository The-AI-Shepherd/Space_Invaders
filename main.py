import datetime as dt
import turtle as t
from assets import Ship, Projectile, Score, Lives, Keeper, Shield
import random

WIDTH = 900
HEIGHT = 1000

# Paths to shape icons
player_icon = "./assets/player.gif"
alien_1 = "./assets/alien1.gif"
alien_2 = "./assets/alien2.gif"
alien_3 = "./assets/alien3.gif"
laser_projectile = "./assets/laser.gif"
laser_player = "./assets/laser_player.gif"
rocket_projectile = "./assets/rocket.gif"
shield_icon = "./assets/shield.gif"
list_of_icons = [player_icon, alien_1, alien_2, alien_3, laser_projectile, laser_player, rocket_projectile, shield_icon]

# Screen settings
screen = t.Screen()
screen.tracer(0, 0)
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.listen()
screen.title("Space Invaders (Python)")
width = screen.window_width()
height = screen.window_height()

# Game settings
alien_projectile_speed = 1
RESPAWN_TIMER = 3
PLAYER_INVINCIBILITY_DURATION = 3


# Function to create shield walls to protect the player ship
def create_shield_wall():
    index_x = 0
    for _ in range(4):
        shield_x = shield_x_cors[index_x]
        shield_y = -(height / 5.5)
        for _ in range(8):
            shield_x += 15
            for _ in range(6):
                shield_piece = Shield(shield_icon, shield_x, shield_y)
                shield_clusters.append(shield_piece)
                shield_y -= 10
            shield_y = -(height / 5.5)
        index_x += 1


# Function to create aliens organized in symmetrical lines
def create_aliens():
    iteration = 0
    position_adjustment_x = 0
    position_adjustment_y = 0
    alien_x = alien_start_x_cor + position_adjustment_x
    alien_y = alien_start_y_cor + position_adjustment_y
    for _ in range(5):
        # Select the shape of the alien ship based on their order from top to bottom
        if iteration < 1:
            shape = alien_1
            row = alien_ship_row_1
        elif 0 < iteration < 3:
            shape = alien_2
            row = alien_ship_row_2
        else:
            shape = alien_3
            row = alien_ship_row_3
        for _ in range(10):
            alien = Ship(shape, alien_x, alien_y, width, height)
            alien_ships.append(alien)
            row.append(alien)
            position_adjustment_x += 70
            alien_x = alien_start_x_cor + position_adjustment_x

        position_adjustment_y -= 70
        position_adjustment_x = 0
        alien_y = alien_start_y_cor + position_adjustment_y
        alien_x = alien_start_x_cor + position_adjustment_x
        iteration += 1


# Alien ship movement function
def move(ship_to_move, movement_direction, movement_speed):
    if not game_paused:
        if movement_direction == "right":
            ship_to_move.move_right(movement_speed)
        else:
            ship_to_move.move_left(movement_speed)


# Player ship movement
def player_move(player_ship_f, direction_f):
    if not game_paused:
        if direction_f == "Left":
            player_ship_f.move_left(20)
        else:
            player_ship_f.move_right(20)


# Function to govern player shooting frequency
def player_shoot(xcor, ycor):
    global player_projectile_on_screen, player_projectile, game_paused
    if game_paused:
        # Unpauses game start and launches the game on shoot button press
        pause()
    else:
        if player_projectile_on_screen:
            pass
        else:
            player_projectile = Projectile(rocket_projectile, xcor, ycor, 90)
            player_projectile_on_screen = True


# Function to govern player shooting frequency
def player_shoot_cheat(xcor, ycor):
    global player_projectile_on_screen, player_projectile_cheat, game_paused, cheat
    if game_paused:
        # Unpauses game start and launches the game on shoot button press
        pause()
    else:
        if player_projectile_on_screen:
            pass
        else:
            cheat = True
            player_projectile_cheat = Projectile(laser_player, xcor, ycor, 90)
            player_projectile_on_screen = True


# Function to detect collision between two turtle instances
def collision_detected(object_a, object_b, collision_distance, debug=False):
    distance = object_a.distance(object_b)
    if distance <= collision_distance:
        if debug:
            print(f"Collision detected between {object_a.name} (x, y:{object_a.pos()}) "
                  f"and {object_b.name} (x, y:{object_b.pos()}). The distance between them is {distance}.")
        return True
    else:
        if debug:
            print("Collision was not detected between {object_a.name} (x, y:{object_a.pos()}) "
                  f"and {object_b.name} (x, y:{object_b.pos()}). The distance between them is {distance}..")
        return False


# Function to run when player is hit by alien projectile
def player_hit(turtle):
    """When player is hit, it makes the player temporarily invincible"""
    global player_invincible
    player_invincible = True
    screen.ontimer(lambda: respawn(turtle), 3000)


# Respawn after player death
def respawn(turtle):
    """Makes the player reappear after player hit"""
    turtle.showturtle()
    turtle.teleport(player_position[0], player_position[1])
    invincibility_frame(turtle)


# Invincibility frame
def invincibility_frame(turtle):
    """Makes the player invincible for a specific amount of time"""
    for i in range(flash_count):
        screen.ontimer(lambda: flash_turtle(turtle), 500 * (i + 1))
    screen.ontimer(lambda: disable_invincibility(turtle), 500 * flash_count)


# Function to flash turtle, mostly used for invincibility frame
def flash_turtle(turtle):
    """Flashes turtle for as long as invincibility lasts"""
    if turtle.isvisible():
        turtle.hideturtle()
    else:
        turtle.showturtle()


# Disable invincibility
def disable_invincibility(turtle):
    """Disables invincibility"""
    global player_invincible
    player_invincible = False
    if not turtle.isvisible():
        turtle.showturtle()


# Function to make alien target player position
def alien_ships_move_forward(alien_ships_f: list, y_increment: int, time_between_moves_in_secs=5.0):
    """Makes the alien ships move forward every number of seconds indicated"""
    global time_to_move_aliens, start_time
    if not game_paused:
        if start_time + dt.timedelta(seconds=time_between_moves_in_secs) <= dt.datetime.now():
            for alien_ship in alien_ships_f:
                alien_ship.goto(alien_ship.xcor(), alien_ship.ycor() - y_increment)
                start_time = dt.datetime.now()
            print("Aliens move forward")


# Function to check if game is over by aliens closing distance with player ship
def game_over_check_1(alien_ships_f: list):
    """Ends the game if aliens reach player ship"""
    global game_is_on, game_over
    for alien_ship in alien_ships_f:
        if alien_ship.ycor() <= player_ship.ycor():
            # game_is_on = False
            game_over = True
            # keeper.write_text("Game Over", (0, 0))


def game_over_check_2():
    """Ends the game if player is out of lives"""
    global game_is_on, game_over
    if lives.count <= 0:
        # game_is_on = False
        game_over = True
        # keeper.write_text("Game Over", (0, 0))


def grant_score(destroyed_ship):
    """Gives score based on what variation of alien ship was destroyed"""
    if destroyed_ship in alien_ship_row_1:
        score.count += 30
    elif destroyed_ship in alien_ship_row_2:
        score.count += 20
    elif destroyed_ship in alien_ship_row_3:
        score.count += 10


# Function to pause the entire game
def pause(text="Game Over"):
    """Pauses the game on specific key press"""
    global game_paused, start_time
    if game_paused:
        if not game_over:
            keeper.clear()
            start_time = dt.datetime.now()  # Sets the start_time to when the game is unpaused
            game_paused = False
    else:
        keeper.write_text(text, (0, 0))
        game_paused = True


# Function that leads game restart once game is over and clears all turtle instances to try again
def clear_aliens_shields(alien_ships_f, alien_projectiles_f, shields):
    """Clears all lists containing alien turtles, projectiles, shields and deletes references"""
    for alien in alien_ships_f:
        alien.delete()
        del alien
    for projectile_f in alien_projectiles_f:
        projectile_f.delete()
        del projectile_f
    for shield_f in shields:
        shield_f.delete()
        del shield_f

    # Clear lists
    alien_ships_f.clear()
    alien_projectiles_f.clear()
    shields.clear()


def clear_player(player, player_projectile_f):
    """Deletes player ship and projectile"""
    # Delete player & projectile
    player.delete()
    del player
    player_projectile_f.delete()
    del player_projectile_f

    # resets stats & updates them
    lives.count = 3
    score.count = 0
    lives.update()
    score.update()


# Sets game restart variable to true to trigger changes that will restart the game
def restart():
    """Sets the restart_game variable to True to allow the loop to repopulate all game elements and start again"""
    global restart_game
    restart_game = True


def next_round(alien_ships_f, alien_projectiles_f, shields):
    """Recreates another wave of aliens and rebuilds shields"""
    global alien_start_y_cor
    clear_aliens_shields(alien_ships_f, alien_projectiles_f, shields)

    alien_start_y_cor = height/1.3

    create_aliens()
    create_shield_wall()


# Adds all required icons to be used as shapes
for icon in list_of_icons:
    screen.addshape(icon)

# Player ship
player_position = (0, -(height / 2) + (height / 7))
player_ship = Ship(player_icon, player_position[0], player_position[1], width, height, ship_type="Player")
player_invincible = False

# The Keeper keeps the game's backgrounds
keeper = Keeper(width, height)

# Score and lives counter
lives = Lives(-(width/2)+(width/15), -(height/2)+(height/40))
score = Score(0, (height/2)-(height/20))

# Shield clusters to protect the player ship
shield_clusters = []
shield_x_cors, shield_y_cors = ([-365, -165, 35, 235],
                                [-(height / 5.5), -(height / 5.5) - 10, -(height / 5.5) - 20, -(height / 5.5) - 30])

# Alien ships to shoot at the shield clusters and the player ship
alien_ships = []
alien_ship_row_1, alien_ship_row_2, alien_ship_row_3 = [], [], []
alien_start_x_cor, alien_start_y_cor = -300, 320

# Player controls
screen.onkeypress(lambda: player_move(player_ship, "Left"), "Left")
screen.onkeypress(lambda: player_move(player_ship, "Right"), "Right")
screen.onkeypress(lambda: player_shoot(player_ship.xcor(), player_ship.ycor()+30), "Up")
screen.onkeypress(lambda: player_shoot(player_ship.xcor(), player_ship.ycor()+30), "space")
# Cheat control to destroy all aliens with one shot
screen.onkeypress(lambda: player_shoot_cheat(player_ship.xcor(), player_ship.ycor()+30), "h")
screen.onkeypress(lambda: pause("PAUSED"), "p")
screen.onkeypress(restart, "Return")

# Game setup, creates shield wall and aliens
create_shield_wall()
create_aliens()

# Alien movement direction and start speed
direction = "right"
alien_ship_speed = 0.3

# Player projectile condition, only one projectile can be at a time
player_projectile_on_screen = False
player_projectile = Projectile(rocket_projectile, 2000, 0, 90)
player_projectile_cheat = Projectile(laser_player, 2000, 0, 90)

# Alien projectile condition, a max of 10 can be present on screen
enough_alien_projectiles = False
player_targeted = False
alien_projectiles = []
max_projectiles = 4
min_projectiles = 1
number_of_alien_projectiles = random.randint(min_projectiles, max_projectiles)

# Misc variables:
start_time = dt.datetime.now()
time_to_move_aliens = 5
time_to_respawn_decided = False
invincibility_time_decided = False
flash_count = PLAYER_INVINCIBILITY_DURATION*2

game_is_on = True
game_paused = False
game_over = False
restart_game = False
next_round_transition = False
cheat = False
new_aliens_move = False

# Game won't start until fire button is pressed
pause("Press UP or Space to start")
while game_is_on:
    screen.update()
    for ship in alien_ships[::-1]:
        # Alien ships move in tandem
        ship.seth(0)
        move(ship, direction, alien_ship_speed)
        if ship.at_left_border():
            direction = "right"
        elif ship.at_right_border():
            direction = "left"

        # Alien ships fire
        if len(alien_projectiles) > number_of_alien_projectiles:
            enough_alien_projectiles = True
        else:
            enough_alien_projectiles = False
            number_of_alien_projectiles = random.randint(min_projectiles, max_projectiles)
        if enough_alien_projectiles:
            pass
        else:
            if not game_paused:
                chance_of_fire = random.choice(["no fire", "no fire", "no fire", "fire"])
                # Shoots projectiles in random places
                if chance_of_fire == "fire":
                    alien_projectile = Projectile(laser_projectile, ship.xcor(), ship.ycor()-20, 270)
                    alien_projectiles.append(alien_projectile)
                # Shoots a projectile at the player
                if not player_targeted:
                    if player_ship.xcor() - 40 <= ship.xcor() <= player_ship.xcor() + 40:
                        alien_projectile_f = Projectile(laser_projectile, ship.xcor(), ship.ycor() - 20, 270)
                        alien_projectiles.append(alien_projectile_f)
                    player_targeted = True

        # Check collision between alien ships and player projectile
        if player_projectile_on_screen:
            if cheat:
                if player_projectile_cheat.ycor() >= alien_ships[::-1][0].ycor() - 55:
                    if collision_detected(player_projectile_cheat, ship, 60):
                        grant_score(ship)
                        score.update()
                        ship.delete()
                        del alien_ships[alien_ships.index(ship)]
            else:
                if player_projectile.ycor() >= alien_ships[::-1][0].ycor() - 55:
                    if collision_detected(player_projectile, ship, 30):
                        grant_score(ship)
                        player_projectile.delete()
                        ship.delete()
                        player_projectile_on_screen = False
                        score.update()
                        del alien_ships[alien_ships.index(ship)]

    # Make the ships move towards the player every determined number of seconds & check if they reach the player
    alien_ships_move_forward(alien_ships[::-1], 10, 20)
    game_over_check_1(alien_ships[::-1])

    # Lasers move towards player & check for collision between lasers and both player projectiles and player ship
    for projectile in alien_projectiles:
        # Checks for collision between player ship and alien projectiles
        if projectile.ycor() <= player_ship.ycor() + 50:
            if collision_detected(projectile, player_ship, 30) and not player_invincible:
                player_ship.hideturtle()
                projectile.delete()
                del alien_projectiles[alien_projectiles.index(projectile)]
                lives.count -= 1
                lives.update()
                game_over_check_2()
                player_hit(player_ship)

        # Checks for collision with player projectiles
        if player_projectile_on_screen:
            # Collision between alien projectiles and player projectiles
            if cheat:
                # Cheat player projectile to destroy all projectiles in its path
                if collision_detected(projectile, player_projectile_cheat, 30):
                    projectile.delete()
                    del alien_projectiles[alien_projectiles.index(projectile)]

            else:
                if collision_detected(projectile, player_projectile, 30):
                    player_projectile.delete()
                    projectile.delete()
                    player_projectile_on_screen = False
                    del alien_projectiles[alien_projectiles.index(projectile)]

        # Delete alien projectiles if they move off-screen
        if projectile.ycor() <= -height/2:
            projectile.delete()
            del alien_projectiles[alien_projectiles.index(projectile)]
            player_targeted = False
        else:
            if not game_paused:
                projectile.move(alien_projectile_speed)

        # Check for collision between alien & player projectiles and shields
        for shield in shield_clusters:
            if collision_detected(projectile, shield, 15):
                shield.delete()
                projectile.delete()
                del shield_clusters[shield_clusters.index(shield)]
                try:
                    del alien_projectiles[alien_projectiles.index(projectile)]
                except ValueError:
                    pass
            if player_projectile_on_screen:
                if collision_detected(shield, player_projectile, 15):
                    shield.delete()
                    player_projectile.delete()
                    player_projectile_on_screen = False
                    del shield_clusters[shield_clusters.index(shield)]

    # Check for the number of ships to increase speed the less alien ships there are
    if alien_ship_speed < 3 or new_aliens_move:
        alien_ship_speed = 20 / (len(alien_ships)+1)

    # Projectile speed increases to less alien ships there are
    if alien_projectile_speed < 4 or new_aliens_move:
        alien_projectile_speed = 50 / (len(alien_ships)+1)

    # Increase projectile count the less alien ships there are
    if max_projectiles < 15 or new_aliens_move:
        max_projectiles = round(300/(len(alien_ships)+1))
    if min_projectiles < 5 or new_aliens_move:
        max_projectiles = round(60/(len(alien_ships)+1))

    # Checks if player projectile is on the screen to keep it moving and to destroy it if it goes off-screen
    if player_projectile_on_screen and not game_paused:
        if cheat:
            if player_projectile_cheat.ycor() >= height/2:
                player_projectile_cheat.delete()
                player_projectile_on_screen = False
                cheat = False
            else:
                player_projectile_cheat.move(3)
        else:
            if player_projectile.ycor() >= height/2:
                player_projectile.delete()
                player_projectile_on_screen = False
            else:
                player_projectile.move(3)

    # game over check
    if game_over:
        pause("Game Over")
        keeper.goto(0, -(height/8))
        keeper.write("Press return to try again", align="center", font=('Oswald', 16, 'normal'))
        alien_start_y_cor = 320
        if restart_game:
            clear_aliens_shields(alien_ships, alien_projectiles, shield_clusters)
            clear_player(player_ship, player_projectile)
            restart_game = False
            game_over = False
            player_ship = Ship(player_icon, player_position[0], player_position[1], width, height, ship_type="Player")
            create_aliens()
            create_shield_wall()
            pause()

    # Check if all aliens are destroyed to start new round
    if not alien_ships:
        next_round_transition = True
        new_aliens_move = True

    if next_round_transition:
        player_projectile.delete()
        player_projectile_cheat.delete()
        next_round(alien_ships, alien_projectiles, shield_clusters)
        next_round_transition = False

    if new_aliens_move:
        alien_ships_move_forward(alien_ships, 5, 0.5)
        for new_alien in alien_ships[::-1]:
            if new_alien.ycor() <= 40:
                new_aliens_move = False


screen.mainloop()
