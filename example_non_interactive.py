#!/usr/bin/env python3
"""
x_console Non-Interactive Example Script
========================================

This is a non-interactive version of the example script that runs automatically
without requiring user input. Useful for testing the package before publishing.
"""

import time
import random
from x_console import CLIManager

# Custom wrapper for prompt to bypass actual user input
def mock_prompt(cli, prompt_text, default_value="Test User"):
    """Simulate user input by returning a default value."""
    cli.echo(f"{prompt_text} [auto-response: {default_value}]")
    return default_value

# Custom wrapper for select to bypass actual menu selection
def mock_select(cli, prompt_text, choices, default):
    """Simulate user selection by returning the default choice."""
    cli.echo(f"{prompt_text} [auto-selected: {default}]")
    return default

def main():
    # Initialize the CLI manager with debug enabled
    cli = CLIManager(debug=True, debug_prefix="TEST")

    # Store original methods
    original_prompt = cli.prompt
    original_select = cli.select

    # Replace with our mock methods
    cli.prompt = lambda text, *args, **kwargs: mock_prompt(cli, text, "Auto User")
    cli.select = lambda text, choices, default: mock_select(cli, text, choices, default)
    
    # Basic echo with formatting
    cli.echo("\n*Welcome to x_console Test Script (Non-Interactive)*\n")
    cli.echo("This script demonstrates the main features of x_console.")
    cli.echoDim("(Automatically running without requiring user input)")
    
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
    
    # User input with prompt (mocked)
    cli.echo("\n*User Input: (Automatic)*")
    name = cli.prompt("What's your name?")
    cli.echo("Nice to meet you, *{name}*!", name=name)
    
    # Selection menu (mocked)
    cli.echo("\n*Selection Menu: (Automatic)*")
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
    
    def short_operation():
        """Simulate a short operation with fewer steps for faster testing."""
        steps = 3
        for i in range(1, steps + 1):
            time.sleep(0.3)  # Shorter delay
            yield ("Step {step} of {total}: {action}...", {
                "step": i, 
                "total": steps,
                "action": random.choice(["Processing", "Calculating", "Analyzing"])
            })
        yield ("Operation completed successfully!", {})
    
    cli.process(short_operation, message="Running example process")
    
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
    cli.echoDim("(Example command definition omitted)")
    
    # Summary
    cli.echo("\n*Test Summary:*")
    cli.echo("All x_console features have been demonstrated in non-interactive mode.")
    cli.echo("This script can be used for automated testing before publishing the package.")
    
    # Restore original methods
    cli.prompt = original_prompt
    cli.select = original_select
    
    # Graceful exit
    cli.echo("\n_Test completed successfully!_\n")

if __name__ == "__main__":
    main()
