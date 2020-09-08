"""
The Snake Game
Main game engine
"""
print("Loading GUI...")
import tkinter as tk

import game_settings
import game_assets
import game_objects

settings = game_settings.Settings()
assets = game_assets.Assets()

NEW_GAME = True                                 # After game has finished continue to new game

task1 = None                                    # Placeholder for tkinter tasks, e.g. calling funtions.
task2 = None

last_score = 0                                  # Markdown place for previous score

dir_dict = {                                    # Keyword - coordinate translation for directions
    "Right":[1,0],
    "Down":[0,1],
    "Left":[-1,0],
    "Up":[0,-1]}

dir_words = ["Right","Down","Left","Up"]        # Int - keyword translation for directions


class Game(tk.Canvas):                          # Main class for the game itself
    def __init__(self,assets, settings,last_score):
        super().__init__(width = settings.win_width,height=settings.win_height,background="black",highlightthickness=0)

        global task1

        self.assets = assets
        self.assets.load_assets()

        self.settings = settings

        self.objects = game_objects.Objects(settings, last_score)

        self.score = 0
        self.timer = self.settings.new_game_delay
        self.move_counter = 0

        self.create_objects()                                           # Draw game objects

        self.bind_all("<Key>",self.player_action)                       # Record player input

        task1 = root.after(self.settings.game_speed,self.perform_actions)             # Advance the first tick



    def render(self,position):                                # Help funtion to swich between object increments and pixel
        """Takes position tuple, gives rendering x-coordinate and y-coordeinate. """
        draw_x = position[0]*self.settings.move_increment
        draw_y = position[1]*self.settings.move_increment
        return draw_x, draw_y


    def create_objects(self):
        for position in self.objects.snake_positions:
            self.create_image(self.render(position),image=self.assets.snake,tag="snake")
        for position in self.objects.food_positions:
            self.create_image(self.render(position),image=self.assets.food,tag="food")

        self.create_text(45,648,text= "Score: {}".format(self.score),tag="score",fill="#fff",font=("Comic Sans MS Bold",14))
        
        self.create_rectangle(7,7,(self.settings.board_x - 1)*self.settings.move_increment-7, (self.settings.board_y - 1)*self.settings.move_increment-7,outline="#525d69")


    def move_snake(self):
        head_x_position, head_y_position = self.objects.snake_positions[0]
        new_head_position = (
            head_x_position + (self.objects.direction[0]),
            head_y_position + (self.objects.direction[1]))

        self.objects.snake_positions = [new_head_position] + self.objects.snake_positions[:-1]

        for n, segment in enumerate(self.find_withtag("snake")):
            draw_positions = (self.render(self.objects.snake_positions[n]))
            self.coords(segment,draw_positions)
        self.move_counter += 1


    def check_collisions(self):
        head_x_position, head_y_position = self.objects.snake_positions[0]
        if (
            head_x_position in (0, self.settings.board_x - 1) or 
            head_y_position in(0, self.settings.board_y - 1) or 
            (head_x_position, head_y_position) in self.objects.snake_positions[1:]):
            return True
        else:
            return False


    def check_food(self):
        if self.objects.snake_positions[0] in self.objects.food_positions:
            self.score += 1
            self.objects.snake_positions.append(self.objects.snake_positions[-1])
            self.create_image(self.render(self.objects.snake_positions[-1]),image=self.assets.snake,tag="snake")

            self.objects.food_positions.remove(self.objects.snake_positions[0])
            self.delete("food")
            self.objects.new_food()
            for position in self.objects.food_positions:
                self.create_image(self.render(position),image=self.assets.food,tag="food")

            score_img = self.find_withtag("score")
            self.itemconfigure(score_img,text="Score: {}".format(self.score),tag="score")


    def resuffle_food(self):
        # print("<DEBUG> New Food Locations!")
        self.objects.food_positions = []
        self.delete("food")
        self.objects.new_food()
        for position in self.objects.food_positions:
                self.create_image(self.render(position),image=self.assets.food,tag="food")


    def perform_actions(self):                                              # Move the snake, check for game events, and proceed to next game tick
        global task1
        global task2

        self.move_snake()

        if self.check_collisions() == True:
            task1 = root.after(1,self.end_game)
            return

        self.check_food()

        if self.move_counter > self.settings.max_moves and self.settings.max_moves > 0:           # End game if maximum moves reached
            task1 = root.after(1,self.end_game)
            return

        if self.settings.resuffling_food_intrv > 0 and self.move_counter >= 1 and self.move_counter % self.settings.resuffling_food_intrv == 0 :     # If enough turns have passed resuffle food
            self.resuffle_food()

        # Proceed to next game tick
        task1 = root.after(self.settings.game_speed,self.perform_actions)


    def change_direction(self,new_direction):                               # If new direction is not opposite to old direct, change direction
        sum_direction = []
        for i in range(2):
            sum_direction.append(new_direction[i]+self.objects.direction[i])
        # print("<DEBUG> New direction: ".,new_direction)
        # print("<DEBUG> Old direction: ",self.objects.direction)
        # print("<DEBUG> Direction sum: ", sum_direction)
        if not sum_direction == [0,0]:
            # print("<DEBUG> Changing direction!")
            self.objects.direction = new_direction


    def player_action(self,e):                                              # If player pressed arrow keys, try to change direction
        try:
            new_direction= dir_dict[e.keysym]
            self.change_direction(new_direction)
        except KeyError:
            # print("<DEBUG> Unknown key pressed!")
            return
        

    def count_down(self):
        global task2
        self.timer -= 1
        timer_text = self.find_withtag("timer")
        self.itemconfigure(timer_text,text="New round begins in {} s".format(self.timer),tag="timer")
        if self.timer <= 0:
            task2 = root.after(1,go_new)
        task2 = root.after(1000,self.count_down)


    def end_game(self):
        global last_score

        last_score = self.score

        self.delete("all")
        self.create_text(
            300,
            150,
            text="Game over, man!\nFinal score {}".format(self.score),
            fill="#fff",
            font=("TkDefaultFont",24)
            )

        self.new_button = tk.Button(self,text="New Game",bg="gray",fg="white",command = go_new)
        self.new_button.place(x=150,y=465,height=30,width=80)
        self.quit_button = tk.Button(self,text="Quit Game",bg="gray",fg="white",command = go_home)
        self.quit_button.place(x=450,y=465,height=30,width=80)

        self.create_text(
            300,
            250,
            text="New round begins in {} s".format(self.timer),
            tag ="timer",
            fill="#fff",
            font=("TkDefaultFont",24)
            )

        task2 = root.after(1,self.count_down)


def game_loop():
    while NEW_GAME == True:
        global root
        global board

        root = tk.Tk()
        root.configure(background='black')
        root.title("A Snake Game")
        root.resizable(False,False)

        board = Game(assets,settings,last_score)
        board.pack(padx=10,pady=10)

        root.mainloop()


def go_new():
    global NEW_GAME
    global task1
    global task2
    if task1 is not None:
        root.after_cancel(task1)
        task1 = None
    if task2 is not None:
        root.after_cancel(task2)
        task2 = None
    root.destroy()


def go_home():
    global NEW_GAME
    global task1
    global task2
    NEW_GAME = False
    if task1 is not None:
        root.after_cancel(task1)
        task1 = None
    if task2 is not None:
        root.after_cancel(task2)
        task2 = None
    root.destroy()


game_loop()
print("Game Ending")