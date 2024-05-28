from .cli_manager import CLIManager

capabilities = {
    'online_translation': False,
    'offline_translation': False,
    'language_detection': False
}

try:
    from deep_translator import GoogleTranslator
    from lingua import Language, LanguageDetectorBuilder
    capabilities['online_translation'] = True
except ImportError:
    pass

try:
    from easynmt import EasyNMT
    from lingua import Language, LanguageDetectorBuilder
    capabilities['offline_translation'] = True
except ImportError:
    pass

try:
    from lingua import Language, LanguageDetectorBuilder
    capabilities['language_detection'] = True
except ImportError:
    pass

init = CLIManager
__all__ = ['CLIManager', 'capabilities']
