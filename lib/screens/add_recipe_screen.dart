import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:http_parser/http_parser.dart';

class AddRecipeScreen extends StatefulWidget {
  const AddRecipeScreen({super.key});

  @override
  State<AddRecipeScreen> createState() => _AddRecipeScreenState();
}

class _AddRecipeScreenState extends State<AddRecipeScreen> {
  final TextEditingController _recipeNameController = TextEditingController();
  List<TextEditingController> _ingredientControllers = [TextEditingController()];
  List<TextEditingController> _instructionControllers = [TextEditingController()];
  Uint8List? _selectedImageBytes;
  bool _isEditingFromAI = false;

  Future<void> pickAndSendImage() async {
    final ImagePicker picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image != null) {
      final bytes = await image.readAsBytes();
      setState(() {
        _selectedImageBytes = bytes;
      });
      await sendImageToServer(bytes);
    }
  }

  Future<void> sendImageToServer(Uint8List imageBytes) async {
    final url = Uri.parse('http://127.0.0.1:5000/upload_image');
    final request = http.MultipartRequest('POST', url);

    request.files.add(http.MultipartFile.fromBytes(
      'image',
      imageBytes,
      filename: 'pantry_image.jpg',
      contentType: MediaType('image', 'jpeg'),
    ));

    try {
      final response = await request.send();
      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        final jsonResponse = json.decode(responseBody);

        if (jsonResponse is Map<String, dynamic> && jsonResponse.containsKey('ingredients')) {
          final ingredients = jsonResponse['ingredients'];
          if (ingredients is List) {
            setState(() {
              _ingredientControllers = ingredients.map((ingredient) {
                return TextEditingController(text: ingredient);
              }).toList();
              _isEditingFromAI = true;
            });
          }
        }
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
  }

  void addIngredientField() {
    setState(() {
      _ingredientControllers.add(TextEditingController());
    });
  }

  void addInstructionField() {
    setState(() {
      _instructionControllers.add(TextEditingController());
    });
  }

  void saveRecipe() {
    final recipeName = _recipeNameController.text;
    final ingredients = _ingredientControllers.map((controller) => controller.text).toList();
    final instructions = _instructionControllers.map((controller) => controller.text).toList();

    if (recipeName.isEmpty || ingredients.every((ingredient) => ingredient.isEmpty)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Recipe name and at least one ingredient are required.")),
      );
      return;
    }

    // Here, you could save the recipe to a backend or local storage
    print("Recipe saved:");
    print("Name: $recipeName");
    print("Ingredients: ${ingredients.join(", ")}");
    print("Instructions: ${instructions.join(", ")}");

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Recipe saved successfully!")),
    );
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Add Recipe"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Manual Recipe Input Section
              const Text("Manual Recipe Input:"),
              TextField(
                controller: _recipeNameController,
                decoration: const InputDecoration(
                  labelText: "Recipe Name",
                ),
              ),
              const SizedBox(height: 10),
              const Text("Ingredients:"),
              ..._ingredientControllers.map((controller) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 5.0),
                  child: TextField(
                    controller: controller,
                    decoration: const InputDecoration(
                      labelText: "Ingredient",
                    ),
                    onSubmitted: (_) {
                      addIngredientField();
                      FocusScope.of(context).requestFocus(FocusNode());
                    },
                  ),
                );
              }).toList(),
              TextButton.icon(
                onPressed: addIngredientField,
                icon: const Icon(Icons.add),
                label: const Text("Add Ingredient"),
              ),
              const SizedBox(height: 10),
              const Text("Instructions:"),
              ..._instructionControllers.map((controller) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 5.0),
                  child: TextField(
                    controller: controller,
                    decoration: const InputDecoration(
                      labelText: "Instruction",
                    ),
                    onSubmitted: (_) {
                      addInstructionField();
                      FocusScope.of(context).requestFocus(FocusNode());
                    },
                  ),
                );
              }).toList(),
              TextButton.icon(
                onPressed: addInstructionField,
                icon: const Icon(Icons.add),
                label: const Text("Add Instruction"),
              ),
              const SizedBox(height: 20),
              Center(
                child: ElevatedButton(
                  onPressed: saveRecipe,
                  child: const Text("Save Recipe"),
                ),
              ),

              const SizedBox(height: 20),
              const Divider(),
              const SizedBox(height: 20),

              // AI Recipe Generation Section
              const Text("AI Recipe Generation:"),
              Center(
                child: Column(
                  children: [
                    if (_selectedImageBytes != null)
                      Image.memory(
                        _selectedImageBytes!,
                        height: 200,
                        width: 200,
                        fit: BoxFit.cover,
                      ),
                    TextButton.icon(
                      onPressed: pickAndSendImage,
                      icon: const Icon(Icons.image),
                      label: const Text("Upload Image"),
                    ),
                    ElevatedButton(
                      onPressed: _selectedImageBytes != null ? () => sendImageToServer(_selectedImageBytes!) : null,
                      child: const Text("Generate Recipe Suggestions"),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// import 'package:flutter/material.dart';
// import 'package:shared_preferences/shared_preferences.dart';
// import 'dart:convert';

// class AddRecipeScreen extends StatefulWidget {
//   const AddRecipeScreen({super.key});

//   @override
//   State<AddRecipeScreen> createState() => _AddRecipeScreenState();
// }

// class _AddRecipeScreenState extends State<AddRecipeScreen> {
//   final TextEditingController _nameController = TextEditingController();
//   final TextEditingController _ingredientsController = TextEditingController();
//   final TextEditingController _instructionsController = TextEditingController();

//   // Save the new recipe
//   Future<void> saveRecipe() async {
//     final name = _nameController.text.trim();
//     final ingredients = _ingredientsController.text.trim();
//     final instructions = _instructionsController.text.trim();

//     if (name.isEmpty || ingredients.isEmpty || instructions.isEmpty) {
//       ScaffoldMessenger.of(context).showSnackBar(
//         const SnackBar(content: Text("Please fill in all fields.")),
//       );
//       return;
//     }

//     final newRecipe = {
//       "name": name,
//       "ingredients": ingredients,
//       "instructions": instructions,
//     };

//     final prefs = await SharedPreferences.getInstance();
//     final String? recipesJson = prefs.getString('recipes');

//     List<Map<String, String>> recipes = [];
//     if (recipesJson != null) {
//       recipes = List<Map<String, String>>.from(json.decode(recipesJson));
//     }

//     recipes.add(newRecipe);
//     await prefs.setString('recipes', json.encode(recipes));

//     ScaffoldMessenger.of(context).showSnackBar(
//       const SnackBar(content: Text("Recipe added successfully!")),
//     );

//     // Clear fields and navigate back
//     _nameController.clear();
//     _ingredientsController.clear();
//     _instructionsController.clear();
//     Navigator.pop(context);
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text("Add Recipe"),
//       ),
//       body: Padding(
//         padding: const EdgeInsets.all(16.0),
//         child: Column(
//           children: [
//             TextField(
//               controller: _nameController,
//               decoration: const InputDecoration(
//                 labelText: "Recipe Name",
//               ),
//             ),
//             const SizedBox(height: 10),
//             TextField(
//               controller: _ingredientsController,
//               decoration: const InputDecoration(
//                 labelText: "Ingredients (comma-separated)",
//               ),
//               maxLines: 3,
//             ),
//             const SizedBox(height: 10),
//             TextField(
//               controller: _instructionsController,
//               decoration: const InputDecoration(
//                 labelText: "Instructions",
//               ),
//               maxLines: 5,
//             ),
//             const SizedBox(height: 20),
//             ElevatedButton(
//               onPressed: saveRecipe,
//               child: const Text("Save Recipe"),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }
