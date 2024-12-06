import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class DietaryRestrictionsScreen extends StatefulWidget {
  @override
  _DietaryRestrictionsScreenState createState() =>
      _DietaryRestrictionsScreenState();
}

class _DietaryRestrictionsScreenState
    extends State<DietaryRestrictionsScreen> {
  final TextEditingController _restrictionsController = TextEditingController();
  String _result = "";

  // Function to send the dietary restrictions to the Flask backend
  Future<void> validateDietaryRestrictions() async {
    final String restrictions = _restrictionsController.text;
    if (restrictions.isEmpty) {
      setState(() {
        _result = "Please enter dietary restrictions.";
      });
      return;
    }

    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/validate_dietary_restrictions'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'restrictions': restrictions}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        _result = data['message'];
      });
    } else {
      setState(() {
        _result = "Failed to validate dietary restrictions.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Dietary Restrictions Validation"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _restrictionsController,
              decoration: InputDecoration(
                labelText: "Enter dietary restrictions",
                hintText: "e.g., vegan, gluten-free, keto",
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: validateDietaryRestrictions,
              child: Text("Validate Restrictions"),
            ),
            SizedBox(height: 20),
            Text(_result),
          ],
        ),
      ),
    );
  }
}
