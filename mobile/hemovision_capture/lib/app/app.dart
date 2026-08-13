import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/screens/home_screen.dart';

class HemoVisionApp extends StatelessWidget {
  const HemoVisionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HemoVision Research Prototype',
      theme: HemoVisionTheme.lightTheme,
      darkTheme: HemoVisionTheme.darkTheme,
      themeMode: ThemeMode.system,
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
