import 'package:flutter/material.dart';

/// Custom page transitions for the DressApp
class AppPageTransitions {
  
  /// Slide transition from right to left
  static Route<T> slideFromRight<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(1.0, 0.0);
        const end = Offset.zero;
        final tween = Tween(begin: begin, end: end);
        final offsetAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return SlideTransition(
          position: offsetAnimation,
          child: child,
        );
      },
    );
  }
  
  /// Slide transition from left to right
  static Route<T> slideFromLeft<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(-1.0, 0.0);
        const end = Offset.zero;
        final tween = Tween(begin: begin, end: end);
        final offsetAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return SlideTransition(
          position: offsetAnimation,
          child: child,
        );
      },
    );
  }
  
  /// Fade transition
  static Route<T> fadeTransition<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 400),
    Curve curve = Curves.easeInOut,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: animation.drive(CurveTween(curve: curve)),
          child: child,
        );
      },
    );
  }
  
  /// Scale transition
  static Route<T> scaleTransition<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = 0.0;
        const end = 1.0;
        final tween = Tween(begin: begin, end: end);
        final scaleAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return ScaleTransition(
          scale: scaleAnimation,
          child: child,
        );
      },
    );
  }
  
  /// Slide up transition
  static Route<T> slideFromBottom<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 350),
    Curve curve = Curves.easeOutCubic,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(0.0, 1.0);
        const end = Offset.zero;
        final tween = Tween(begin: begin, end: end);
        final offsetAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return SlideTransition(
          position: offsetAnimation,
          child: child,
        );
      },
    );
  }
  
  /// Slide down transition
  static Route<T> slideFromTop<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 350),
    Curve curve = Curves.easeOutCubic,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(0.0, -1.0);
        const end = Offset.zero;
        final tween = Tween(begin: begin, end: end);
        final offsetAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return SlideTransition(
          position: offsetAnimation,
          child: child,
        );
      },
    );
  }
  
  /// Combined fade and slide transition
  static Route<T> fadeAndSlide<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 400),
    Curve curve = Curves.easeInOut,
    Offset slideOffset = const Offset(0.0, 0.3),
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        final fadeAnimation = animation.drive(CurveTween(curve: curve));
        final slideAnimation = animation.drive(
          Tween(begin: slideOffset, end: Offset.zero).chain(
            CurveTween(curve: curve),
          ),
        );
        
        return FadeTransition(
          opacity: fadeAnimation,
          child: SlideTransition(
            position: slideAnimation,
            child: child,
          ),
        );
      },
    );
  }
  
  /// Rotate transition
  static Route<T> rotateTransition<T extends Object?>(
    Widget page, {
    Duration duration = const Duration(milliseconds: 500),
    Curve curve = Curves.easeInOut,
  }) {
    return PageRouteBuilder<T>(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionDuration: duration,
      reverseTransitionDuration: duration,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = 0.0;
        const end = 1.0;
        final tween = Tween(begin: begin, end: end);
        final rotateAnimation = animation.drive(tween.chain(
          CurveTween(curve: curve),
        ));
        
        return RotationTransition(
          turns: rotateAnimation,
          child: FadeTransition(
            opacity: animation,
            child: child,
          ),
        );
      },
    );
  }
}

/// Page transition extensions for easier usage
extension PageTransitionExtensions on Widget {
  
  /// Navigate with slide from right transition
  Route<T> slideFromRight<T extends Object?>({
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return AppPageTransitions.slideFromRight<T>(
      this,
      duration: duration,
      curve: curve,
    );
  }
  
  /// Navigate with slide from left transition
  Route<T> slideFromLeft<T extends Object?>({
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return AppPageTransitions.slideFromLeft<T>(
      this,
      duration: duration,
      curve: curve,
    );
  }
  
  /// Navigate with fade transition
  Route<T> fadeTransition<T extends Object?>({
    Duration duration = const Duration(milliseconds: 400),
    Curve curve = Curves.easeInOut,
  }) {
    return AppPageTransitions.fadeTransition<T>(
      this,
      duration: duration,
      curve: curve,
    );
  }
  
  /// Navigate with scale transition
  Route<T> scaleTransition<T extends Object?>({
    Duration duration = const Duration(milliseconds: 300),
    Curve curve = Curves.easeInOut,
  }) {
    return AppPageTransitions.scaleTransition<T>(
      this,
      duration: duration,
      curve: curve,
    );
  }
  
  /// Navigate with slide from bottom transition
  Route<T> slideFromBottom<T extends Object?>({
    Duration duration = const Duration(milliseconds: 350),
    Curve curve = Curves.easeOutCubic,
  }) {
    return AppPageTransitions.slideFromBottom<T>(
      this,
      duration: duration,
      curve: curve,
    );
  }
  
  /// Navigate with fade and slide transition
  Route<T> fadeAndSlide<T extends Object?>({
    Duration duration = const Duration(milliseconds: 400),
    Curve curve = Curves.easeInOut,
    Offset slideOffset = const Offset(0.0, 0.3),
  }) {
    return AppPageTransitions.fadeAndSlide<T>(
      this,
      duration: duration,
      curve: curve,
      slideOffset: slideOffset,
    );
  }
}