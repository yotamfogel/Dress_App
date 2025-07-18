import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../shared/presentation/widgets/settings_button.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../../data/models/closet_item_model.dart';
import '../../../../core/services/ai_backend_manager.dart';

class MyClosetScreen extends ConsumerStatefulWidget {
  const MyClosetScreen({super.key});

  @override
  ConsumerState<MyClosetScreen> createState() => _MyClosetScreenState();
}

class _MyClosetScreenState extends ConsumerState<MyClosetScreen> {
  List<ClosetItemModel> _items = [];
  List<ClosetItemModel> _filteredItems = [];
  bool _loading = true;
  
  // Filter states
  List<String> _selectedClothingTypes = [];
  List<String> _selectedStyles = [];
  List<String> _selectedColors = [];
  bool _showFilters = false;
  
  // Available filter options
  List<String> _availableClothingTypes = [];
  List<String> _availableStyles = [];
  List<String> _availableColors = [];

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  Future<void> _loadItems() async {
    setState(() => _loading = true);
    try {
      final items = await ClosetDatabaseHelper.getAllItems();
      final clothingTypes = await ClosetDatabaseHelper.getUniqueClothingTypes();
      final styles = await ClosetDatabaseHelper.getUniqueStyles();
      final colors = await ClosetDatabaseHelper.getUniqueColors();
      
      setState(() {
        _items = items;
        _filteredItems = items;
        _availableClothingTypes = clothingTypes;
        _availableStyles = styles;
        _availableColors = colors;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error loading items: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _applyFilters() {
    setState(() {
      _filteredItems = _items.where((item) {
        // Filter by clothing type
        if (_selectedClothingTypes.isNotEmpty) {
          if (item.clothingType == null || 
              !_selectedClothingTypes.any((type) => 
                  item.clothingType!.toLowerCase().contains(type.toLowerCase()))) {
            return false;
          }
        }
        
        // Filter by style
        if (_selectedStyles.isNotEmpty) {
          if (!item.applicableStyles.any((style) => _selectedStyles.contains(style))) {
            return false;
          }
        }
        
        // Filter by color
        if (_selectedColors.isNotEmpty) {
          if (!item.colors.any((color) => 
              _selectedColors.any((filterColor) => 
                  color.name.toLowerCase().contains(filterColor.toLowerCase())))) {
            return false;
          }
        }
        
        return true;
      }).toList();
    });
  }

  void _clearFilters() {
    setState(() {
      _selectedClothingTypes.clear();
      _selectedStyles.clear();
      _selectedColors.clear();
      _filteredItems = _items;
    });
  }

  void _showAddItemDialog() {
    showDialog(
      context: context,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          title: const Text('Add Item to Closet'),
          content: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Choose how you want to add an item to your closet'),
              SizedBox(height: 8),
              Text(
                'AI analysis will automatically identify the clothing type, style, and colors.',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                _pickImage(ImageSource.camera);
              },
              child: const Text('Take Photo'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                _pickImage(ImageSource.gallery);
              },
              child: const Text('Choose from Gallery'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(source: source);
      
      if (image != null) {
        await _processAndSaveImage(image);
        _loadItems(); // Reload the items
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error picking image: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _processAndSaveImage(XFile imageFile) async {
    try {
      // Show loading dialog
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (BuildContext context) {
          return const AlertDialog(
            content: Row(
              children: [
                CircularProgressIndicator(),
                SizedBox(width: 16),
                Expanded(
                  child: Text('Analyzing clothing with AI...'),
                ),
              ],
            ),
          );
        },
      );

      // Analyze image with AI
      final aiResult = await AIBackendManager.analyzeFashion(File(imageFile.path));
      
      AIAnalysisData? aiAnalysis;
      
      if (aiResult != null && aiResult['success'] == true) {
        if (aiResult['multiple_items'] == true) {
          // Handle multiple items - show selection dialog
          Navigator.of(context).pop(); // Close loading dialog
          final selectedItem = await _showMultipleItemsDialog(aiResult['items']);
          
          if (selectedItem != null) {
            // Show loading dialog again
            showDialog(
              context: context,
              barrierDismissible: false,
              builder: (BuildContext context) {
                return const AlertDialog(
                  content: Row(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(width: 16),
                      Expanded(
                        child: Text('Analyzing selected item...'),
                      ),
                    ],
                  ),
                );
              },
            );
            
            // Analyze selected item
            final selectedResult = await AIBackendManager.selectFashionItem(
              File(imageFile.path), 
              selectedItem
            );
            
            if (selectedResult != null && selectedResult['success'] == true) {
              aiAnalysis = AIAnalysisData.fromJson(selectedResult['analysis']);
            }
          }
        } else {
          // Single item analysis
          aiAnalysis = AIAnalysisData.fromJson(aiResult);
        }
      }

      // Create item with AI analysis
      final item = ClosetItemModel(
        imagePath: imageFile.path,
        aiAnalysis: aiAnalysis,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      // Save to database
      await ClosetDatabaseHelper.insertItem(item);

      // Close loading dialog
      if (mounted) {
        Navigator.of(context).pop();
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              aiAnalysis != null 
                  ? 'Item added with AI analysis!'
                  : 'Item added (AI analysis failed)',
            ),
            backgroundColor: aiAnalysis != null ? Colors.green : Colors.orange,
          ),
        );
      }
    } catch (e) {
      // Close loading dialog
      if (mounted) {
        Navigator.of(context).pop();
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error processing image: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<int?> _showMultipleItemsDialog(List<dynamic> items) async {
    return showDialog<int>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Multiple Items Detected'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Please select which item to analyze:'),
              const SizedBox(height: 12),
              ...items.map<Widget>((item) {
                return ListTile(
                  leading: CircleAvatar(
                    child: Text(item['id'].toString()),
                  ),
                  title: Text(item['description']),
                  onTap: () {
                    Navigator.of(context).pop(item['id']);
                  },
                );
              }).toList(),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
          ],
        );
      },
    );
  }

  void _showItemDetails(ClosetItemModel item) {
    showDialog(
      context: context,
      builder: (BuildContext dialogContext) {
        return Dialog(
          backgroundColor: Colors.transparent,
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Image section
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                  child: Image.file(
                    File(item.imagePath),
                    height: 300,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                ),
                
                // Details section
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Clothing type
                      if (item.clothingType != null) ...[
                        Text(
                          'Type: ${item.clothingType!.toUpperCase()}',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                      ],
                      
                      // Colors
                      if (item.colors.isNotEmpty) ...[
                        Text(
                          'Colors:',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Wrap(
                          spacing: 8,
                          children: item.colors.map((color) {
                            return Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 8,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: Color.fromRGBO(
                                  color.rgb[0],
                                  color.rgb[1],
                                  color.rgb[2],
                                  1,
                                ),
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(color: Colors.grey.shade300),
                              ),
                              child: Text(
                                '${color.name} (${color.percentage.toStringAsFixed(1)}%)',
                                style: TextStyle(
                                  color: _getContrastColor(color.rgb),
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                        const SizedBox(height: 12),
                      ],
                      
                      // Patterns
                      if (item.patterns.isNotEmpty) ...[
                        Text(
                          'Patterns: ${item.patterns.join(', ')}',
                          style: const TextStyle(fontSize: 14),
                        ),
                        const SizedBox(height: 8),
                      ],
                      
                      // Date added
                      if (item.createdAt != null) ...[
                        Text(
                          'Added: ${item.createdAt!.toString().split(' ')[0]}',
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                
                // Close button
                Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: TextButton(
                    onPressed: () => Navigator.of(dialogContext).pop(),
                    child: const Text('Close'),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Color _getContrastColor(List<int> rgb) {
    // Calculate luminance to determine if we need light or dark text
    final luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255;
    return luminance > 0.5 ? Colors.black : Colors.white;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xFFFFFFFF), // White
              Color(0xFFFEFAD4), // Cream
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header with settings button
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'My Closet',
                      style: theme.textTheme.headlineMedium?.copyWith(
                        fontWeight: FontWeight.w900,
                        color: const Color(0xFF461700),
                        fontFamily: 'Segoe UI',
                      ),
                    ),
                    const SettingsButton(),
                  ],
                ),
              ),
              
              // Content
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      Text(
                        'Manage your digital wardrobe',
                        style: theme.textTheme.bodyLarge?.copyWith(
                          color: const Color(0xFF461700),
                          fontFamily: 'Segoe UI',
                          fontWeight: FontWeight.w600,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),
                      
                      _loading
                          ? const CircularProgressIndicator()
                          : _items.isEmpty
                              ? Expanded(
                                  child: Center(
                                    child: Column(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.checkroom_outlined,
                                          size: 64,
                                          color: Colors.grey.shade400,
                                        ),
                                        const SizedBox(height: 16),
                                        Text(
                                          'No items in your closet yet',
                                          style: TextStyle(
                                            fontSize: 18,
                                            color: Colors.grey.shade600,
                                          ),
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          'Add your first clothing item to get started!',
                                          style: TextStyle(
                                            fontSize: 14,
                                            color: Colors.grey.shade500,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                )
                              : Expanded(
                                  child: GridView.builder(
                                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                                      crossAxisCount: 2,
                                      crossAxisSpacing: 12,
                                      mainAxisSpacing: 12,
                                      childAspectRatio: 0.8,
                                    ),
                                    itemCount: _items.length,
                                    itemBuilder: (context, index) {
                                      final item = _items[index];
                                      return GestureDetector(
                                        onTap: () => _showItemDetails(item),
                                        child: Container(
                                          decoration: BoxDecoration(
                                            borderRadius: BorderRadius.circular(12),
                                            boxShadow: [
                                              BoxShadow(
                                                color: Colors.black.withValues(alpha: 0.1),
                                                blurRadius: 8,
                                                offset: const Offset(0, 2),
                                              ),
                                            ],
                                          ),
                                          child: ClipRRect(
                                            borderRadius: BorderRadius.circular(12),
                                            child: Stack(
                                              children: [
                                                // Image
                                                Image.file(
                                                  File(item.imagePath),
                                                  width: double.infinity,
                                                  height: double.infinity,
                                                  fit: BoxFit.cover,
                                                ),
                                                
                                                // Overlay with info
                                                Positioned(
                                                  bottom: 0,
                                                  left: 0,
                                                  right: 0,
                                                  child: Container(
                                                    decoration: BoxDecoration(
                                                      gradient: LinearGradient(
                                                        begin: Alignment.topCenter,
                                                        end: Alignment.bottomCenter,
                                                        colors: [
                                                          Colors.transparent,
                                                          Colors.black.withValues(alpha: 0.7),
                                                        ],
                                                      ),
                                                    ),
                                                    padding: const EdgeInsets.all(8),
                                                    child: Column(
                                                      crossAxisAlignment: CrossAxisAlignment.start,
                                                      mainAxisSize: MainAxisSize.min,
                                                      children: [
                                                        if (item.clothingType != null)
                                                          Text(
                                                            item.clothingType!.toUpperCase(),
                                                            style: const TextStyle(
                                                              color: Colors.white,
                                                              fontSize: 12,
                                                              fontWeight: FontWeight.bold,
                                                            ),
                                                          ),
                                                        if (item.colors.isNotEmpty)
                                                          Text(
                                                            item.colors.first.name,
                                                            style: const TextStyle(
                                                              color: Colors.white,
                                                              fontSize: 10,
                                                            ),
                                                          ),
                                                      ],
                                                    ),
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      );
                                    },
                                  ),
                                ),
                      
                      const SizedBox(height: 16),
                      
                      // Add Item Button
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _showAddItemDialog,
                          icon: const Icon(Icons.add),
                          label: const Text('Add Item to Closet'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFFFEFAD4),
                            foregroundColor: const Color(0xFF461700),
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
} 