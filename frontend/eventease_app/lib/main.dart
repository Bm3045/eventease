// main.dart
// ------------------------------
// EventEase Mobile - Flutter Frontend
// ------------------------------
// ✅ Features:
// - Fetch events from backend
// - Login using demo user
// - Book an event
// - Show Snackbar notifications
// ------------------------------

import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

// 🔹 Backend API URL
// Chrome / Web ke liye: localhost
// Android Emulator ke liye hota: 10.0.2.2
const String API_BASE = "http://127.0.0.1:8000";

void main() {
  runApp(const EventEaseApp());
}

// 🔹 Main App Widget
class EventEaseApp extends StatefulWidget {
  const EventEaseApp({super.key});

  @override
  State<EventEaseApp> createState() => _EventEaseAppState();
}

class _EventEaseAppState extends State<EventEaseApp> {
  // JWT token after login
  String token = "";

  // List of events fetched from API
  List<dynamic> events = [];

  @override
  void initState() {
    super.initState();
    fetchEvents(); // app start hone par events fetch karo
  }

  // -----------------------------
  // 🔸 Function: Fetch events
  // -----------------------------
  Future<void> fetchEvents() async {
    try {
      final response = await http.get(Uri.parse("$API_BASE/events"));
      if (response.statusCode == 200) {
        setState(() {
          events = jsonDecode(response.body);
        });
      } else {
        throw Exception("Failed to fetch events");
      }
    } catch (e) {
      print("Error fetching events: $e");
    }
  }

  // -----------------------------
  // 🔸 Function: Login demo user
  // -----------------------------
  Future<void> login() async {
    try {
      final response = await http.post(
        Uri.parse("$API_BASE/login"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"email": "test@example.com", "password": "pass123"}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          token = data["access_token"];
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("✅ Login successful")),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("❌ Invalid credentials")),
        );
      }
    } catch (e) {
      print("Login error: $e");
    }
  }

  // -----------------------------
  // 🔸 Function: Book event
  // -----------------------------
  Future<void> bookEvent(int eventId) async {
    if (token.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("⚠️ Please login first")),
      );
      return;
    }

    try {
      final response = await http.post(
        Uri.parse("$API_BASE/book/$eventId"),
        headers: {
          "Authorization": "Bearer $token",
        },
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("✅ Booking successful")),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("❌ Booking failed: ${response.body}")),
        );
      }
    } catch (e) {
      print("Booking error: $e");
    }
  }

  // -----------------------------
  // 🔸 UI Layout
  // -----------------------------
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "EventEase",
      home: Scaffold(
        appBar: AppBar(
          title: const Text("EventEase"),
          backgroundColor: Colors.blueAccent,
          centerTitle: true,
        ),
        body: RefreshIndicator(
          onRefresh: fetchEvents, // Pull down to refresh events
          child: Column(
            children: [
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: login,
                child: Text(
                  token.isEmpty ? "Login (Demo User)" : "Logged In ✅",
                ),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: events.isEmpty
                    ? const Center(child: CircularProgressIndicator())
                    : ListView.builder(
                        itemCount: events.length,
                        itemBuilder: (context, index) {
                          final e = events[index];
                          return Card(
                            margin: const EdgeInsets.symmetric(
                                horizontal: 12, vertical: 6),
                            elevation: 3,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: ListTile(
                              leading: const Icon(Icons.event),
                              title: Text(
                                e["title"],
                                style: const TextStyle(
                                    fontWeight: FontWeight.bold, fontSize: 16),
                              ),
                              subtitle: Text(
                                "${e["date"].toString().split('T')[0]} • ${e["location"] ?? 'N/A'}",
                                style: const TextStyle(fontSize: 13),
                              ),
                              trailing: ElevatedButton(
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.green,
                                  foregroundColor: Colors.white,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                onPressed: () => bookEvent(e["id"]),
                                child: const Text("Book"),
                              ),
                            ),
                          );
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
