import 'dart:convert';
import 'package:http/http.dart' as http;

// Function fetches backend API (hello() function in app.py)
Future<void> fetchHello() async {
  final url = Uri.parse('http://127.0.0.1:5000/hello');
  final response = await http.get(url);

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    print(data['message']);  // Should print "Hello from Flask!"
  } else {
    print("Failed to load data: ${response.statusCode}");
  }
}
