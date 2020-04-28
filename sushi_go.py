import random
import os



#game_info from https://boardgamegeek.com/boardgame/133473/sushi-go
game_info = "\nIn this super-fast sushi card game, you are eating at a sushi restaurant\n\
and trying to grab the best combination of sushi dishes as they whiz by.\n\
Score points for collecting the most sushi rolls or making a full set of\n\
sashimi. Dip your favorite nigiri in wasabi to triple its value! And once\n\
you've eaten it all, finish your meal with all the pudding you've got!\n\
But be careful which sushi you allow your friends to take; it might be\n\
just what they need to beat you!\n\n\
This game is played with 2 to 5 players and has 3 rounds. In each round,\n\
a pile of cards is dealt to each player. Each player will choose a card\n\
from their pile and reveal it in their hand. The pile of cards is\n\
passed to the next player until all piles are empty. The round ends and\n\
scores are calculated according to the description of each card.\n\n\
Card description summary:\n\
Maki Rolls: Player with the most rolls at the end of the round gains\n\
    6 points, second most rolls gains 3 points, and ties are split\n\
Tempura: A set of 2 gains 5 points, otherwise no points are awarded\n\
Sashimi: A set of 3 gains 10 points, otherwise no points are awarded\n\
Dumplings: 1, 2, 3, 4, and 5+ dumpling cards gain 1, 3, 6, 10, 15 \n\
    points, respectively\n\
Nigiri: A squid nigiri gains 3 points, salmon nigiri gains 2 points,\n\
    and egg nigiri gains 1 point\n\
Wasabi: A wasabi card triples the value of the next nigiri you select\n\
Chopsticks: You may use a chopsticks card on a later turn to swap for\n\
    two cards\n\
Puddings: Player with the most puddings at the end of 3 rounds gains\n\
    6 points, the least puddings loses 6 points, and ties are split\n\
    (no points are lost for games with 2 players)\n"

#dictionary of key = card name and value = [card description, number in deck]
card_info = {"Tempura": ["x2 = 5", 14], "Sashimi": ["x3 = 10", 14], "Dumpling": ["1 3 6 10 15", 14], 
             "3 Maki Rolls": ["Most 6/Second 3", 8], "2 Maki Rolls": ["Most 6/Second 3", 12],
             "1 Maki Roll": ["Most 6/Second 3", 8], "Squid Nigiri": ["3", 5], "Salmon Nigiri": ["2", 10], 
             "Egg Nigiri": ["1", 5], "Pudding": ["End Most 6/Least -6", 10], 
             "Wasabi": ["Next Nigiri x3", 6], "Chopsticks": ["Swap for 2", 4]}

#dictionary of key = number of players and value = number of cards in a pile
num_info = {2: 10, 3: 9, 4: 8, 5: 7}

#list of computer player names
player_names = ["Haru", "Saki", "Sora", "Hana", "Niko", "Kanna", "Luna", "Asami", "Ryota", "Kosuke", "Yuki", "Aoto", "Momo"]
random.shuffle(player_names)

class Card():
    """A Card object is initialized with card_info key and values.
    Init:
        1st argument (str): card name
        
    Attributes:
        name (str): card name
        description (str): card description
    """
    def __init__(self, card_name):
        self.name = card_name
        self.description = card_info[self.name][0]
        
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False
        
    def __lt__(self, other):
        if self.name < other.name:
            return True
        else:
            return False
        
    def __gt__(self, other):
        if self.name > other.name:
            return True
        else:
            return False

class Pile():
    """A Pile object is initialized during initialization of Round object and represents a list of Card objects.
    Init:
        1st argument (obj): a Game object
        2nd argument (obj): a Round object
        
    Attributes:
        pile (list): list of card objects popped from deck     
        
    Functions:
        display_cards(): prints the cards in the pile to the user
    """
    def __init__(self, game, round):
        self.pile = [game.deck.pop(0) for i in range(round.num_cards)]
        self.pile.sort()
        
    def __repr__(self):
        return str(self.pile)
    
    def display_cards(self):
        count = 0
        for card in self.pile:
            count += 1
            print("Your pile - Card " + str(count) + ": "+ card.name + " (" + card.description + ")")
        
class Player():
    """A Player object has two subclasses: HumanPlayer and ComputerPlayer.
    Init:
        1st argument (str): player_name
        
    Attributes:
        name (str): player's name
        hand (list): list of Card objects
        chosen_card (obj): a chosen Card object, initializes as None
        round_score (int): keeps track of the player's current round score, resets for new round
        game_score (int): keeps track of the player's game score
        pudding (int): keeps track of the number of pudding cards a player has for the game
        maki (int): keeps track of the number of maki rolls a player has for the round, resets for new round
        wasabi (list): list of True values for each wasabi a player has in hand, resets for new round
        sashimi (int): keeps track of the number of sashimi a player has, resets for new round or after reaching 3
        tempura (int): keeps track of the number of tempura a player has, resets for new round or after reaching 2
        dumpling(int): keeps track of the number of dumpling a player has, resets for new round
        chopsticks (list): list of True values for each chopsticks a player has in hand, resets for new round
        calc_functions (dict): a dictionary with key as the card name and values as a list [calculation function name, function parameter] 
        
    Functions:
        display_cards(name = player's name): prints the cards in the player's hand to the user
        add_round_score(game_round = Round(obj)): uses function from self.calc_functions dictionary, adds points to self.round_score
        calculate_tempura(param = None): add 1 to self.tempura, if there is 2 tempuras, reset self.tempura to 0 and return 5, otherwise return 0
        calculate_sashimi(param = None): add 1 to self.sashimi, if there is 3 sashimi, reset self.sashimi to 0 and return 10, otherwise return 0
        calculate_nigiri(param = 1, 2, or 3): if self.wasabi is not empty, return 3*param and pop one value from self.wasabi, otherwise return param
        calculate_dumpling(param = None): add 1 to self.dumpling, if self.dumpling is less than or equal to 5, return self.dumpling, otherwise return 0
        calculate_maki(param = 1, 2, or 3): add param to self.maki, return 0
        add_wasabi(param = None): append True to self.wasabi, return 0
        add_chopsticks(param = None): append True to self.chopsticks, return 0
        add_pudding(param = None): add 1 to self.pudding, return 0
        
    """
    def __init__(self, player_name):
        self.name = player_name
        self.hand = []
        self.chosen_card = None
        self.round_score = 0
        self.game_score = 0
        self.pudding = 0
        self.maki = 0
        self.wasabi = []
        self.sashimi = 0
        self.tempura = 0
        self.dumpling = 0
        self.chopsticks = []
        self.calc_functions = {"Tempura": [self.calculate_tempura, None], "Sashimi": [self.calculate_sashimi, None], "Egg Nigiri": [self.calculate_nigiri, 1], 
               "Salmon Nigiri": [self.calculate_nigiri, 2], "Squid Nigiri": [self.calculate_nigiri, 3], "Dumpling": [self.calculate_dumpling, None],
               "3 Maki Rolls": [self.calculate_maki, 3], "2 Maki Rolls": [self.calculate_maki, 2], "1 Maki Roll": [self.calculate_maki, 1],
               "Wasabi": [self.add_wasabi, None], "Chopsticks": [self.add_chopsticks, None], "Pudding": [self.add_pudding, None]}
    
    def __repr__(self):
        return self.name
    
    def display_cards(self, name):
        print("")
        if self.hand == []:
            print(name + " hand is empty.")
        else:
            #self.hand.sort()
            count = 0
            count_words = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
            print(name + " hand contains the cards:")
            for card in self.hand:
                print(name + " " + count_words[count] + " card: "+ card.name + " (" + card.description + ")")
                count += 1
    
    def calculate_tempura(self, param):
        self.tempura += 1
        if self.tempura == 2:
            self.tempura = 0
            return 5
        else:
            return 0
    
    def calculate_sashimi(self, param):
        self.sashimi += 1
        if self.sashimi == 3:
            self.sashimi = 0
            return 10
        else:
            return 0  
    
    def calculate_nigiri(self, param):
        if len(self.wasabi) != 0:
            self.wasabi.pop()
            return param*3
        else:
            return param
    
    def calculate_dumpling(self, param):
        self.dumpling += 1
        if self.dumpling <= 5:
            return self.dumpling
        else:
            return 0
    
    def calculate_maki(self, param):
        self.maki += param
        return 0
    
    def add_wasabi(self, param):
        self.wasabi.append(True)
        return 0
    
    def add_chopsticks(self, param):
        self.chopsticks.append(True)
        return 0
    
    def add_pudding(self, param):
        self.pudding += 1
        return 0
    
    def add_round_score(self, game_round):
        #call function based on self.chosen_card
        function = self.calc_functions[self.chosen_card.name]
        self.round_score += function[0](function[1])
        return self.round_score
        
class HumanPlayer(Player):
    """HumanPlayer objects are initialized during initialization of Game object. It is a subclass of the Player class.
    Init:
        1st argument (str): player_name
        
    Functions:
        select_a_card(pile = Pile(obj)): asks for a user input of which card to select from the pile, sets self.chosen_card to that card, 
                      appends it to self.hand, and removes it from the pile
        take_a_turn(game = Game(obj), game_round = Round(obj), pile = Pile(obj)): prints all player hands, asks user to select a card from pile,
                    if player has a chopsticks card, asks user if they want to use it, adds points to self.round_score, calls the functions:
                    self.display_cards(player_name), Pile.display_cards(), self.select_a_card(pile), self.add_round_score(game_round)
    """
    def __init__(self, player_name):
        super().__init__(player_name)
        
    def select_a_card(self, pile):
        pile_count = len(pile.pile)
        while True:
            choose = input("Which card do you want to move to your hand? Enter the card number: ")
            try:
                choose = int(choose)
                if choose <= 0 or choose > pile_count:
                    print("That's not a card in the pile. Enter a card number between 1 and", pile_count)
                else:
                    break
            except:
                if pile_count == 1:
                    print("There's only 1 card left in the pile. Enter card number 1.")
                
                #give user option to view game_info or quit game
                elif choose == "i":
                    print(game_info)
                elif choose == "q":
                    exit()
                
                else:
                    print("That's not a card in the pile. Enter a card number between 1 and", pile_count)
                    
        #set self.chosen_card, append it to hand and remove from pile
        self.chosen_card = pile.pile[choose-1]
        self.hand.append(self.chosen_card)
        pile.pile.remove(self.chosen_card)        
    
    def take_a_turn(self, game, game_round, pile):
        print("")
        print("It's", self.name + "'s turn!")
        print("-"*(13+len(self.name)))
        
        #prints the cards in everyone elses' hand
        for player in game.players:
            if player == self:
                continue
            player.display_cards(player.name + "'s")
            
        #print the cards in your hand
        self.display_cards("Your")

        #print the cards in the pile
        print("\nYou are passed a pile with the cards: ")
        pile.display_cards()
          
        #asks user to select a card in the pile
        self.select_a_card(pile)
        print("You selected a", self.chosen_card, "card.\n")
    
        #if chopsticks is in the hand and there are cards left in pile, give user the option to use it
        if len(self.chopsticks) != 0 and len(pile.pile) > 0:
            print("You currently have a Chopsticks card in your hand. Do you want to use it now?")
            while True:
                use_chopsticks = input("Enter 'y' to use it or 'n' to save it for later: ").lower()
                if use_chopsticks == "y":
                    
                    #if user wants to use chopsticks, first add to round score and update counters
                    self.round_score = self.add_round_score(game_round)
                    
                    #display cards in pile to user
                    print("\nYou have a pile with the cards:")
                    pile.display_cards()
                    self.select_a_card(pile)
                    
                    #remove chopsticks card from hand, append it back to pile, sort pile, and remove a value from self.chopsticks counter
                    self.hand.remove(Card("Chopsticks"))
                    pile.pile.append(Card("Chopsticks"))
                    pile.pile.sort()
                    self.chopsticks.pop()
                    print("You selected a", self.chosen_card, "card.\n")
                    break
                elif use_chopsticks == "n":
                    break
                
                #give user option to view game_info or quit game
                elif use_chopsticks == "i":
                    print(game_info)
                elif use_chopsticks == "q":
                    exit()
                
                else:
                    print("Not a valid command.")
                    
        #add to the round score and update counters
        self.round_score = self.add_round_score(game_round)

        #clear the screen
        clear()
    
class ComputerPlayer(Player):
    """ComputerPlayer objects are initialized during initialization of Game object. It is a subclass of the Player class.
    Init:
        1st argument (str): player_name
        
    Functions:
        take_a_turn(game = Game(obj), game_round = Round(obj), pile = Pile(obj)): randomly chooses a card from the pile, 
                    randomly uses chopsticks card if hand has one, calls the function: Player.add_round_score(game_round)
    """
    def __init__(self, player_name):
        super().__init__(player_name)
    
    def take_a_turn(self, game, game_round, pile):
        #set self.chosen_card randomly from the pile, append it to hand, remove it from pile, and add to round score and update counters
        self.chosen_card = random.sample(pile.pile, 1)[0]
        self.hand.append(self.chosen_card)
        pile.pile.remove(self.chosen_card)  
        
        #if chopsticks is in the hand and there are cards left in pile, give computer 50/50 chance to use it
        if len(self.chopsticks) != 0 and len(pile.pile) > 0:
            if random.randint(0, 1) == 1:
                
                #if computer wants to use chopsticks, first add to round score and update counters
                self.round_score = self.add_round_score(game_round)
                self.chosen_card = random.sample(pile.pile, 1)[0]
                pile.pile.remove(self.chosen_card)
                self.hand.append(self.chosen_card)
                
                #remove chopsticks card from hand, append it back to pile, sort pile, and remove a value from self.chopsticks counter
                self.hand.remove(Card("Chopsticks"))
                pile.pile.append(Card("Chopsticks"))
                pile.pile.sort()
                self.chopsticks.pop()
                print(self, "has a current round score of", self.round_score)
        
        #add to the round score and update counters        
        self.round_score = self.add_round_score(game_round)
        
class Game():
    """A Game object is initialized to play a game.
    Init:
        1st argument (int): number of human players
        2nd argument (list): list of human player names
        3rd argument (int): number of computer players
        
    Attributes:
        num_players (int): number of total players
        deck (list): list of Card objects, shuffled upon initialization
        players (list): list of HumanPlayers and ComputerPlayers objects (if applicable)
        rounds (list): list of Round objects
        scoreboard (dict): dictionary of key as Player object and values as list of scores [Round 1, Round 2, Round 3, Game]
        pudding_tally (dict): dictionary of key as number of puddings and values as list of Player objects with that number of puddings
        
    Functions:
        find_most_pudding(): find and add/subtract points for the players with the most and least number of puddings, and prints to user
        find_winner(): finds the players with the highest game_score
        begin_round(round_num = round number(int), game_round = Round(obj)): resets player counters, each player takes a turn for the number
                    of cards in the pile, maki score is added to the round score, the round score is added to their game score, 
                    scoreboard is displayed to user, pudding score is added to game score after 3 rounds, functions called:
                    Player.take_a_turn(game, game_round, pile), Player.display_cards(player_name), Round.find_most_maki(self), self.find_most_pudding()
        begin_game(): calls function begin_round(round_num, game_round) 3 times
    """
    def __init__(self, num_hplayers, name_hplayers, num_cplayers):
        num_players = num_hplayers + num_cplayers
        if num_players >= 2 and num_players <= 5:
            self.num_players = num_players
            self.deck = [Card(name) for name in card_info for i in range(card_info[name][1])]
            random.shuffle(self.deck)
            self.players = [HumanPlayer(name) for name in name_hplayers]+[ComputerPlayer(player_names[i]) for i in range(num_cplayers)]
            self.rounds = [Round(self) for i in range(3)]
            self.scoreboard = {player: ["-", "-", "-", "-"] for player in self.players}
            self.pudding_tally = {i: [] for i in range(11)}
        else:
            raise Exception("Only 2 to 5 people can play this game!")
            
    def find_most_pudding(self):
        #update self.pudding_tally
        for player in self.players:
            self.pudding_tally[player.pudding].append(player)
        
        #find max of keys where values is not an empty list
        most_pudding = max([key for key in self.pudding_tally if self.pudding_tally[key] != []])
        if most_pudding > 0:
            most_pudding_num = len(self.pudding_tally[most_pudding])
            ending_list = [", ", ", ", ", ", " and ", ""]
            
            #for player in the list of players with the most puddings, add points to their round_score
            for player in self.pudding_tally[most_pudding]:
                player.game_score += int(6/most_pudding_num)
                ending = ending_list.pop(5-most_pudding_num)
                print(player.name + ending, end = "")
            print(" had the most puddings in the game.")
            
        #if there are more than 2 players, find min of keys where values is not an empty list
        if self.num_players > 2:
            least_pudding = min([key for key in self.pudding_tally if self.pudding_tally[key] != []])
            
            #ensure that the least_pudding is less than most_pudding
            if most_pudding > least_pudding:
                least_pudding_num = len(self.pudding_tally[least_pudding])
                ending_list = [", ", ", ", ", ", " and ", ""]
                
                #for player in the list of players with the least puddings, subtract points to their round_score
                for player in self.pudding_tally[least_pudding]:
                    player.game_score -= int(6/least_pudding_num)
                    ending = ending_list.pop(5-least_pudding_num)
                    print(player.name + ending, end = "")
                print(" had the least puddings in the game.")
            
    def find_winner(self):
        highest_score = 0
        highest_score_players = []
        for player in self.players:
            if player.game_score > highest_score:
                highest_score = player.game_score
                highest_score_players = [player]
            elif player.game_score == highest_score:
                highest_score_players.append(player)
        return highest_score_players        
    
    def begin_round(self, round_num, game_round):
        print("\n=======")
        print("ROUND", round_num)
        print("=======")
        
        #reset player counters
        for player in self.players:
            player.hand = []
            player.chosen_card = None
            player.round_score = 0
            player.pudding = 0
            player.maki = 0
            player.wasabi = []
            player.sashimi = 0
            player.tempura = 0
            player.dumpling = 0
            player.chopsticks = [] 
            
        #start playing
        for n in range(game_round.num_cards):
            pile_index = 0
            for player in self.players:
                player.take_a_turn(self, game_round, game_round.piles[pile_index])
                pile_index += 1
            last_pile = game_round.piles.pop(-1)
            game_round.piles.insert(0, last_pile)
            
        #prints the cards in everyone's hand
        for player in self.players:
            player.display_cards(player.name + "'s")
            
        #add maki score to round score
        game_round.find_most_maki(self)
            
        #add round score to game score
        for player in self.players:
            player.game_score += player.round_score
            
        #add pudding score to game score
        if round_num == 3:
            self.find_most_pudding()
        
        #update game scoreboard
        for player in self.players:
            self.scoreboard[player][round_num-1] = player.round_score
            self.scoreboard[player][-1] = player.game_score
            #display pudding count for first and second rounds
            if round_num != 3:
                print(player, "has", player.pudding, "Pudding cards.")
        
        #display game scoreboard
        print("\nGame Scoreboard:")
        print("Player        Round 1      Round 2       Round 3      Game")
        print("-------------------------------------------------------------")
        for player in self.scoreboard:
            print(player.name, " "*(15-len(player.name)), 
            str(self.scoreboard[player][0]), " "*(11-len(str(self.scoreboard[player][0]))),
            str(self.scoreboard[player][1]), " "*(11-len(str(self.scoreboard[player][1]))),
            str(self.scoreboard[player][2]), " "*(11-len(str(self.scoreboard[player][2]))),
            str(self.scoreboard[player][3]), " "*(11-len(str(self.scoreboard[player][3]))))
        
        #print the winner(s)!
        if round_num == 3:
            winners = self.find_winner()
            ending_list = [", ", ", ", ", ", " and ", ""]
            print("")
            for winner in winners:
                ending = ending_list.pop(5-len(winners))
                print(winner.name + ending, end = "")
            print(" won the game!!!")
            
    def begin_game(self):
        self.begin_round(1, self.rounds[0])
        self.begin_round(2, self.rounds[1])
        self.begin_round(3, self.rounds[2])
    
class Round():
    """3 Round objects are initialized upon initialization of a Game object.
    Init:
        1st argument (obj): Game object
        
    Attributes:
        num_cards (int) = looks into num_info dictionary for number of cards associated with number of players
        piles (list) = list of Pile objects
        maki_tally (dict) = dictionary with key as number of maki rolls and values as list of Player objects with that number of maki rolls
    Functions:
        find_most_maki(): find and add points for the players with the most and second most number of maki rolls, and prints to user
    """
    def __init__(self, game):
        self.num_cards = num_info[game.num_players]
        self.piles = [Pile(game, self) for i in range(game.num_players)]
        self.maki_tally = {i: [] for i in range(21)}
    
    def find_most_maki(self, game):
        #update self.maki_tally
        for player in game.players:
            self.maki_tally[player.maki].append(player)
        
        #find max of keys where values is not an empty list
        most_maki = max([key for key in self.maki_tally if self.maki_tally[key] != []])
        if most_maki > 0:
            print("")
            most_maki_num = len(self.maki_tally[most_maki])
            ending_list = [", ", ", ", ", ", " and ", ""]
            
            #for player in the list of players with the most puddings, add points to their round_score
            for player in self.maki_tally[most_maki]:
                player.round_score += int(6/most_maki_num)
                ending = ending_list.pop(5-most_maki_num)
                print(player.name + ending, end = "")
            print(" had the most maki rolls in this round.")
        
        #find the second max of keys where values is not an empty list
        second_maki = max([key for key in self.maki_tally if self.maki_tally[key] != [] if key < most_maki])
        
        #only add points if the players with the second most maki had more than 0 maki rolls and there were no ties for the most maki
        if second_maki > 0 and most_maki_num == 1:
            second_maki_num = len(self.maki_tally[second_maki])
            ending_list = [", ", ", ", ", ", " and ", ""]
            
            #for player in the list of players with the most puddings, add points to their round_score
            for player in self.maki_tally[second_maki]:
                player.round_score += int(3/second_maki_num)
                ending = ending_list.pop(5-second_maki_num)
                print(player.name + ending, end = "")
            print(" had the second most maki rolls in this round.")
        print("")

#define our clear function 
def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def main():              
    print(" _______  __   __  _______  __   __  ___     _______  _______  __ ")
    print("|       ||  | |  ||       ||  | |  ||   |   |       ||       ||  |")
    print("|  _____||  | |  ||  _____||  |_|  ||   |   |    ___||   _   ||  |") 
    print("| |_____ |  |_|  || |_____ |       ||   |   |   | __ |  | |  ||  |") 
    print("|_____  ||       ||_____  ||       ||   |   |   ||  ||  |_|  ||__|")
    print(" _____| ||       | _____| ||   _   ||   |   |   |_| ||       | __ ")
    print("|_______||_______||_______||__| |__||___|   |_______||_______||__|") 
    
    print(game_info)
    print("Do you want to play?")
    
    while True:
        start_game = input("Press 'enter' to play, 'i' to see game info, or 'q' to quit: ").lower()
        
        #give user option to view game_info or quit game
        if start_game == "q":
            exit()
        elif start_game == "i":
            print(game_info)
        
        #if enter is selected, begin the game
        elif start_game == "":
            print("\nAt any time during the game, you may enter 'i' to see game info or 'q' to quit.\n")
            while True:
           
            #ask user for number of human players
                num_humans = input("How many human players? ")
                try:
                    num_humans = int(num_humans)
                    if num_humans < 1:
                        print("At least one human has to play!")
                    elif num_humans > 5:
                        print("Only a maximum of 5 players can play this game!")
                    else:
                        break
                except:
                    #give user option to view game_info or quit game
                    if num_humans == "i":
                        print(game_info)
                    elif num_humans == "q":
                        exit()
                        
                    else:
                        print("Not a valid input! Enter a number 1 to 5.")
            
            #ask user for names of human players
            order = ["first", "second", "third", "fourth", "fifth"]
            human_names = []
            for i in range(num_humans):
                while True:
                    human_name = input("What is the "+order[i]+" human player's name? ")
                    if len(human_name) > 15:
                        print("Your name is too long! Please enter a name less than 15 characters long.")
                    elif len(human_name) == 0:
                        print("Please input a player name!")
                    
                    #give user option to view game_info or quit game
                    elif human_name == "i":
                        print(game_info)
                    elif human_name == "q":
                        exit()
                    
                    else:
                        human_names.append(human_name)
                        break
            
            #if there is less than 5 human players, ask user for number of computer players
            if num_humans < 5:
                while True:
                    num_computers = input("How many computer players? ")
                    try:
                        num_computers = int(num_computers)
                        num_players = num_humans + num_computers
                        if num_players < 2:
                            print("There needs to be at least 2 players to play this game.")
                        elif num_players > 5:
                            print("Only a maximum of 5 players can play this game!")
                        else:
                            break
                    except:
                        if num_humans == 1:
                            print("Not a valid input! Enter a number 1 to", str(5-num_humans))
                        
                        #give user option to view game_info or quit game
                        elif num_computers == "i":
                            print(game_info)
                        elif num_computers == "q":
                            exit()
                        
                        else:
                            print("Not a valid input! Enter a number 0 to", str(5-num_humans))
            
            #if there is 5 or more human players, set number of computer players to 0
            else:
                num_computers = 0
            
            #initialize a Game object and begin game
            game = Game(num_humans, human_names, num_computers)
            game.begin_game()
            print("Do you want to play another game?")
            
        else:
            print("Not a valid command")
        
main()


