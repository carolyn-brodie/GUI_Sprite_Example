
import arcade
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5
CHARACTER_SCALING = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

LOREM_IPSUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. "
    "Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. "
    "Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, "
    "non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante "
    "pellentesque. Cras rutrum aliquam fermentum. Donec id mollis mi.\n"
    "\n"
    "Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit "
    "amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, "
    "sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus "
    "ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, "
    "finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed "
    "arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id "
    "scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem "
    "tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.\n"
)

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Test of Instruction ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Screen ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyWindow()
        game_view.setup()
        self.window.show_view(game_view)


##This inherits from arcade.Sprite class
class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]

    def update(self):
        if self.center_x < 0 or self.center_x > SCREEN_WIDTH:
            self.change_x *= -1
        super().update()


class MyWindow(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.text = ""
        self.player_list = arcade.SpriteList()
        self.player = PlayerCharacter()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 0.8
        self.player.change_x = 2

        self.player_list.append(self.player)


    def setup(self):
        self.manager = UIManager()


        self.manager.enable()
        ## Create Text Area
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=100,
                               y=200,
                               width=200,
                               height=300,
                               text=LOREM_IPSUM,
                               text_color=(0, 0, 0, 255))



        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

        ##Text input area
        self.input_area = UIInputText(x=340, y=200, width=200, height=50, text="")
        self.manager.add(
            UITexturePane(
                #UIInputText(x=340, y=200, width=200, height=50, text=""),
                self.input_area,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            ))

        ##Text on screen
        self.manager.add(
            UIInputText(x=340, y=110, width=200, height=50, text=self.text),
        )

        ##Buttons
        # Create a BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        reload_button = arcade.gui.UIFlatButton(text="Read Text", width=200)
        self.v_box.add(reload_button.with_space_around(bottom=20))

        reload_button.on_click = self.on_click_reload

        end_button = arcade.gui.UIFlatButton(text="Ending Button", width=200)
        self.v_box.add(end_button.with_space_around(bottom=20))

        end_button.on_click = self.on_click_end

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box)
        )

    def on_click_reload(self, event):
        print("My Start:", event)
        self.text = self.input_area.text
        self.clear()
        self.setup()


    def on_click_end(self, event):
        print("My Start:", event)
        end_view = EndingView()
        self.window.show_view(end_view)


    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):

        # Move the player
        self.player_list.update()
        # Update the players animation
        self.player_list.update_animation()


class EndingView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("End of Game ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
       arcade.exit()


# window = MyWindow()
# arcade.run()
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "GUI")
instruction_view = InstructionView()
window.show_view(instruction_view)
arcade.run()