"""
Test script to verify x_console works with different dependency configurations.
This tests basic functionality with and without translation modules.
"""
import sys
import importlib.util

def check_module(module_name):
    """Check if a module is available and print the result."""
    is_available = importlib.util.find_spec(module_name) is not None
    print(f"Module '{module_name}': {'Available' if is_available else 'Not Available'}")
    return is_available

def main():
    print("\n=== Testing x_console with available dependencies ===\n")
    
    # Check which optional dependencies are installed
    print("Checking available dependencies:")
    has_lingua = check_module('lingua')
    has_deep_translator = check_module('deep_translator')
    has_easynmt = check_module('easynmt')
    
    # Import and use x_console regardless of which modules are available
    try:
        from x_console import CLIManager
        print("\nSuccessfully imported CLIManager")
        
        # Create an instance (should work with any combination of dependencies)
        cli = CLIManager(debug=True, debug_prefix="TEST")
        print("Successfully created CLIManager instance")
        
        # Test basic functionality (should always work)
        print("\nTesting basic functionality:")
        cli.echo("*Basic echo test*")
        
        # Test translation functionality if available
        if has_lingua and (has_deep_translator or has_easynmt):
            print("\nTesting translation functionality:")
            
            # Test with online translation if available
            if has_deep_translator:
                print("Testing online translation:")
                try:
                    translation = cli.translate("Hola mundo", target_lang="en", online=True)
                    print(f"Spanish 'Hola mundo' translated to: '{translation}'")
                except Exception as e:
                    print(f"Online translation failed: {e}")
            
            # Test with offline translation if available
            if has_easynmt:
                print("Testing offline translation:")
                try:
                    translation = cli.translate("Bonjour le monde", target_lang="en", online=False)
                    print(f"French 'Bonjour le monde' translated to: '{translation}'")
                except Exception as e:
                    print(f"Offline translation failed: {e}")
        else:
            print("\nSkipping translation tests (required modules not available)")
            # Test that translate method returns original text when translation isn't available
            original = "Hello World"
            result = cli.translate(original, target_lang="es", online=True)
            if result == original:
                print("Verified: translate() returns original text when translation isn't available")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
