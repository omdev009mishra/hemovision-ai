import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';

class ConjunctivaPreviewCard extends StatefulWidget {
  final String? imagePath;
  final String? roiMaskB64;

  const ConjunctivaPreviewCard({
    super.key,
    this.imagePath,
    this.roiMaskB64,
  });

  @override
  State<ConjunctivaPreviewCard> createState() => _ConjunctivaPreviewCardState();
}

class _ConjunctivaPreviewCardState extends State<ConjunctivaPreviewCard> {
  int _selectedTab = 0; // 0: Original, 1: ROI Mask

  @override
  Widget build(BuildContext context) {
    final bool hasPath = widget.imagePath != null && File(widget.imagePath!).existsSync();
    final bool hasMask = widget.roiMaskB64 != null && widget.roiMaskB64!.isNotEmpty;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Flexible(
                  child: Text(
                    'Conjunctiva Inspection',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  decoration: BoxDecoration(
                    color: const Color(0xFF1F2937),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      _buildTabButton(0, 'ORIGINAL'),
                      _buildTabButton(1, 'ROI MASK'),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: SizedBox(
                height: 180,
                width: double.infinity,
                child: _selectedTab == 0
                    ? (hasPath
                        ? Image.file(File(widget.imagePath!), fit: BoxFit.cover)
                        : _buildPlaceholder('Original Image Preview'))
                    : (hasMask
                        ? Image.memory(base64Decode(widget.roiMaskB64!), fit: BoxFit.cover)
                        : _buildPlaceholder('Palpebral ROI Mask Visual Overlay')),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTabButton(int index, String label) {
    final isSelected = _selectedTab == index;
    return GestureDetector(
      onTap: () => setState(() => _selectedTab = index),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? HemoVisionTheme.tealAccent : Colors.transparent,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w800,
            color: isSelected ? Colors.black : HemoVisionTheme.textMuted,
          ),
        ),
      ),
    );
  }

  Widget _buildPlaceholder(String label) {
    return Container(
      color: const Color(0xFF111827),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.remove_red_eye_outlined, size: 36, color: HemoVisionTheme.textMuted),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(fontSize: 12, color: HemoVisionTheme.textMuted)),
          ],
        ),
      ),
    );
  }
}
