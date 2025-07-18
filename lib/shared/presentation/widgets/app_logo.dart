import 'package:flutter/material.dart';

class AppLogo extends StatefulWidget {
  final double size;
  final bool showBackground;
  final BorderRadius? borderRadius;
  final EdgeInsetsGeometry? margin;
  final bool animated;
  final Duration animationDuration;
  final bool showTagline;

  const AppLogo({
    super.key,
    this.size = 120,
    this.showBackground = true,
    this.borderRadius,
    this.margin,
    this.animated = true,
    this.animationDuration = const Duration(milliseconds: 1500),
    this.showTagline = false,
  });

  @override
  State<AppLogo> createState() => _AppLogoState();
}

class _AppLogoState extends State<AppLogo> with TickerProviderStateMixin {
  late AnimationController _controller;
  late AnimationController _pulseController;
  late Animation<double> _fadeAnimation;
  late Animation<double> _scaleAnimation;
  late Animation<double> _rotationAnimation;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    
    if (widget.animated) {
      _controller = AnimationController(
        duration: widget.animationDuration,
        vsync: this,
      );
      
      _pulseController = AnimationController(
        duration: const Duration(seconds: 2),
        vsync: this,
      );

      _fadeAnimation = Tween<double>(
        begin: 0.0,
        end: 1.0,
      ).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.0, 0.6, curve: Curves.easeOut),
      ));

      _scaleAnimation = Tween<double>(
        begin: 0.5,
        end: 1.0,
      ).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.2, 0.8, curve: Curves.elasticOut),
      ));

      _rotationAnimation = Tween<double>(
        begin: -0.1,
        end: 0.0,
      ).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.4, 1.0, curve: Curves.easeOut),
      ));

      _pulseAnimation = Tween<double>(
        begin: 1.0,
        end: 1.05,
      ).animate(CurvedAnimation(
        parent: _pulseController,
        curve: Curves.easeInOut,
      ));

      _controller.forward();
      
      // Start subtle pulse animation after main animation completes
      _controller.addStatusListener((status) {
        if (status == AnimationStatus.completed) {
          _pulseController.repeat(reverse: true);
        }
      });
    }
  }

  @override
  void dispose() {
    if (widget.animated) {
      _controller.dispose();
      _pulseController.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.animated) {
      return _buildLogo();
    }

    return AnimatedBuilder(
      animation: Listenable.merge([_controller, _pulseController]),
      builder: (context, child) {
        return FadeTransition(
          opacity: _fadeAnimation,
          child: Transform.scale(
            scale: _scaleAnimation.value * _pulseAnimation.value,
            child: Transform.rotate(
              angle: _rotationAnimation.value,
              child: _buildLogo(),
            ),
          ),
        );
      },
    );
  }

  Widget _buildLogo() {
    Widget logoWidget = Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Logo image
        Image.asset(
          'assets/images/logo.png',
          width: widget.size,
          height: widget.size,
          fit: BoxFit.contain,
          errorBuilder: (context, error, stackTrace) {
            // Fallback to custom DressApp logo
            return Container(
              width: widget.size,
              height: widget.size,
              decoration: BoxDecoration(
                color: const Color(0xFF461700),
                borderRadius: BorderRadius.circular(widget.size * 0.2),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.checkroom,
                    size: widget.size * 0.4,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'DressApp',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: widget.size * 0.12,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Segoe UI',
                    ),
                  ),
                ],
              ),
            );
          },
        ),
        
        // Tagline
        if (widget.showTagline) ...[
          const SizedBox(height: 8),
          Text(
            'Look better. Feel better.',
            style: TextStyle(
              color: const Color(0xFF461700).withOpacity(0.8),
              fontSize: widget.size * 0.1,
              fontWeight: FontWeight.w600,
              fontFamily: 'Segoe UI',
              letterSpacing: 0.5,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ],
    );

    if (widget.showBackground) {
      return Container(
        margin: widget.margin ?? const EdgeInsets.only(bottom: 32),
        decoration: BoxDecoration(
          borderRadius: widget.borderRadius ?? BorderRadius.circular(20),
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              const Color(0xFFFEFAD4), // Cream
              const Color(0xFFFFFFFF), // White
            ],
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 20,
              offset: const Offset(0, 10),
            ),
          ],
        ),
        child: ClipRRect(
          borderRadius: widget.borderRadius ?? BorderRadius.circular(20),
          child: Container(
            padding: const EdgeInsets.all(16),
            child: logoWidget,
          ),
        ),
      );
    }

    return Container(
      margin: widget.margin ?? const EdgeInsets.only(bottom: 32),
      child: logoWidget,
    );
  }
} 