# My own code
import pytest
from unittest.mock import MagicMock # Import MagicMock to mock user input
from cooking_frenzy import CookingGame

class TestCookingGame:
    def test_initial_day(self):
        """Check if the game starts on day 0.

        This test initializes the CookingGame instance and checks if the current_day attribute
        is set to -1, indicating that the game starts on day 0.
        """
        
        game = CookingGame(input_func = MagicMock(return_value = "Naomi"))
        assert game.current_day == -1

    def test_choose_category_invalid_choice(self):
        """Check if the choose_category method works fine with invalid inputs.

        This test verifies the behavior of the choose_category method when provided with invalid
        inputs, in this case like "7", "10", "invalid". It creates a CookingGame instance and 
        simulates user input with invalid choices. It checks if the method returns None in 
        response to invalid inputs.
        """
        
        game = CookingGame(input_func = MagicMock(side_effect = ["7", "10", "invalid"]))
        for _ in range(3):
            category = game.choose_category()
            assert category is None
            
    def test_initial_money(self):
        """Check if the initial amount of money is zero.

        This test verifies that the initial amount of money (the coins attribute) in the 
        CookingGame class is set to zero.
        """
        
        game = CookingGame(input_func = MagicMock(return_value = "Naomi"))
        assert game.coins == 0

