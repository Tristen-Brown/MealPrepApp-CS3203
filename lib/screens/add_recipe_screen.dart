import 'package:flutter/material.dart';

class AddRecipeScreen extends StatefulWidget {
  const AddRecipeScreen({super.key});

  @override
  State<AddRecipeScreen> createState() => _AddRecipeScreenState();
}

class _AddRecipeScreenState extends State<AddRecipeScreen> {
  final TextEditingController _recipeNameController = TextEditingController();
  final TextEditingController _ingredientsController = TextEditingController();
  final TextEditingController _instructionsController = TextEditingController();

  void saveRecipe() {
    final recipeName = _recipeNameController.text;
    final ingredients = _ingredientsController.text;
    final instructions = _instructionsController.text;

    if (recipeName.isEmpty || ingredients.isEmpty || instructions.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill out all fields.")),
      );
      return;
    }

    // Here, you could save the recipe to a database or local storage
    print("Recipe saved:");
    print("Name: $recipeName");
    print("Ingredients: $ingredients");
    print("Instructions: $instructions");

    // Show a success message and navigate back to the home screen
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Recipe saved successfully!")),
    );
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Add Recipe"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _recipeNameController,
              decoration: const InputDecoration(
                labelText: "Recipe Name",
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _ingredientsController,
              decoration: const InputDecoration(
                labelText: "Ingredients (comma-separated)",
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _instructionsController,
              decoration: const InputDecoration(
                labelText: "Instructions",
              ),
              maxLines: 5,
            ),
            const SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: saveRecipe,
                child: const Text("Save Recipe"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

