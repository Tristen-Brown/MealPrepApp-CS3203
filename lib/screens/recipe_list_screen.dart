import 'package:flutter/material.dart';

class RecipeListScreen extends StatefulWidget {
  const RecipeListScreen({super.key});

  @override
  State<RecipeListScreen> createState() => _RecipeListScreenState();
}

class _RecipeListScreenState extends State<RecipeListScreen> {
  // Simulated recipe storage
  List<Map<String, String>> recipes = [
    {
      "name": "Spaghetti Bolognese",
      "ingredients": "Spaghetti, Ground Beef, Tomato Sauce, Onion, Garlic",
      "instructions": "Cook spaghetti. Cook beef with onion and garlic. Add sauce.",
    },
    {
      "name": "Grilled Chicken Salad",
      "ingredients": "Chicken Breast, Lettuce, Tomato, Cucumber, Olive Oil",
      "instructions": "Grill chicken. Chop veggies. Mix with olive oil.",
    },
    {
      "name": "Garlic Bread",
      "ingredients": "Bread, Butter, Garlic, Parsley",
      "instructions": "Spread garlic butter on bread. Toast in oven.",
    },
  ];

  // List for search results
  List<Map<String, String>> filteredRecipes = [];

  // Text editing controller for search input
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    filteredRecipes = recipes; // Initially display all recipes
  }

  // Search function
  void searchRecipes(String query) {
    final lowerCaseQuery = query.toLowerCase();
    setState(() {
      filteredRecipes = recipes.where((recipe) {
        final name = recipe["name"]!.toLowerCase();
        final ingredients = recipe["ingredients"]!.toLowerCase();
        return name.contains(lowerCaseQuery) || ingredients.contains(lowerCaseQuery);
      }).toList();
    });
  }

  // Method to delete a recipe
  void deleteRecipe(int index) {
    setState(() {
      recipes.removeAt(index);
      filteredRecipes = recipes;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Recipe deleted successfully!")),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Saved Recipes"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _searchController,
              decoration: const InputDecoration(
                labelText: "Search Recipes",
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: searchRecipes,
            ),
            const SizedBox(height: 10),
            Expanded(
              child: filteredRecipes.isEmpty
                  ? const Center(
                      child: Text("No recipes found."),
                    )
                  : ListView.builder(
                      itemCount: filteredRecipes.length,
                      itemBuilder: (context, index) {
                        final recipe = filteredRecipes[index];
                        return Card(
                          margin: const EdgeInsets.all(10),
                          child: ListTile(
                            title: Text(recipe["name"]!),
                            subtitle: Text(recipe["ingredients"]!),
                            trailing: IconButton(
                              icon: const Icon(Icons.delete, color: Colors.red),
                              onPressed: () {
                                showDialog(
                                  context: context,
                                  builder: (context) {
                                    return AlertDialog(
                                      title: const Text("Delete Recipe"),
                                      content: Text("Are you sure you want to delete \"${recipe["name"]}\"?"),
                                      actions: [
                                        TextButton(
                                          onPressed: () => Navigator.pop(context),
                                          child: const Text("Cancel"),
                                        ),
                                        TextButton(
                                          onPressed: () {
                                            deleteRecipe(index);
                                            Navigator.pop(context);
                                          },
                                          child: const Text("Delete", style: TextStyle(color: Colors.red)),
                                        ),
                                      ],
                                    );
                                  },
                                );
                              },
                            ),
                            onTap: () {
                              showDialog(
                                context: context,
                                builder: (context) {
                                  return AlertDialog(
                                    title: Text(recipe["name"]!),
                                    content: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        const Text("Ingredients:"),
                                        Text(recipe["ingredients"]!),
                                        const SizedBox(height: 10),
                                        const Text("Instructions:"),
                                        Text(recipe["instructions"]!),
                                      ],
                                    ),
                                    actions: [
                                      TextButton(
                                        onPressed: () {
                                          Navigator.pop(context);
                                        },
                                        child: const Text("Close"),
                                      ),
                                    ],
                                  );
                                },
                              );
                            },
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

