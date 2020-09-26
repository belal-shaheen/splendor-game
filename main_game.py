"""
 *****************************************************************************
   FILE:splendor

   AUTHOR: BELAL SHAHEEN

   ASSIGNMENT:Final Project: Splendor

   DATE:11/13/2019

   DESCRIPTION: Code that successfully implements an entire game of Splendor.

 *****************************************************************************
"""

from cs110graphics import *

gem_pos = [(640,200),(640,270),(640,340),(640,410),(640,480)]

level1_development_cards_pos = {(200,220):False,(315,220):False,
(430,220):False,(545,220):False}

level2_development_cards_pos = {(200,370):False,(315,370):False,
(430,370):False,(545,370):False}

level3_development_cards_pos = {(200,520):False,(315,520):False,
(430,520):False,(545,520):False}

nobles_pos_one = {(200,670):False,(315,670):False,(430,670):False}

nobles_pos_two = {(200,670):False,(315,670):False,(430,670):False,
(545,670):False}

nobles_pos_three = {(200,670):False,(315,670):False,(430,670):False,
(545,670):False,(660,670):False}

reserved_cards = [(745,220),(745,370),(745,520)]

from cardimporter import cardimporter_yuh
from player_input import take_input
import random


def main(window):
    """Sets the board and gets input from the player"""

    player_input = take_input()

    window.set_background('gray')
    window.set_width(1200)
    window.set_height(1200)

    board = Board(window,player_input)


class Win_Message:
    def __init__(self, window, player_name, prestige):
        """Creates a win message with the name of the player that won"""

        self._window = window
        self._player_name = player_name
        self._player_prestige = prestige

        background = Square(self._window,1200,(600,600))
        background.set_depth(-200)
        self._window.add(background)

        winner = Text(self._window,\
        str(player_name) + " wins with " + str(self._player_prestige) \
        + " points.",50,(600,500))
        winner.set_depth(-300)
        self._window.add(winner)

class Player_Display:
    def __init__(self, window):
        """Creates a display for the player where their gems and card gems
            will be displayed"""

        self._window = window

        self._window.add(Rectangle(self._window,35,70,(400,100)))
        self._window.add(Square(self._window,70,(420,100)))

        self._window.add(Rectangle(self._window,35,70,(490,100)))
        self._window.add(Square(self._window,70,(510,100)))

        self._window.add(Rectangle(self._window,35,70,(580,100)))
        self._window.add(Square(self._window,70,(600,100)))

        self._window.add(Rectangle(self._window,35,70,(670,100)))
        self._window.add(Square(self._window,70,(690,100)))

        self._window.add(Rectangle(self._window,35,70,(760,100)))
        self._window.add(Square(self._window,70,(780,100)))

        self._window.add(Rectangle(self._window,35,70,(850,100)))
        self._window.add(Square(self._window,70,(870,100)))

        self._texts = []

    def set_values(self,gems,card_gems):
        """Used to set the values of the player display. Sets colors that
            correspond with the gem type"""

        player_card_r_gems = int(card_gems[0])
        self._texts.append(Text(self._window,str(player_card_r_gems)
        ,33,(435,100)))
        self._texts[0].set_color('red')

        player_card_d_gems = int(card_gems[1])
        self._texts.append(Text(self._window,str(player_card_d_gems)
        ,33,(525,100)))

        player_card_s_gems = int(card_gems[2])
        self._texts.append(Text(self._window,str(player_card_s_gems)
        ,33,(615,100)))
        self._texts[2].set_color('blue')

        player_card_o_gems = int(card_gems[3])
        self._texts.append(Text(self._window,str(player_card_o_gems)
        ,33,(705,100)))
        self._texts[3].set_color('brown')

        player_card_e_gems = int(card_gems[4])
        self._texts.append(Text(self._window,str(player_card_e_gems)
        ,33,(795,100)))
        self._texts[4].set_color('green')

        r_gems = int(gems[0])
        self._texts.append(Text(self._window,str(r_gems),33,(400,100)))
        self._texts[5].set_color('red')

        d_gems = int(gems[1])
        self._texts.append(Text(self._window,str(d_gems),33,(490,100)))

        s_gems = int(gems[2])
        self._texts.append(Text(self._window,str(s_gems),33,(580,100)))
        self._texts[7].set_color('blue')

        o_gems = int(gems[3])
        self._texts.append(Text(self._window,str(o_gems),33,(670,100)))
        self._texts[8].set_color('brown')

        e_gems = int(gems[4])
        self._texts.append(Text(self._window,str(e_gems),33,(760,100)))
        self._texts[9].set_color('green')

        g_gems = int(gems[5])
        self._texts.append(Text(self._window,str(g_gems),33,(850,100)))
        self._texts[10].set_color('gold')

        for text in self._texts:
            text.set_depth(-100)

    def draw(self):
        """Draws the text and adds it to the window"""

        for text in self._texts:
            self._window.add(text)

    def undraw(self):
        """Delets the text. This is used to update the text for every player"""

        for text in self._texts:
            self._window.remove(text)
            self._texts = []
            self._window.refresh()


class Board:
    def __init__(self,window,player_input):
        """Set the board up by using the player input"""

        self._mode = player_input[0]
        self._players = len(player_input[1])
        self._game_ended = False
        self._window = window

        self._player_list = []
        background = Background(window)
        self._display = Player_Display(window)

        #creates a list of the players
        for player in player_input[1]:
            self._player_list.append(Player(player))

        #selects a random player to begin
        self._player_turn = random.randint(1,len(self._player_list))
        self._player = self._player_list[self._player_turn-1]
        self._player_area = Player_Area(window,self,self._player)

        #sets a default list of gems and development cards
        self._init_gems = [0,0,0,0,0,0]
        self._init_development_cards = []

        if self._mode == '2':
            self._init_gems = [4,4,4,4,4,5]
        elif self._mode == '3':
            self._init_gems = [5,5,5,5,5,5]
        else:
            self._init_gems = [7,7,7,7,7,5]

        self._gem_numbers = self._init_gems

        #updates the player display for the current player with their name
        #and prestige points
        self._player_display = Text(window,self._player.get_name(),15,(150,50))
        self._window.add(self._player_display)

        self._pp_point = Text(window,'Prestige Points:' +
        str(self._player.print_prestige()),15,(200,100))
        self._window.add(self._pp_point)

        #creates the class Gems, Development Cards, and Nobles
        self._gems = Gems(self._window,self._player_area,self._gem_numbers)
        self._development_cards = DevelopmentCards(window,self._player_area,
        self._player)
        self._nobles_cards = Nobles(window,self._player_area, self._player,
        self._mode)

    def switch_turns_cards(self):
        """Function that switches the turn whenever a card is bought"""

        self._player_area.change_player(self._player)
        card_placed = self._player_area.return_card_placed()

        #if the card being bought was reserved, it removes it from the list
        #of reserved cards the player has
        if card_placed.reservation() == True:
            self._player.remove_reserved_card(card_placed)

        #updates the players PP, card gems, and deletes the card from the screen
        self.add_card_to_player()
        self.draw_development_card()
        self.remove_player_gems_purchase()
        self.add_pp_to_player()
        self.add_cards_gems_to_player()
        self.delete_cards()
        self._player.undraw_reserved_cards()

        #updates the player display
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

        #if the player has enough card gems, it checks if there's any valid
        #nobles and get it
        if self.check_nobles():
            for noble in self._nobles_cards.return_drawn_nobles():
                if noble.get_legit() == True:
                    self._player.add_pp(noble.get_pp())
                    noble.delete_card()
                    self._nobles_cards.remove_drawn_nobles(noble)

        #ends the game with a print statement if the player is over 15
        if self._player.print_prestige() >= 15:
            win = Win_Message(self._window, self._player.get_name(),
            self._player.print_prestige())

        #switches the players turn by updated the screen
        self._player_turn = self._player_turn % self._players + 1
        self._player = self._player_list[self._player_turn-1]

        self._window.remove(self._player_display)
        self._window.remove(self._pp_point)
        self.update_player_stats(self._player)
        self.update_player_text_pp()
        self._display.undraw()
        self._player_area.change_player(self._player)
        self._player.draw_reserved_cards()
        self._player_area.remove_cards_from_area()

        #updates the player display
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

    def switch_turns_reserve_cards(self):
        """Function that reserves a card for a player"""

        #adds the card placed to the player
        card_placed = self._player_area.return_card_placed()
        card_placed.reserve()
        self._player.add_reserved_card(card_placed)

        self._player_area.change_player(self._player)

        self.add_card_to_player()
        self.draw_development_card()
        self.add_gems_to_player()
        self._player.undraw_reserved_cards()

        #updates the player screen
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

        #switches the turn
        self._player_turn = self._player_turn % self._players + 1
        self._player = self._player_list[self._player_turn-1]

        self._window.remove(self._player_display)
        self._window.remove(self._pp_point)
        self.update_player_stats(self._player)
        self.update_player_text_pp()
        self._display.undraw()
        self._player_area.change_player(self._player)
        self._player.draw_reserved_cards()

        self.remove_gems_from_area()
        self._player_area.remove_cards_from_area()

        #updates the player display
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

    def switch_turns_gems(self):
        """Function that allows the player to purchase gems"""

        self._player_area.change_player(self._player)
        self.add_gems_to_player()
        self._player.undraw_reserved_cards()

        #updates the current display for the current player
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

        #changes the player
        self._player_turn = self._player_turn % self._players + 1
        self._player = self._player_list[self._player_turn-1]

        self._window.remove(self._player_display)
        self._window.remove(self._pp_point)
        self.update_player_stats(self._player)
        self.update_player_text_pp()
        self._display.undraw()
        self._player_area.change_player(self._player)
        self._player.draw_reserved_cards()

        self.remove_gems_from_area()
        self.set_player_gems_to_zero()

        #updates the display for the changed player
        self._display.set_values(self._player.return_player_gems(),
        self._player.return_player_card_gems())
        self._display.draw()

    def check_nobles(self):
        """Function that checks to see if there are any Nobles the player
            can have"""

        player_card_gems = self._player.return_player_card_gems()
        self._player_card_r_gems = int(player_card_gems[0])
        self._player_card_d_gems = int(player_card_gems[1])
        self._player_card_s_gems = int(player_card_gems[2])
        self._player_card_o_gems = int(player_card_gems[3])
        self._player_card_e_gems = int(player_card_gems[4])
        nobles = self._nobles_cards.return_drawn_nobles()

        for noble in nobles:
            noble_r =  noble.r_value()
            noble_d = noble.d_value()
            noble_s = noble.s_value()
            noble_o = noble.o_value()
            noble_e = noble.e_value()

            #compares the value of the Noble to the player card gems and gets it
            if int(noble_r) > self._player_card_r_gems:
                return False
            elif int(noble_d) > self._player_card_d_gems:
                return False
            elif int(noble_s) > self._player_card_s_gems:
                return False
            elif int(noble_o) > self._player_card_o_gems:
                return False
            elif int(noble_e) > self._player_card_e_gems:
                return False
            else:
                noble.set_legit()
                return True

    def remove_player_gems_purchase(self):
        """Function that removes gems from a player whenever a purchase is
            made by comparing the value of the card to the players card gems,
            gems and gold gems"""

        player_gems = self._player.return_player_gems()
        player_card_gems = self._player.return_player_card_gems()
        self._player_card_r_gems = int(player_card_gems[0])
        self._player_card_d_gems = int(player_card_gems[1])
        self._player_card_s_gems = int(player_card_gems[2])
        self._player_card_o_gems = int(player_card_gems[3])
        self._player_card_e_gems = int(player_card_gems[4])

        self._r_gems = int(player_gems[0])
        self._d_gems = int(player_gems[1])
        self._s_gems = int(player_gems[2])
        self._o_gems = int(player_gems[3])
        self._e_gems = int(player_gems[4])
        self._g_gems = int(player_gems[5])

        card_placed = self._player_area.return_card_placed()
        gold_gem_used = False

        #if statements that look at each card value and whether the player needs
        #gold gems or not to buy the card
        if (int(card_placed.r_value()) <=
        self._player_card_r_gems + self._r_gems):

            leftover_r =  int(card_placed.r_value()) - self._player_card_r_gems

            if leftover_r > 0:
                self._player.remove_r_gems_purchase(leftover_r)
                self._gems.return_r_gems(leftover_r)

        elif ((int(card_placed.r_value()) <= (self._player_card_r_gems +
        self._r_gems + self._g_gems )) and not gold_gem_used):

            leftover_r  = int(card_placed.r_value()) - self._player_card_r_gems
            leftover_gold = leftover_r - self._r_gems

            self._player.remove_r_gems_purchase(leftover_r - leftover_gold)
            self._player.remove_g_gems_purchase(leftover_gold)
            self._gems.return_r_gems(leftover_r - leftover_gold)
            self._gems.return_g_gems(leftover_gold)

            if self._g_gems - leftover_gold > 0:
                gold_gem_used = False
            else:
                gold_gem_used = True

        if (int(card_placed.d_value()) <=
        self._player_card_d_gems + self._d_gems):

            leftover_d =  int(card_placed.d_value()) - self._player_card_d_gems

            if leftover_d > 0:
                self._player.remove_d_gems_purchase(leftover_d)
                self._gems.return_d_gems(leftover_d)

        elif ((int(card_placed.d_value()) <= (self._player_card_d_gems +
        self._d_gems + self._d_gems )) and not gold_gem_used):

            leftover_d =  int(card_placed.d_value()) - self._player_card_d_gems
            leftover_gold = leftover_d - self._d_gems

            self._player.remove_d_gems_purchase(leftover_d - leftover_gold)
            self._player.remove_g_gems_purchase(leftover_gold)
            self._gems.return_d_gems(leftover_d - leftover_gold)
            self._gems.return_g_gems(leftover_gold)

            if self._g_gems - leftover_gold > 0:
                gold_gem_used = False
            else:
                gold_gem_used = True

        if (int(card_placed.s_value()) <=
        self._player_card_s_gems + self._s_gems):

            leftover_s =  int(card_placed.s_value()) - self._player_card_s_gems

            if leftover_s > 0:
                self._player.remove_s_gems_purchase(leftover_s)
                self._gems.return_s_gems(leftover_s)

        elif ((int(card_placed.s_value()) <= (self._player_card_s_gems + \
         self._s_gems + self._s_gems )) and not gold_gem_used):

            leftover_s =  (int(card_placed.s_value()) - \
            self._player_card_s_gems)
            leftover_gold = leftover_s - self._s_gems

            self._player.remove_s_gems_purchase(leftover_s - leftover_gold)
            self._player.remove_g_gems_purchase(leftover_gold)
            self._gems.return_s_gems(leftover_s - leftover_gold)
            self._gems.return_g_gems(leftover_gold)

            if self._g_gems - leftover_gold > 0:
                gold_gem_used = False
            else:
                gold_gem_used = True

        if (int(card_placed.o_value()) <=
        self._player_card_o_gems + self._o_gems):


            leftover_o =  int(card_placed.o_value()) - self._player_card_o_gems

            if leftover_o > 0:
                self._player.remove_o_gems_purchase(leftover_o)
                self._gems.return_o_gems(leftover_o)

        elif ((int(card_placed.o_value()) <= (self._player_card_o_gems + \
        self._o_gems + self._o_gems )) and not gold_gem_used):

            leftover_o =  int(card_placed.o_value()) - \
            self._player_card_o_gems
            leftover_gold = leftover_o - self._o_gems

            self._player.remove_o_gems_purchase(leftover_d - leftover_gold)
            self._player.remove_g_gems_purchase(leftover_gold)
            self._gems.return_o_gems(leftover_d - leftover_gold)
            self._gems.return_g_gems(leftover_gold)

            if self._g_gems - leftover_gold > 0:
                gold_gem_used = False
            else:
                gold_gem_used = True

        if (int(card_placed.e_value()) <=
        self._player_card_e_gems + self._e_gems):

            leftover_e =  int(card_placed.e_value()) - self._player_card_e_gems

            if leftover_e > 0:
                self._player.remove_e_gems_purchase(leftover_e)
                self._gems.return_e_gems(leftover_e)

        elif ((int(card_placed.e_value()) <= (self._player_card_e_gems + \
        self._e_gems + self._e_gems )) and not gold_gem_used):

            leftover_e =  int(card_placed.e_value()) - \
            self._player_card_e_gems
            leftover_gold = leftover_e - self._e_gems

            self._player.remove_e_gems_purchase(leftover_e - leftover_gold)
            self._player.remove_g_gems_purchase(leftover_gold)
            self._gems.return_e_gems(leftover_e - leftover_gold)
            self._gems.return_g_gems(leftover_gold)

            if self._g_gems - leftover_gold > 0:
                gold_gem_used = False
            else:
                gold_gem_used = True

    def add_pp_to_player(self):
        """Adds prestige points to the player"""

        development_cards = self._player.return_development_cards()
        development_card = development_cards[-1]
        prestige_points = development_card.get_pp()
        self._player.add_pp(prestige_points)

    def draw_development_card(self):
        """Draws a development card in the place of the old development card"""

        cards = self._player.return_development_cards()

        if cards[-1].card_type() == 1:
            level_1_cards = self._development_cards.return_level_1_card()

            chosen_card = level_1_cards.pop(random.randint(0,
            len(level_1_cards)-1))

            card_position = cards[-1].return_position()
            chosen_card.change_position(card_position)
            chosen_card.draw()

        elif cards[-1].card_type() == 2:
            level_2_cards = self._development_cards.return_level_2_card()

            chosen_card = level_2_cards.pop(random.randint(0,
            len(level_2_cards)-1))

            card_position = cards[-1].return_position()
            chosen_card.change_position(card_position)
            chosen_card.draw()

        elif cards[-1].card_type() == 3:
            level_3_cards = self._development_cards.return_level_3_card()

            chosen_card = level_3_cards.pop(random.randint(0,
            len(level_3_cards)-1))

            card_position = cards[-1].return_position()
            chosen_card.change_position(card_position)
            chosen_card.draw()

    def delete_cards(self):
        """Deletes a development card once it is purchased"""

        development_cards = self._player.return_development_cards()
        development_card = development_cards[-1]
        development_card.delete_card()

    def add_cards_gems_to_player(self):
        """Adds card gems to the player by looking at the card they purchased"""

        development_cards = self._player.return_development_cards()
        development_card = development_cards[-1]
        gem_value = development_card.gem_returned()

        if gem_value == 'r':
            self._player.add_r(1)
        if gem_value == 'd':
            self._player.add_d(1)
        if gem_value == 's':
            self._player.add_s(1)
        if gem_value == 'o':
            self._player.add_o(1)
        if gem_value == 'e':
            self._player.add_e(1)

    def set_player_gems_to_zero(self):
        """resets the gems bought for the next player"""

        self._gems.reset_gems()

    def add_gems_to_player(self):
        """Used to adds Gems placed by the player to the player"""

        self._player.add_gems(self._gems.return_player_gems())
        self._gems.reset_gems()

    def add_card_to_player(self):
        """adds development cards to the player"""

        self._player.add_development_card(
        self._player_area.return_card_placed())

    def remove_gems_from_player(self):
        """Removes gems from the player. Used whenever a player purchases a
            card"""

        self._player.remove_gems(self._gems.return_player_gems())

    def remove_gems_from_area(self):
        """Clears the player area of gems and cards"""
        self._player_area.clear_area()

    def update_player_stats(self,player):
        """updares the name of the player when the turn is switched"""

        self._player_display = Text(self._window,
        self._player.get_name(),15,(150,50))

        self._window.add(self._player_display)

    def update_player_text_pp(self):
        """Updates the player's prestige points"""

        self._pp_point = Text(self._window,'Prestige Points:' +
        str(self._player.print_prestige()),15,(200,100))
        self._window.add(self._pp_point)


class Player:
    def __init__(self,name):
        """Initializes a Player"""

        self._prestige_points = 0
        self._name = name

        self._player_gems = [0,0,0,0,0,0]
        self._card_gems = [0,0,0,0,0,0]

        self._max_gems = 10

        self._max_reserve_cards = 3

        self._development_cards = []
        self._noble_tiles = []
        self._reserved_cards = []

    def add_pp(self, value):
        """used the add PP to a player"""

        self._prestige_points += int(value)

    def add_r(self,value):
        """used the add r card gems to a player"""

        self._card_gems[0] += int(value)

    def add_d(self,value):
        """used the add d card gems to a player"""

        self._card_gems[1] += int(value)

    def add_s(self,value):
        """used the add s card gems to a player"""

        self._card_gems[2] += int(value)

    def add_o(self,value):
        """used the add o card gems to a player"""

        self._card_gems[3] += int(value)

    def add_e(self,value):
        """used the add e card gems to a player"""

        self._card_gems[4] += int(value)

    def add_reserved_card(self,card):
        """Function that adds a reserved card to the player"""
        if len(self._reserved_cards) <= 3:
            self._reserved_cards.append(card)

    def return_reserve(self):
        """Function that returns the reserved cards of the player"""

        return self._reserved_cards

    def draw_reserved_cards(self):
        """Function that draws the reserved cards of the player"""

        for index,card in enumerate(self._reserved_cards):
            card.set_location(reserved_cards[index])
            card.draw2()

    def remove_reserved_card(self,card):
        """Function that removes reserved cards from the player"""

        self._reserved_cards.remove(card)

    def undraw_reserved_cards(self):
        """Function that undraws the reserved cards"""

        for card in self._reserved_cards:
            card.delete_card()

    def remove_r_gems_purchase(self,value):
        """Function that removes r gems"""

        self._player_gems[0] -= int(value)

    def remove_d_gems_purchase(self,value):
        """Function that removes d gems"""

        self._player_gems[1] -= int(value)

    def remove_s_gems_purchase(self,value):
        """Function that removes s gems"""

        self._player_gems[2] -= int(value)

    def remove_o_gems_purchase(self, value):
        """Function that removes o gems"""

        self._player_gems[3] -= int(value)

    def remove_e_gems_purchase(self, value):
        """Function that removes e gems"""

        self._player_gems[4] -= int(value)

    def remove_g_gems_purchase(self, value):
        """Function that removes d gems"""

        self._player_gems[5] -= int(value)

    def add_gems(self,gem_passed):
        """Function that adds multiple gems to the player"""

        for gem in range(len(gem_passed)):
            self._player_gems[gem] += gem_passed[gem]

    def remove_gems(self,gem_passed):
        """Function that removed multiple gems to the player"""

        for gem in range(len(gem_passed)):
            self._player_gems[gem] -= gem_passed[gem]

    def return_player_gems(self):
        """Function that returns the players gems"""

        return self._player_gems

    def return_player_card_gems(self):
        """Function that returns the players card gems"""

        return self._card_gems

    def print_prestige(self):
        """Function that returns the players PP"""

        return self._prestige_points

    def add_development_card(self,card):
        """Function that adds development cards to the players"""

        self._development_cards.append(card)

    def return_development_cards(self):
        """Function that returns the development cards of the player"""
        return self._development_cards

    def get_name(self):
        """Gets the name of the player"""

        return self._name


class Nobles():
    def __init__(self,window,player_area,player,mode):
        """Initializes Nobles"""

        self._window = window
        self._player_area = player_area
        self._player = player

        self._nobles_images = cardimporter_yuh(r'Nobles')
        self._nobles = []
        self._drawn_nobles = []
        self._mode = int(mode)

        self.initialize_cards()

    def initialize_cards(self):
        """Creates each individual noble card"""

        for filename in self._nobles_images:
            pp = self._nobles_images[filename][0]
            gem = self._nobles_images[filename][1]
            r = self._nobles_images[filename][2]
            d = self._nobles_images[filename][3]
            s = self._nobles_images[filename][4]
            o = self._nobles_images[filename][5]
            e = self._nobles_images[filename][6]

            card = Noble(self._window,'Nobles/' + filename,1,
            (0,0),pp,gem,r,d,s,o,e, self._player_area, self._player, self)
            self._nobles.append(card)

        #creates 3 nobles if the mode is 2
        if self._mode == 2:
            for posx,posy in nobles_pos_one:
                nobles_pos_one[(posx,posy)] = True

                chosen_card = self._nobles.pop(random.randint(0,
                len(self._nobles)-1))

                self._drawn_nobles.append(chosen_card)
                chosen_card.change_position((posx,posy))
                chosen_card.draw()

        #creates 4 nobles if the mode is 3
        if self._mode == 3:
            for posx,posy in nobles_pos_two:
                nobles_pos_two[(posx,posy)] = True

                chosen_card = self._nobles.pop(random.randint(0,
                len(self._nobles)-1))

                self._drawn_nobles.append(chosen_card)
                chosen_card.change_position((posx,posy))
                chosen_card.draw()

        #creates 5 nobles if the mode is 4
        if self._mode == 4:
            for posx,posy in nobles_pos_three:
                nobles_pos_three[(posx,posy)] = True

                chosen_card = self._nobles.pop(random.randint(0,
                len(self._nobles)-1))

                self._drawn_nobles.append(chosen_card)
                chosen_card.change_position((posx,posy))
                chosen_card.draw()

    def return_nobles(self):
        """Returns the nobles in the list"""

        return self._nobles

    def return_drawn_nobles(self):
        """Returns the nobles that were chosen and drawn by the pop method"""

        return self._drawn_nobles

    def remove_drawn_nobles(self,card):
        """Removes a noble once it has been chosen"""

        self._drawn_nobles.remove(card)


class Noble(EventHandler):
    def __init__(self,window,image,type,position,pp,gem,r,d,s,o,e,
    player_area,player,development_card):
        """Initializes each individual noble"""

        self._window = window
        self._image = image
        self._pp = pp
        self._gem = gem
        self._r = r
        self._d = d
        self._s = s
        self._o = o
        self._e = e
        self._type = type
        self._position = position
        self._legit = False
        self._player_area = player_area
        self._player = player

    def delete_card(self):
        """deletes the noble once it has been seleteced by a player"""

        self._window.remove(self._body)
        self._window.refresh()

    def get_pp(self):
        """Returns the PP of the noble"""

        return self._pp

    def r_value(self):
        """Returns the r value of the noble"""

        return self._r

    def d_value(self):
        """Returns the d value of the noble"""

        return self._d

    def s_value(self):
        """Returns the s value of the noble"""

        return self._s

    def o_value(self):
        """Returns the o value of the noble"""

        return self._o

    def e_value(self):
        """Returns the e value of the noble"""

        return self._e

    def get_legit(self):
        """Returns the legitimacy of the noble"""

        return self._legit

    def set_legit(self):
        """Sets set_legit to True if the noble can be acquired by a player"""

        self._legit = True

    def change_position(self,position):
        """changes posiiton of the noble"""

        self._position = position

    def draw(self):
        """draws the noble"""

        self._body = Image(self._window,self._image,100,130,self._position)
        self._body.set_depth(2)
        self._body.add_handler(self)
        self._window.add(self._body)


class DevelopmentCards():
    def __init__(self,window,player_area,player):
        """initializes Development Cards"""

        self._window = window
        self._player_area = player_area
        self._player = player

        self._level1_cards_images = cardimporter_yuh(r'Level1Card')
        self._level1_cards = []
        self._level2_cards_images = cardimporter_yuh(r'Level2Card')
        self._level2_cards = []
        self._level3_cards_images = cardimporter_yuh(r'Level3Card')
        self._level3_cards = []

        self.initialize_cards()

    def return_level_1_card(self):
        """Returns all the level 1 cards"""

        return self._level1_cards

    def return_level_2_card(self):
        """Returns all the level 2 cards"""

        return self._level2_cards

    def return_level_3_card(self):
        """Returns all the level 3 cards"""

        return self._level3_cards

    def initialize_cards(self):
        """Creates each individual Development Card and uses the pop method
            to draw a certain number of them"""

        for filename in self._level1_cards_images:
            pp = self._level1_cards_images[filename][0]
            gem = self._level1_cards_images[filename][1]
            r = self._level1_cards_images[filename][2]
            d = self._level1_cards_images[filename][3]
            s = self._level1_cards_images[filename][4]
            o = self._level1_cards_images[filename][5]
            e = self._level1_cards_images[filename][6]

            card = DevelopmentCard(self._window,'Level1Card/' + filename,1,
            (0,0),pp,gem,r,d,s,o,e, self._player_area, self._player, self)
            self._level1_cards.append(card)

        for filename in self._level2_cards_images:
            pp = self._level2_cards_images[filename][0]
            gem = self._level2_cards_images[filename][1]
            r = self._level2_cards_images[filename][2]
            d = self._level2_cards_images[filename][3]
            s = self._level2_cards_images[filename][4]
            o = self._level2_cards_images[filename][5]
            e = self._level2_cards_images[filename][6]

            card = DevelopmentCard(self._window,'Level2Card/' + filename,2,
            (0,0),pp,gem,r,d,s,o,e, self._player_area, self._player, self)
            self._level2_cards.append(card)

        for filename in self._level3_cards_images:
            pp = self._level3_cards_images[filename][0]
            gem = self._level3_cards_images[filename][1]
            r = self._level3_cards_images[filename][2]
            d = self._level3_cards_images[filename][3]
            s = self._level3_cards_images[filename][4]
            o = self._level3_cards_images[filename][5]
            e = self._level3_cards_images[filename][6]

            card = DevelopmentCard(self._window,'Level3Card/' + filename,3,
            (0,0),pp,gem,r,d,s,o,e, self._player_area, self._player, self)
            self._level3_cards.append(card)

        for posx,posy in level1_development_cards_pos:

            level1_development_cards_pos[(posx,posy)] = True

            chosen_card = self._level1_cards.pop(random.randint(0,
            len(self._level1_cards)-1))

            chosen_card.change_position((posx,posy))
            chosen_card.draw()

        for posx,posy in level2_development_cards_pos:

            level2_development_cards_pos[(posx,posy)] = True

            chosen_card = self._level2_cards.pop(random.randint(0,
            len(self._level2_cards)-1))

            chosen_card.change_position((posx,posy))
            chosen_card.draw()

        for posx,posy in level3_development_cards_pos:

            level3_development_cards_pos[(posx,posy)] = True

            chosen_card = self._level3_cards.pop(random.randint(0,
            len(self._level3_cards)-1))

            chosen_card.change_position((posx,posy))
            chosen_card.draw()


class DevelopmentCard(EventHandler):
    def __init__(self,window,image,type,position,pp,gem,
    r,d,s,o,e,player_area,player,development_card):
        """Initializes each individual development card"""

        self._window = window
        self._image = image
        self._pp = pp
        self._gem = gem
        self._r = r
        self._d = d
        self._s = s
        self._o = o
        self._e = e
        self._type = type
        self._position = position
        self._added = False
        self._player_area = player_area
        self._player = player
        self._development_cards = development_card
        self._reserved = False

    def delete_card(self):
        """Deletes the card if it was bought"""

        self._window.remove(self._body)
        self._window.refresh()

    def get_pp(self):
        """Returns the PP of the card"""

        return self._pp

    def gem_returned(self):
        """Returns the gem of the card"""

        return self._gem

    def r_value(self):
        """Returns the r value of the card"""

        return self._r

    def d_value(self):
        """Returns the d value of the card"""

        return self._d

    def s_value(self):
        """Returns the s value of the card"""

        return self._s

    def o_value(self):
        """Returns the o value of the card"""

        return self._o

    def e_value(self):
        """Returns the e value of the card"""

        return self._e

    def card_type(self):
        """Returns the card type"""

        return self._type

    def reservation(self):
        """Returns the reservation of the card"""

        return self._reserved

    def reserve(self):
        """Changes self._reserved to true if the player wants to reserve it"""

        self._reserved = True

    def return_position(self):
        """Returns the position of the card"""

        return self._position

    def change_position(self,position):
        """Changes the position of the card"""

        self._position = position

    def set_location(self,position):
        """Sets the location of the card by x and y coordinates"""

        self._x = position[0]
        self._y = position[1]

    def get_mouse_location(self):
        """Returns the location of the mouse release"""

        return (self._x ,self._y)

    def handle_mouse_release(self,event):
        """EventHandler so that the card can move"""

        self._window.remove(self._body)
        self._window.refresh()

        self.set_location(event.get_mouse_location())
        self.draw2()

        if self._player_area.check_collision(event.get_mouse_location(),
        100,130):
                self._player_area.add_card(self)

    def draw(self):
        """Draws the card with a position"""

        self._body = Image(self._window,self._image,100,130,self._position)
        self._body.set_depth(2)
        self._body.add_handler(self)
        self._window.add(self._body)

    def draw2(self):
        """Draws the card with x and y coordinates"""

        self._body = Image(self._window,self._image,100,130,(self._x,self._y))
        self._body.set_depth(2)
        self._body.add_handler(self)
        self._window.add(self._body)


class Gems():
    def __init__(self,window,player_area,gem_numbers):
        """Initializes Gems"""

        self._gem_types = ['ruby','diamond','onyx','sapphire','emerald']
        self._gem_numbers = gem_numbers
        self._number_of_cards = self._gem_numbers[0]
        self._player_gems_yuh = [0,0,0,0,0,0]
        self._player_gem_objects = []
        self._window = window
        self._player_area = player_area

        for gold_gem in range(5):
            path = 'images/'+ 'gold' + '.png'
            Gem(self._window,path,(640,550),'gold',self._player_area,
            self,self._player_gems_yuh)

        for gem in range(len(self._gem_types)):
            for card in range(self._number_of_cards):
                path = 'images/'+ self._gem_types[gem] + '.png'
                Gem(self._window,path,gem_pos[gem],self._gem_types[gem],
                self._player_area,self,self._player_gems_yuh)

    def return_player_gems(self):
        """returns the player gems"""

        return self._player_gems_yuh

    def return_gem_numbers(self):
        """returns the number of gems created"""

        return self._gem_numbers

    def reset_gems(self):
        """Resets gems back to 0"""

        self._player_gems_yuh = [0,0,0,0,0,0]

    def return_r_gems(self,leftover):
        """Returns r gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'ruby' + '.png'
            Gem(self._window,path,gem_pos[0],self._gem_types[0],
            self._player_area,self,self._player_gems_yuh)

    def return_d_gems(self,leftover):
        """Returns d gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'diamond' + '.png'
            Gem(self._window,path,gem_pos[1],self._gem_types[1],
            self._player_area,self,self._player_gems_yuh)

    def return_o_gems(self,leftover):
        """Returns o gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'onyx' + '.png'
            Gem(self._window,path,gem_pos[2],self._gem_types[2],
            self._player_area,self,self._player_gems_yuh)

    def return_s_gems(self,leftover):
        """Returns s gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'sapphire' + '.png'
            Gem(self._window,path,gem_pos[3],self._gem_types[3],
            self._player_area,self,self._player_gems_yuh)

    def return_e_gems(self,leftover):
        """Returns e gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'emerald' + '.png'
            Gem(self._window,path,gem_pos[4],self._gem_types[4],
            self._player_area,self,self._player_gems_yuh)

    def return_g_gems(self, leftover):
        """Returns g gems back to the board"""

        for gem in range(leftover):
            path = 'images/'+ 'gold' + '.png'
            Gem(self._window,path,(640,550),'gold',self._player_area,
            self,self._player_gems_yuh)


class Gem(EventHandler):
    def __init__(self,window,location,pos,type,player_area,gems,player_gems):
        """Initializes each Gem"""

        self._window = window
        self._x = pos[0]
        self._y = pos[1]
        self._location = location
        self._player_area = player_area
        self._added = False
        self._type = type
        self._gem_numbers = gems.return_gem_numbers()
        self.draw()
        self._gems = gems

    def delete_gem(self):
        """Deletes the gem off the board"""

        self._window.remove(self._body)

    def set_location(self,location):
        """Sets the location of the board"""

        self._x = location[0]
        self._y = location[1]

    def get_mouse_location(self):
        """gets the location of where the gem was released"""

        return (self._x ,self._y)

    def get_type(self):
        """Gets the gem type"""

        return self._type

    def get_gem_numbers(self):
        """Returns the number of this type of Gem"""

        return self._gem_numbers

    def handle_mouse_release(self,event):
        """EventHandler so that the gem can be moved"""

        self._window.remove(self._body)
        self._window.refresh()
        self.set_location(event.get_mouse_location())
        self.draw()
        self._player_gem = self._gems.return_player_gems()

        if self._player_area.check_collision(event.get_mouse_location(),70,70):

            if self._added == False:
                self._player_area.add_gems(self)
                self._added = True

                #makes it so that the a gem can be moved into the board"""
                if self._type == 'ruby':
                    self._gem_numbers[0] -= 1
                    self._player_gem[0] += 1

                if self._type == 'diamond':
                    self._gem_numbers[1] -= 1
                    self._player_gem[1] += 1

                if self._type == 'sapphire':
                    self._gem_numbers[2] -= 1
                    self._player_gem[2] += 1

                if self._type == 'onyx':
                    self._gem_numbers[3] -= 1
                    self._player_gem[3] += 1

                if self._type == 'emerald':
                    self._gem_numbers[4] -= 1
                    self._player_gem[4] += 1

                if self._type == 'gold':
                    self._gem_numbers[5] -= 1
                    self._player_gem[5] += 1


        elif self._added == True and \
        self._player_area.check_collision(event.get_mouse_location(),70,70) \
        == False:

            self._player_area.remove_gems(self)
            self._added = False

            #makes it so that a gem can be removed from the board"""
            if self._type == 'ruby':
                self._gem_numbers[0] += 1
                self._player_gem[0] -= 1

            if self._type == 'diamond':
                self._gem_numbers[1] += 1
                self._player_gem[1] -= 1

            if self._type == 'sapphire':
                self._gem_numbers[2] += 1
                self._player_gem[2] -= 1

            if self._type == 'onyx':
                self._gem_numbers[3] += 1
                self._player_gem[3] -= 1

            if self._type == 'emerald':
                self._gem_numbers[4] += 1
                self._player_gem[4] -= 1

            if self._type == 'gold':
                self._gem_numbers[5] += 1
                self._player_gem[5] -= 1

    def draw(self):
        """Draws the Gem"""
        self._body = Image(self._window,self._location,70,70,(self._x,self._y))
        self._body.set_depth(2)
        self._body.add_handler(self)
        self._window.add(self._body)


class Button(EventHandler):
    def __init__(self,window,area,board):
        """Button that allows the player to buy gems"""

        self._window = window
        self._body = Rectangle(self._window, 120, 70,(1120,260))
        self._text = Text(self._window,'Check Gems',14,(1120,260))
        self._player_area = area
        self._board = board
        self.draw()

    def draw(self):
        self._body.add_handler(self)
        self._text.add_handler(self)
        self._body.set_depth(3)
        self._text.set_depth(1)
        self._window.add(self._body)
        self._window.add(self._text)


    def handle_mouse_press(self,event):

        self.return_event_gems()

    def return_event_gems(self):

        #checks the player area to make sure the gems are valid
        if self._player_area.check_gems():
            self._board.switch_turns_gems()


class Button2(EventHandler):
    def __init__(self,window,area,board):
        """Button that allows the player to buy cards"""

        self._window = window
        self._body2 = Rectangle(self._window, 120, 70,(1120,330))
        self._text2 = Text(self._window,'Check Card',14,(1120,330))
        self._player_area = area
        self._board = board
        self.draw()

    def draw(self):

        self._body2.add_handler(self)
        self._text2.add_handler(self)
        self._body2.set_depth(3)
        self._text2.set_depth(1)
        self._window.add(self._body2)
        self._window.add(self._text2)

    def handle_mouse_press(self,event):

        self.return_event_cards()

    def return_event_cards(self):

        #checks the player area to make sure the card is valid
        if self._player_area.check_cards():
            self._board.switch_turns_cards()


class Button3(EventHandler):
    def __init__(self,window,area,board):
        """Button that allows the player to reserve"""

        self._window = window
        self._body3 = Rectangle(self._window, 120, 70,(1120,400))
        self._text3 = Text(self._window,'Reserve',14,(1120,400))
        self._player_area = area
        self._board = board
        self.draw()

    def draw(self):

        self._body3.add_handler(self)
        self._text3.add_handler(self)
        self._body3.set_depth(3)
        self._text3.set_depth(1)
        self._window.add(self._body3)
        self._window.add(self._text3)

    def handle_mouse_press(self,event):

        self.return_event_cards()

    def return_event_cards(self):
        self._board.switch_turns_reserve_cards()


class Player_Area():
    def __init__(self,window,board,player):
        """Initializeds the player area"""

        self._window = window
        self._position = (920,315)
        self._body = Rectangle(self._window, 170, 380,(950,350))
        self._body.set_fill_color('tan')
        self._player = player
        button = Button(self._window,self,board)
        button2 = Button2(self._window,self,board)
        button3 =  Button3(self._window,self,board)
        self.draw()

    def draw(self):
        """Draws the player area"""

        self._window.add(self._body)
        self._gems_placed = []
        self._card_placed = []

    def change_player(self,player):
        """Changes the player area of the player"""

        self._player = player

    def check_collision(self,object,width,height):
        """Checks to see if anything is in the player area"""

        rect1 = self._position
        rect1_width = 170
        rect1_height = 1000
        object_width = width
        object_height = height

        #makes sure that the object is within the player area
        if ((rect1[0] < object[0] + object_width) and \
        (rect1[0] + rect1_width > object[0]) and \
        (rect1[1] < object[1] + object_height) and \
        (rect1[1] + rect1_height > object[1])):
            return True
        else:
            return False

    def add_gems(self,gem):
        """Adds gems to the player area"""

        self._gems_placed.append(gem)

    def remove_gems(self,gem):
        """removes gems from the player area"""

        self._gems_placed.remove(gem)

    def add_card(self,card):
        """Adds cards to the player area"""

        self._card_placed.append(card)

    def return_card_placed(self):
        """returns the last card placed"""

        return self._card_placed[-1]

    def clear_area(self):
        """Resets the gems and cards placed"""

        for gem in self._gems_placed:
            gem.delete_gem()
        self._gems_placed[:] = []
        self._card_placed[:] = []

    def remove_cards_from_area(self):
        """Resets the cards in the area"""
        self._card_placed[:] = []

    def check_cards(self):
        """Checks to see if the card is valid"""

        self._player_gems = self._player.return_player_gems()
        self._player_card_gems = self._player.return_player_card_gems()

        self._player_card_r_gems = int(self._player_card_gems[0])
        self._player_card_d_gems = int(self._player_card_gems[1])
        self._player_card_s_gems = int(self._player_card_gems[2])
        self._player_card_o_gems = int(self._player_card_gems[3])
        self._player_card_e_gems = int(self._player_card_gems[4])

        self._r_gems = int(self._player_gems[0])
        self._d_gems = int(self._player_gems[1])
        self._s_gems = int(self._player_gems[2])
        self._o_gems = int(self._player_gems[3])
        self._e_gems = int(self._player_gems[4])
        self._g_gems = int(self._player_gems[5])

        #if statemnst that look at the values of a card and compares them to
        #the gems that the player has

        if int(self._card_placed[-1].r_value()) > self._r_gems \
        + self._g_gems + self._player_card_r_gems:
            return False

        elif int(self._card_placed[-1].d_value()) > self._d_gems \
        + self._g_gems + self._player_card_d_gems:
            return False

        elif int(self._card_placed[-1].s_value()) > self._s_gems \
        + self._g_gems + self._player_card_s_gems:
            return False

        elif int(self._card_placed[-1].o_value()) > self._o_gems \
        + self._g_gems + self._player_card_o_gems:
            return False

        elif int(self._card_placed[-1].e_value()) > self._e_gems \
         + self._g_gems + self._player_card_e_gems:
            return False

        else:
            return True

    def check_gems(self):
        """Checks to see if the gem is valid"""

        #checks to make sure the two gems that were placed are valid
        if not(len(self._gems_placed) > 3):
            if len(self._gems_placed) == 2:
                if self._gems_placed[0].get_type() == \
                self._gems_placed[1].get_type() :

                    type = self._gems_placed[0].get_type()
                    gem_numbers = self._gems_placed[0].get_gem_numbers()
                    number = 0

                    if type == 'ruby':
                        number = gem_numbers[0]

                    if type == 'diamond':
                        number = gem_numbers[1]

                    if type == 'sapphire':
                        number = gem_numbers[2]

                    if type == 'onyx':
                        number = gem_numbers[3]

                    if type == 'emerald':
                        number = gem_numbers[4]

                    if not (number < 2):
                        return True

            #checks to make sure that the 3 gems placed are valid
            elif len(self._gems_placed) == 3:
                type1 = self._gems_placed[0].get_type()
                type2 = self._gems_placed[1].get_type()
                type3 = self._gems_placed[2].get_type()
                if not (type1 == type2)  and not(type1 == type3) and \
                    not (type2 == type1) and not (type2==type3) and \
                    not (type3 == type1) and not(type3 == type2):
                        return True

            else:
                return False


class Background():
    def __init__(self,win):
        """Class that creates the background and the back of development card"""

        self._window = win           # graphics window

        self._body = Image(win,'images/icky.jpg',1200,1200,(600,600))
        self._level_1 = Image(win, 'images/level_1_background.jpg',
        100, 130,(75,220))
        self._level_2 = Image(win, 'images/level_2_background.jpg',
        100, 130,(75,370))
        self._level_3 = Image(win, 'images/level_3_background.jpg',
        100, 130,(75,520))
       # self._logo = Image(win, 'images/splendor_logo.jpg',
        #200, 100,(950,600))
        self.draw()

    def draw(self):
        """Draws the background and the development cards"""

        self._body.set_depth(90)
        self._window.add(self._body)
        self._window.add(self._level_1)
        self._window.add(self._level_2)
        self._window.add(self._level_3)
        #self._window.add(self._logo)


if __name__ == '__main__':
    StartGraphicsSystem(main)
