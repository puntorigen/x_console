import os, sys, time, re
import rich_click as click
#import logging
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from simple_term_menu import TerminalMenu
#from rich.logging import RichHandler
from yaspin import yaspin, Spinner
from utils.localizer import Localizer
from utils.translator import TranslationService

# setup logging
#FORMAT = "%(message)s"
#logging.basicConfig(
#    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
#)
#log = logging.getLogger("rich")

class CLIManager:
    def __init__(self, debug=True, debug_prefix="DEBUG", domain="cli", locales_dir=None, output_language=None, color_tokens={}, spinner=["⭐", "✨", "🌟", "🚀"]):
        self.configure_rich_click()
        self.debug = debug
        self.debug_prefix = debug_prefix
        self.domain = domain
        self.target_lang = "en"
        self.console = Console()
        if locales_dir is None:
            locales_dir = os.path.join(os.path.dirname(__file__), "translations")
        self.localizer = Localizer(locale_path=locales_dir, domain=domain, target_lang=self.target_lang, online=True)
        self.translator = TranslationService()
        self.input_text_english = ""
        if color_tokens:
            self.color_mapping = color_tokens
        else:
            self.color_mapping = {
                "*": "yellow",
                "_": "i",
                "|": "dim"
            }
        self._ = self.localizer._
        self.spinner = Spinner(spinner, 200)
        if output_language:
            self.setup_language(language=output_language)

    def configure_rich_click(self):
        """Configure rich_click with all necessary styles and settings."""
        click.rich_click.USE_RICH_MARKUP = True
        click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
        click.rich_click.ERRORS_SUGGESTION = "Try running the '--help' flag for more information."
        #click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://www.puntorigen.com/m]https://www.puntorigen.com/m[/link]"
        #click.rich_click.SHOW_ARGUMENTS = True
        #click.rich_click.STYLE_OPTIONS_TABLE_LEADING = 1
        #click.rich_click.STYLE_OPTIONS_TABLE_BOX = "SIMPLE"
        click.rich_click.STYLE_OPTIONS_TABLE_ROW_STYLES = ["bold", ""]
        click.rich_click.STYLE_COMMANDS_TABLE_SHOW_LINES = True
        click.rich_click.STYLE_COMMANDS_TABLE_PAD_EDGE = True
        click.rich_click.STYLE_COMMANDS_TABLE_BOX = "DOUBLE"
        click.rich_click.STYLE_COMMANDS_TABLE_BORDER_STYLE = "red"
        click.rich_click.STYLE_COMMANDS_TABLE_ROW_STYLES = ["magenta", "yellow", "cyan", "green"]

    def setColorTokens(self, token_colors):
        """Set the token to color mappings."""
        self.color_mapping = token_colors

    def apply_color(self, text):
        """Wrap tokens with rich color tags based on the mappings."""
        for token, color in self.color_mapping.items():
            # Create a regex pattern that matches pairs of the token with at least one non-token character between them
            pattern = re.compile(f'\\{token}([^\\{token}]+)\\{token}')
            # Replace each found pair with Rich formatted color tags
            text = pattern.sub(f'[{color}]\\1[/]', text)
        return text 

    def echo(self, text, *args, **kwargs):
        """Echo messages with translation and formatting."""
        # Translates the text and uses args and kwargs for formatting
        translated_text = self._(text, *args, **kwargs)
        # Apply color formatting
        formatted_text = self.apply_color(translated_text)
        # Print the formatted text with 'Rich' support
        print(formatted_text)

    def echoDim(self, text, *args, **kwargs):
        """Echo messages with translation and formatting in dim color."""
        # Translates the text and uses args and kwargs for formatting
        translated_text = self._(text, *args, **kwargs)
        # Apply color formatting
        formatted_text = self.apply_color(translated_text)
        # Print the formatted text with 'Rich' support
        print("[dim]"+formatted_text+"[/]")

    def prompt(self, text, *args, **kwargs):
        """Prompt a question to the user with formatting support."""
        translated_text = text
        # check if text is a string or a tuple
        if isinstance(text, str):
            # Translates the text to the user lang
            translated_text = self._(text)
        elif isinstance(text, tuple):
            template, kw = text
            # Translates the tuple text with (kwargs) into the user lang
            translated_text = self._(template, **kw)
        # Apply color formatting
        formatted_text = self.apply_color(translated_text)
        # Prompts the formatted text with 'Rich' support
        return Prompt.ask(formatted_text, *args, **kwargs)

    def select(self, text, choices: list[str], default):
        """Prompt a question to the user with choices and formatting support."""
        # uses rich prompt
        translated_text = text
        # check if text is a string or a tuple
        if isinstance(text, str):
            # Translates the text to the user lang
            translated_text = self._(text)
        elif isinstance(text, tuple):
            template, kw = text
            # Translates the tuple text with (kwargs) into the user lang
            translated_text = self._(template, **kw)
        # Apply color formatting
        formatted_text = self.apply_color(translated_text)

        # Translate the choices and map them back to the original choices
        translated_choices = [self._(choice) for choice in choices]
        choice_map = {translated: original for translated, original in zip(translated_choices, choices)}

        # Display the prompt with translated choices using rich
        #translated_default = self._(default)
        #selected_translated_choice = Prompt.ask(formatted_text, choices=translated_choices, default=translated_default)
        selected_translated_choice = TerminalMenu(translated_choices, title=formatted_text)
        selected_translated_choice.show()

        # Map the selected translated choice back to the original choice
        return choice_map[selected_translated_choice.chosen_menu_entry]

    def Choice(self, *args, **kwargs):
        click.Choice(*args, **kwargs)
    
    def debug_(self, text, *args, **kwargs):
        """Echo debug messages with formatting."""
        # Apply color formatting
        formatted_text = self.apply_color(text)
        if not self.debug:
            return
        formatted_text = f"[green][dim]{self.domain}:{self.debug_prefix}: [blue]{formatted_text.format(*args, **kwargs)}[/][/]"
        # Print the formatted text with 'Rich' support
        print(formatted_text)

    def warn_(self, text, *args, **kwargs):
        """Echo warning messages with formatting."""
        # Apply color formatting
        formatted_text = self.apply_color(text)
        if not self.debug:
            return
        formatted_text = f"[red][dim]{self.domain}:WARN:[/] [red]{formatted_text.format(*args, **kwargs)}[/][/]"
        # Print the formatted text with 'Rich' support
        print(formatted_text)

    def translate(self, text, target_lang="en", online=True):
        """Translate text (to english) using the shared TranslationService."""
        target_lang = target_lang if target_lang else self.target_lang
        detected_lang = self.translator.detect_language(text)
        if target_lang != detected_lang:
            return self.translator.translate(text, target_lang=target_lang, online=online)
        return text
    
    def log(self, message, *args, **kwargs):
        """Log messages with translation and formatting."""
        colored = self.apply_color(message)
        self.console.log(colored, emoji=True, *args, **kwargs)

    def process(self, task, message="Processing", *args, **kwargs):
        """
        Process function with spinner and dynamic progress updates.
        The task should be a generator that yields messages indicating progress.
        """
        message_ = self._(message, **kwargs)
        def colorize(text):
            formatted_text = self.apply_color(text)
            with self.console.capture() as capture:
                self.console.print(formatted_text, end="")
            return capture.get().strip()
            
        with yaspin(self.spinner, text=message_) as spinner:
            try:
                for template, kwargs in task():
                    translated_update = self._(template, **kwargs)
                    spinner.text = colorize(translated_update)
                    time.sleep(0.1)  # Simulate time delay for demonstration
                spinner.text = ""
                spinner.ok(colorize("[green]✔[/] "+self._("Done")))
            except Exception as e:
                #spinner.text = ""
                spinner.fail(colorize("[red]✖[/] "+self._("Error")))
                self.console.print_exception(show_locals=True)
                #self.echo("An error occurred: {e}",e=str(e))

    def setup_language(self, input_text="", language=None):
        """Detect and set language for output based on input or specified language."""
        if language:
            self.target_lang = language
        else:
            detected_lang = self.translator.detect_language(input_text).lower()
            self.target_lang = detected_lang
            self.input_text_english = input_text
            if detected_lang != "en":
                self.input_text_english = self.translate(input_text)
                self.debug_("Input text in _English_: {input}",input=self.input_text_english)
        self.localizer.target_lang = self.target_lang
        self.debug_("Output language set to: _{lang}_",lang=self.target_lang)

    def command(self, *args, **kwargs):
        """Decorator to wrap rich_click command."""
        return click.command(*args, **kwargs)

    def option(self, *args, **kwargs):
        """Decorator to wrap rich_click option."""
        return click.option(*args, **kwargs)

    def argument(self, *args, **kwargs):
        """Decorator to wrap rich_click argument."""
        return click.argument(*args, **kwargs)
