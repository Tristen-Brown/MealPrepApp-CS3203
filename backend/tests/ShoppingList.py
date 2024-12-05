import unittest
import Recipe_storage
from Recipe_storage import Recipe

class ShoppingList:
  
    #Takes in a recipe object, reads the ingredients for each and adds them to the shoppingList to return.
    #Catches empty lists, lists longer than 256 (who's going to buy more than 256 things in a shopping trip) and duplicate ingredients
    #Duplicate catching is very dumb because index function returns an error for some reason if it isn't in the list.
    def buildList(recipes):
        if not recipes:
            return []
        shoppingList = []
        numIterations = 0
        for recipe in recipes:
            numIterations += 1
            if(numIterations > 256):
                break
            
            ingredients = recipe.ingredients
            for ingredient in ingredients:
                try: #This is really bad but thats how python does index searching I guess.
                    i = shoppingList.index(ingredient)
                    continue
                except ValueError:
                    shoppingList.append(ingredient)
                    
        return shoppingList


class ShoppingListTest(unittest.TestCase):
    def setUp(self):
        self.Recipes = []
        self.Recipes.append(Recipe("Omlet",["Egg", "Flour", "Spinach", "Italian Sausage"],"Cook"))
        self.Recipes.append(Recipe("Burger", ["Bun", "Ground Beef", "Cheese", "Lettuce", "Tomato", "Mayonaise"], "Cook"))
        self.Recipes.append(Recipe("Hot Dog", ["Hot Dog Bun", "Jalepeno Cheese Hot Dog", "Shredded Cheese", "Ketchup"], "Cook"))
        self.Recipes.append(Recipe("Salad", ["Lettuce", "Tomato", "Crouton", "Shredded Cheese", "Ranch"], "Cook"))
        self.noRecipes = []
        self.tooManyRecipes = []
        for i in range(300): #Max of 256 recipes in list.
            self.tooManyRecipes.append(Recipe("",[str(i)],""))
        
        
    def testDuplicates(self):
        shoppingList = ShoppingList.buildList(self.Recipes)
        self.assertEqual(shoppingList, ["Egg", "Flour", "Spinach", "Italian Sausage", 
                                        "Bun", "Ground Beef", "Cheese", "Lettuce", "Tomato", "Mayonaise",
                                        "Hot Dog Bun", "Jalepeno Cheese Hot Dog", "Shredded Cheese", "Ketchup",
                                        "Crouton","Ranch"])
    
    def testNoRecipe(self):
        shoppingList = ShoppingList.buildList(self.noRecipes)
        self.assertEqual(shoppingList, [])
        
    def testTooManyRecipes(self):
        shoppingList = ShoppingList.buildList(self.tooManyRecipes)
        self.assertEqual(len(shoppingList), 256)
if __name__ == '__main__':
    unittest.main()