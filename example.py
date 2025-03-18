#!/usr/bin/env python3
"""
x_console Example Script
========================

This script demonstrates all the key features of the x_console package.
Run this to test functionality before publishing.
"""

import time
import random
from x_console import CLIManager

def main():
    # Initialize the CLI manager with debug enabled
    cli = CLIManager(debug=True, debug_prefix="TEST")
    
    # Basic echo with formatting
    cli.echo("\n*Welcome to x_console Test Script*\n")
    cli.echo("This script demonstrates the main features of x_console.")
    cli.echoDim("Let's start with some basic formatting...")
    
    # Show formatting capabilities
    cli.echo("\n*Text Formatting:*")
    cli.echo("  • Default: *yellow* text, _italic_ text, and |dim| text")
    
    # Custom color tokens
    cli.echo("\n*Custom Color Tokens:*")
    cli.setColorTokens({
        "*": "bold red",
        "#": "blue",
        "~": "green italic",
        "@": "cyan underline"
    })
    cli.echo("  • Custom: *red bold*, #blue#, ~green italic~ and @underlined@!")
    
    # Reset to default tokens
    cli.setColorTokens({
        "*": "yellow",
        "_": "i",
        "|": "dim"
    })
    
    # User input with prompt
    cli.echo("\n*User Input:*")
    name = cli.prompt("What's your name?")
    cli.echo("Nice to meet you, *{name}*!", name=name)
    
    # Selection menu
    cli.echo("\n*Selection Menu:*")
    options = ["Option A", "Option B", "Option C", "Option D"]
    selected = cli.select("Please select an option:", options, default="Option A")
    cli.echo("You selected: *{option}*", option=selected)
    
    # Debug and warning messages
    cli.echo("\n*Debug and Warning Messages:*")
    cli.debug_("This is a _debug_ message with parameter: {param}", param="test-value")
    cli.warn_("This is a _warning_ message with parameter: {param}", param="caution")
    cli.log("This is a regular log message")
    
    # Processing with spinner
    cli.echo("\n*Processing with Spinner:*")
    
    def long_operation():
        """Simulate a long-running operation with progress updates."""
        steps = random.randint(5, 10)
        for i in range(1, steps + 1):
            time.sleep(0.8)  # Simulate work
            yield ("Step {step} of {total}: {action}...", {
                "step": i, 
                "total": steps,
                "action": random.choice(["Processing", "Calculating", "Analyzing", "Validating"])
            })
        yield ("Operation completed successfully!", {})
    
    cli.process(long_operation, message="Running example process")
    
    # Translation demo (if available)
    cli.echo("\n*Translation Features:*")
    try:
        # Try to detect language from Spanish input
        cli.setup_language("Hola mundo")
        cli.echo("Language detection active. This should be translated to Spanish.")
        
        # Reset to English
        cli.setup_language(language="en")
        cli.echo("Back to English now.")
        
        # Manual translation
        english = cli.translate("Bonjour le monde", target_lang="en")
        cli.echo("French 'Bonjour le monde' translated to English: *{text}*", text=english)
    except Exception as e:
        cli.echo("Translation features require additional dependencies.")
        cli.echoDim("Install with: pip install \"x_console[online]\" or \"x_console[full]\"")
        cli.debug_("Translation error: {error}", error=str(e))
    
    # CLI command example
    cli.echo("\n*CLI Commands:*")
    cli.echo("This package can be used to build CLI apps with rich_click.")
    cli.echo("Example command definition:")
    cli.echoDim("""
    @cli.command()
    @cli.option("--name", "-n", help="Your name")
    @cli.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
    def hello(name, verbose):
        '''Say hello to someone.'''
        if verbose:
            cli.debug_("Running with verbose mode")
        cli.echo("Hello, *{name}*!", name=name or "World")
    """)
    
    # Summary
    cli.echo("\n*Test Summary:*")
    cli.echo("All x_console features have been demonstrated.")
    cli.echo("You can use this script as a reference for your own applications.")
    cli.echo("For more information, check the *README.md* file.")
    
    # Graceful exit
    cli.echo("\n_Thank you for testing x_console!_\n")

if __name__ == "__main__":
    main()
