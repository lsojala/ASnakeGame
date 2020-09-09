"""
General setting and parameters
"""

class Settings:
    
    #Movement
    move_increment = 20                         # Defines game resolution, snakes moves this many pixels per tick
    moves_per_second = 15  
    game_speed = 1000 // moves_per_second       # Length of game tick, in ms

    # Game window size
    win_width = 640
    win_height=670

    # Play field size in move_increments
    board_x = 32
    board_y = 32


    # Additional options for modified start and game play, mainly used for AI training
    new_game_delay = 6                      # Automatically start a new game after this many secods

    food_spawning = 0                       # Defines the number of food
                                            # 0 - Classic, there always exists one food
                                            # 1 - Random, for each game a random number is selected between min_food and max_food
                                            # 2 - Decreasing, the score gained in previous games subtracts the available food in the next game

    min_food = 1
    max_food = 10

    init_snake_max = 3                      # Starting snake length is randomly chosen between 3 and init_snake_max.
                                            # Set to 3 or below to have starting snake always the length of 3 

    resuffling_food_intrv = 0               # Sets interval after which all current food is destroyd and recreated in random locations
                                            # Set 0 to disable resuffling

    max_moves = 0                           # Game ends after this many ticks have passed
                                            # Set 0 to disable for classic infinite play.

