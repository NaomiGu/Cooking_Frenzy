# My own code
from termcolor import colored
import random
import threading
import time

class CookingGame:

    """The class representing the entire Cooking Frenzy game.

    Attributes:
    -----------
        input_func (function): A function is used for taking user input.
        current_category (str): The current category of cuisine being cooked.
        chosen_category (str): The category of cuisine that was chosen by the player.
        menu (dict): A dictionary containing the menu items categorized by diff cuisines.
        max_attempts (int): The maximum number of attempts allowed per round.
        rounds_to_win (int): The number of rounds required to win in a day.
        answered_correctly (int): The number of rounds answered correctly.
        total_rounds_played (int): The total number of rounds played.
        failed_rounds (int): The number of rounds failed.
        coins (int): The current number of coins the player has.
        current_day (int): The current day of the game.
        daily_expenses (dict): A dictionary containing the daily expenses.
        rent_due_day (int): The day when rent is due.
        rent_due (bool): Flag indicating if rent is due.
        bankrupt (bool): Flag indicating if the player has no money.
    """
    
    def __init__(self,input_func=input):
        
        """Initialize the CookingGame Class.
        
        Parameters:
        -----------
            input_func : function, optional
            A function used for taking user input. 
            Defaults to Python's built-in `input` function.
        """
        
        self.menu = {   # Menu provides five categories of cuisine
            "Italian": {
                "Pasta": ["Tomato", "Cheese", "Meat"],
                "Pizza": ["Tomato", "Cheese", "Meat"],
                "Lasagna": ["Pasta", "TomatoSauce", "GroundBeef"],
                "Fettuccine": ["Fettuccine", "AlfredoSauce", "Cheese"],
                "Spaghetti": ["Spaghetti", "TomatoSauce", "Meatballs"],
                "Carbonara": ["Pasta", "Eggs", "Bacon"],
                "Risotto": ["Rice", "ChickenBroth", "Mushrooms"],
                "Calzone": ["Dough", "TomatoSauce", "Cheese"],
                "Bruschetta": ["Bread", "Tomato", "Basil"],
                "Minestrone": ["Beans", "Tomato", "Vegetables"]
            },
            "Mexican": {
                "Tacos": ["Tortilla", "GroundBeef", "Cheese"],
                "Burrito": ["Tortilla", "Rice", "Beans"],
                "Guacamole": ["Avocado", "Tomato", "Onion"],
                "Enchiladas": ["Tortilla", "Chicken", "Cheese"],
                "Quesadilla": ["Tortilla", "Cheese", "Chicken"],
                "Fajitas": ["Chicken", "BellPeppers", "Onion"],
                "Chili": ["GroundBeef", "TomatoSauce", "Beans"],
                "Nachos": ["Chips", "Cheese", "Beans"],
                "Salsa": ["Tomato", "Onion", "Cilantro"],
                "Churros": ["Dough", "Sugar", "Cinnamon"]
            },
            "Asian": {
                "Sushi": ["Rice", "Nori", "Fish"],
                "Stir-Fry": ["Rice", "Chicken", "MixedVeggies"],
                "Pad Thai": ["RiceNoodles", "Peanuts", "Tofu"],
                "Ramen": ["Noodles", "Broth", "Egg"],
                "Teriyaki": ["Chicken", "TeriyakiSauce", "Rice"],
                "Fried Rice": ["Rice", "Eggs", "Veggies"],
                "Curry": ["Rice", "CurrySauce", "Chicken"],
                "Spring Rolls": ["RicePaper", "Veggies", "Shrimp"],
                "Bibimbap": ["Rice", "Beef", "Vegetables"],
                "Soba Noodles": ["SobaNoodles", "Broth", "Tofu"]
            },
            "American": {
                "Burger": ["GroundBeef", "Lettuce", "Tomato"],
                "Hot Dog": ["HotDogBun", "Sausage", "Ketchup"],
                "Mac and Cheese": ["Macaroni", "Cheese", "Milk"],
                "Chicken Wings": ["Chicken", "BuffaloSauce", "Celery"],
                "BBQ Ribs": ["Ribs", "BBQSauce", "ColeSlaw"],
                "Grilled Cheese": ["Bread", "Cheese", "Butter"],
                "Fried Chicken": ["Chicken", "Flour", "Oil"],
                "Meatloaf": ["Ground Beef", "Breadcrumbs", "Ketchup"],
                "Clam Chowder": ["Clams", "Potatoes", "Cream"],
                "Cornbread": ["Cornmeal", "Flour", "Milk"]
            },
            "Mediterranean": {
                "Greek Salad": ["Lettuce", "FetaCheese", "Olives"],
                "Hummus": ["Chickpeas", "Tahini", "OliveOil"],
                "Falafel": ["Chickpeas", "Garlic", "PitaBread"],
                "Tabbouleh": ["Bulgur", "Tomato", "Parsley"],
                "Shakshuka": ["Eggs", "Tomato", "BellPepper"],
                "Moussaka": ["Eggplant", "Potatoes", "GroundBeef"],
                "Gyro": ["PitaBread", "Lamb", "TzatzikiSauce"],
                "Dolma": ["GrapeLeaves", "Rice", "Herbs"],
                "Baklava": ["PhylloDough", "Walnuts", "Honey"],
                "Spanakopita": ["Spinach", "FetaCheese", "PhylloDough"]
            },
            "Breakfast": {
                "Omelette": ["Eggs", "Cheese", "Veggies"],
                "Pancakes": ["Flour", "Eggs", "Milk"],
                "French Toast": ["Bread", "Eggs", "Milk"],
                "Waffles": ["WaffleMix", "Eggs", "Milk"],
                "Bagel and Lox": ["Bagel", "CreamCheese", "SmokedSalmon"],
                "Egg Sandwich": ["Bread", "Eggs", "Cheese"],
                "Smoothie": ["Banana", "Berries", "Yogurt"],
                "Avocado Toast": ["Bread", "Avocado", "Tomato"],
                "Cereal": ["Cereal", "Milk", "Fruit"],
                "Quiche": ["PieCrust", "Eggs", "Bacon"]
            }
        }
        self.input_func = input_func
        self.current_category = None
        self.chosen_category = None
        self.max_attempts = 1
        self.rounds_to_win = 3 # Number of rounds needs to win in order to success in one day
        self.answered_correctly = 0
        self.total_rounds_played = 0
        self.failed_rounds = 0
        self.coins = 0  # Starting coins, initially 0
        self.current_day = -1  # Start from day 0
        self.daily_expenses = {"food": 50, "cat": 20, "rent": 200}  # Initial daily expenses
        self.rent_due_day = 3 # Need to pay rent every 3 days, other expenses are paid daily
        self.rent_due = False
        self.bankrupt = False

    def play_game(self):
        
        """
        Play the cooking game called Cooking Frenzy.

        This method initializes and controls the main loop of Cooking Frenzy.
        The player enters their name, and progresses through multiple days.
        They first choose a category of cuisine they wish to cook on the first day and cooking
        dishes from that category for subsequent days until the player quits or goes bankrupt.

        Returns:
        --------
            None
        """

        print("Welcome to Cooking Frenzy!")
        self.player_name = self.input_func("Your name: ")
        print(f"Hi {self.player_name}! Welcome to Cooking Frenzy!")
        from .background_story import print_back_story  # Use relative file path so that it works in notebook
        answer = self.input_func("Would you like to know the background story? "
                       "(yes/no): ").lower()
        if answer == "yes":
            print_back_story()  # Print background story

        while not self.bankrupt:

            self.current_day += 1
            print(f"\n--- Day {self.current_day} ---")
            print(f"You have {self.coins} Gollum coins.")

            if self.current_day > 0 and self.current_day % self.rent_due_day == 0:
                print("Rent is due today!")
                self.coins -= self.daily_expenses['rent']
                print(f"{self.daily_expenses['rent']} coins deducted for rent.")

            if (self.current_day > 0 and
                    self.coins < self.daily_expenses['food'] + self.daily_expenses['cat']):
                print("You don't have enough money to cover today's expenses. "
                      "You went bankrupt.")
                self.bankrupt = True
                break  # Terminate the game

            if self.current_day > 0:
                self.coins -= self.daily_expenses['food']
                print(f"{self.daily_expenses['food']} coins deducted for food.")

                self.coins -= self.daily_expenses['cat']
                print(f"{self.daily_expenses['cat']} coins deducted for cat food.")

            if self.current_day == 0 or self.current_category is None:
                self.current_category = self.choose_category()
                if self.current_category is None:
                    print("Invalid category. Please choose again.")
                    continue

            if self.current_category not in self.menu:
                print("Invalid category. Please choose again.")
                continue

            self.current_menu = self.menu[self.current_category]

            if not self.current_menu:
                continue  # Skip to the next iteration if menu is None

            self.total_rounds_played = 0  # Reset total rounds played for each day
            self.answered_correctly = 0
            self.failed_rounds = 0

            while (self.total_rounds_played < 5 and
                   self.answered_correctly < self.rounds_to_win):
                print(f"\nRound {self.total_rounds_played + 1}")
                chosen_dish = random.choice(list(self.current_menu.keys()))
                print(f"\nYou'll be making {chosen_dish}!\n")
                ingredients = self.current_menu[chosen_dish]
                print(f"To make {chosen_dish}, you need the following ingredients: "
                      f"{ingredients}\n")
                self.input_func("Press Enter to start cooking!")
                print("Let's start cooking!\n")
                self.ask_missing_ingredient(chosen_dish, ingredients)
                self.total_rounds_played += 1

            if self.answered_correctly >= self.rounds_to_win:
                print(colored("Congratulations! You won the day!", "green"))
                self.coins += 300
            else:
                print(colored("Sorry, you lost the day.", "red"))

            print(f"End of Day {self.current_day}. "
                  f"Now you have total of {self.coins} Gollum coins.")

            replay = self.input_func("Do you want to play another day? (yes/no): ").lower()
            if replay != "yes":
                break
            else:
                continue

    def choose_category(self): 
        """Prompt the player to choose a category.

        Returns:
            str: The chosen category by the player.
        """
        
        if self.chosen_category:
            print(f"Continue cooking from the '{self.chosen_category}' category.")
            return self.chosen_category
        
        print("Choose a category to cook from:")
        categories = {
            "1": "Italian",
            "2": "Mexican",
            "3": "Asian",
            "4": "American",
            "5": "Mediterranean",
            "6": "Breakfast"
        }
        for num, category in categories.items():
            print(f"{num}. {category}")
        choice = self.input_func("Enter the number of the category you want to cook from: ")
        return categories.get(choice, None)

    def ask_missing_ingredient(self, dish, ingredients):
        
        """Ask the player to provide the missing ingredient for a dish within a time limit.

        Parameters:
        -----------
            dish : str
            The name of the dish for which the missing ingredient needs to be added.
            ingredients : list
            A list of ingredients required to make the dishes.

        Returns:
        --------
        None

        Notes:
        ------
        This method asks the player to provide the input of missing ingredient for a random given 
        dish within a time limit of 5 seconds. If the player provides the correct ingredient
        within the time limit, they gain credit for the round; otherwise, they do not gain
        credit for the round.

        """
        
        random_ingredients = random.sample(ingredients, k=2)
        remaining_ingredient = [ingredient for ingredient in ingredients 
                                if ingredient not in random_ingredients]
        print((f"If you make {dish}, you have ingredients "
               f"{random_ingredients[0]} and {random_ingredients[1]}."))
        print("You have 5 seconds to provide the missing ingredient.")

        correct_answer_given = False  # Flag to track if correct answer is given within time limit

        def countdown_timer():
            nonlocal correct_answer_given
            for i in range(5, 0, -1):
                print(f"Time remaining: {i} seconds")
                time.sleep(1)
                if self.correct_answer_provided:
                    correct_answer_given = True
                    return
            if not self.correct_answer_provided:  # Check if correct answer was given after time expired
                print("Time's up!")
                self.failed_rounds += 1
                print("Sorry, you did not find the correct ingredient on time." 
                      " You did not gain credit for this round.")

        self.correct_answer_provided = False
        timer_thread = threading.Thread(target=countdown_timer)
        timer_thread.start()

        guess = self.input_func("Enter the missing ingredient to the dish: ").strip().lower()

        if guess == remaining_ingredient[0].lower():
            print(f"Correct! {remaining_ingredient[0]} is added to the dish.")
            self.answered_correctly += 1
            self.correct_answer_provided = True
        elif (len(remaining_ingredient) > 1 and 
              guess == remaining_ingredient[1].lower()):
            print(f"Correct! {remaining_ingredient[1]} is added to the dish.")
            self.answered_correctly += 1
            self.correct_answer_provided = True
        else:
            pass

        timer_thread.join()  # Wait for timer thread to finish

        if not correct_answer_given:  # Check if correct answer was given after time expired
            self.failed_rounds += 1
            print("Sorry, you did not find the correct ingredient on time." 
                  "You did not gain credit for this round.")


# Create the instance of Cooking_Game that be able to start the game
if __name__ == "__main__":
    game = Cooking_Game()
    game.play_game()
