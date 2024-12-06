import 'package:flutter/material.dart';
import 'macros_calculator_screen.dart';
import 'add_recipe_screen.dart';
import 'recipe_list_screen.dart';
import 'meal_recommendation_screen.dart';  // Import the new screen
//import 'meal_prep_list_screen.dart';
import 'meal_plan_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Meal Prep App"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const MacrosCalculatorScreen()),
                );
              },
              child: const Text("Go to Macros Calculator"),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const AddRecipeScreen()),
                );
              },
              child: const Text("Add Recipe"),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const RecipeListScreen()),
                );
              },
              child: const Text("View Saved Recipes"),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const MealRecommendationScreen()),
                );
              },
              child: const Text("Get Meal Recommendations"),
            // ), const SizedBox(height: 10), 
            // ElevatedButton(
            //   onPressed: () {
            //     Navigator.push(
            //       context,
            //       MaterialPageRoute(builder: (context) => const MealPlanInputScreen()),
            //     );
            //   },
            //   child: const Text("Go to Meal Plan Validator"),
            // ), const SizedBox(height: 10), 
            // ElevatedButton(
            //   onPressed: () {
            //     Navigator.push(
            //       context,
            //       MaterialPageRoute(builder: (context) => const MealPlanScreen()),
            //     );
            //   },
            // child: const Text("Meal Plan Validator"),
            ), const SizedBox(height: 10), 
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const MealPlanScreen()),
                );
              },
            child: const Text("Create Meal Plan"),
            ),
          ],
        ),
      ),
    );
  }
}
