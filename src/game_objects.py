from random import randint

class Objects:
    def __init__(self,settings,last_score):
        self.settings = settings
        self.last_score = last_score

        self.snake_positions = []
        self.make_snake()
        self.food_amount = self.calc_food()
        self.food_positions = []
        self.new_food()


    def calc_food(self):
        food_amount = 1
        if self.settings.food_spawning == 2:
            amount_raw = self.settings.max_food - self.last_score
            if amount_raw > 1:
                food_amount = int(amount_raw)
            # print("<DEBUG> Last score: ",self.last_score)
            # print("<DEBUG> Amount_raw: ",amount_raw)
            # print("<DEBUG> Food amount: ",food_amount)
            return food_amount
        elif self.settings.food_spawning == 1:
            return randint(min_food,max_food)
        else:
            return food_amount


    def make_snake(self):
        dir_coord = {                                # Directions available for snake in x-y coordinates
            0:[1,0],
            1:[0,1],
            2:[-1,0],
            3:[0,-1]}
        head_x = randint(3,self.settings.board_x - 3)                   # Place snake head a little away from walls
        head_y = randint(3,self.settings.board_y - 3)
        dir_int = randint(0,3)                                          # Decide where the snake is headed

        snake_length = 3
        if self.settings.init_snake_max > 3:                            # If snake has random initial length, decide length
            snake_length = randint(3,self.settings.init_snake_max)
        self.direction = dir_coord[dir_int]
        head_pos = (head_x,head_y)
        self.snake_positions.append(head_pos)

        for _ in range(snake_length - 1):                                 # Populate the snake body until final length is met
            body_pos = (
                        self.snake_positions[-1][0] - (self.direction[0]),
                        self.snake_positions[-1][1] - (self.direction[1]))
            self.snake_positions.append(body_pos)


    def new_food(self):
        if len(self.food_positions) >= self.food_amount:                # Check if food is already in place
            return
        while len(self.food_positions)<self.food_amount:                # Make new food until food amount is satisfied
            x_position = randint(1,self.settings.board_x-2)             # Food must spawn in unoccupied space.
            y_position = randint(1,self.settings.board_x-2)
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions and food_position not in self.food_positions:
                self.food_positions.append(food_position)