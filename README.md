# x_console

[![PyPI version](https://img.shields.io/pypi/v/x_console.svg)](https://pypi.org/project/x_console/)
[![Python Versions](https://img.shields.io/pypi/pyversions/x_console.svg)](https://pypi.org/project/x_console/)
[![License](https://img.shields.io/github/license/puntorigen/x_console.svg)](https://github.com/puntorigen/x_console/blob/main/LICENSE)

Python CLI class for nice and easy user interaction, with coloring, formatting and automatic translation support.

## Features

- **Rich Text Formatting** - Apply colors and styles with simple token markers
- **Automatic Translation** - Detect input language and translate output (supports both online and offline modes)
- **Interactive Prompts** - Simple prompts, menus and selection dialogs
- **Spinners and Progress Indicators** - Show processing status with animated spinners
- **Rich Command Line Interface** - Built on top of rich_click with beautiful styling
- **Debug and Logging** - Formatted debug messages and warnings

## Installation

```bash
# Basic installation
pip install x_console

# With online translation support (using Google Translate)
pip install "x_console[online]"

# With offline translation support (using EasyNMT)
pip install "x_console[offline]"

# Full installation with all translation features
pip install "x_console[full]"
```

## Basic Usage

```python
from x_console import CLIManager

# Initialize the CLI manager
cli = CLIManager(debug=True, debug_prefix="APP")

# Display formatted message
cli.echo("Hello *World*! This text has _italic_ and |dim| formatting.")

# Ask for user input
name = cli.prompt("What is your name?")
cli.echo("Nice to meet you, *{name}*!", name=name)

# Show a process with spinner
def my_task():
    # This generator yields status update messages
    yield ("Starting process...", {})
    yield ("Processing step {step}...", {"step": 1})
    yield ("Processing step {step}...", {"step": 2})
    yield ("Finalizing...", {})
    
cli.process(my_task, message="Running task")
```

## Text Formatting

x_console provides simple token-based formatting:

```python
# Default token mappings:
# * for yellow text
# _ for italic text
# | for dim text

cli.echo("This is *yellow* text with _italic_ and |dim| formatting.")

# Custom tokens
cli.setColorTokens({
    "*": "bold red",
    "#": "blue",
    "~": "green italic",
    "@": "cyan underline"
})

cli.echo("Now *red bold*, #blue#, ~green italic~ and @underlined@!")
```

## Language Detection and Translation

```python
# Automatic language detection and translation
cli.setup_language("Hola mundo")  # Detects Spanish and sets as target language

# Messages will now be automatically translated
cli.echo("Hello world!")  # Will output "Hola mundo!"

# Translate text manually
english_text = cli.translate("Bonjour le monde", target_lang="en", online=True)
print(english_text)  # "Hello world"
```

## Interactive Menus

```python
# Create a selection menu
choices = ["Option 1", "Option 2", "Option 3"]
selected = cli.select("Choose an option:", choices, default="Option 1")
cli.echo("You selected: *{option}*", option=selected)
```

## Command Line Applications

x_console integrates with rich_click for beautiful CLI applications:

```python
from x_console import CLIManager

cli = CLIManager()

@cli.command()
@cli.option("--name", "-n", help="Your name")
@cli.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def hello(name, verbose):
    """Say hello to someone."""
    if verbose:
        cli.debug_("Running with verbose mode")
    cli.echo("Hello, *{name}*!", name=name or "World")

if __name__ == "__main__":
    hello()
```

## Processing with Spinners

```python
import time

def long_process():
    for i in range(1, 11):
        # Simulate work
        time.sleep(0.5)
        # Yield status updates as (message_template, kwargs) tuples
        yield ("Step {step} of {total}...", {"step": i, "total": 10})
    
    # Final yield with completion message
    yield ("Process completed successfully!", {})

# Run the process with a spinner
cli.process(long_process, message="Running long process")
```

## Debug and Warning Messages

```python
# Enable debug mode
cli.debug = True

# Debug message (only shown when debug=True)
cli.debug_("Connected to {server} on port {port}", server="example.com", port=8080)

# Warning message (only shown when debug=True)
cli.warn_("Connection timeout after {seconds}s", seconds=30)

# Log messages (always shown)
cli.log("Application started")
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
