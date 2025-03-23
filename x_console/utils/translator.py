# x_console/utils/translator.py

import warnings
import importlib.util
from .cache import Cache

# Ignore all warnings from the huggingface_hub.file_download module
warnings.filterwarnings("ignore", module="huggingface_hub.file_download")

# Check capabilities dynamically rather than importing from x_console
capabilities = {
    'language_detection': importlib.util.find_spec('lingua') is not None,
    'online_translation': importlib.util.find_spec('deep_translator') is not None,
    'offline_translation': importlib.util.find_spec('easynmt') is not None
}

if capabilities['language_detection']:
    from lingua import Language, LanguageDetectorBuilder

class TranslationService:
    def __init__(self, cache_dir=None, offline_model='opus-mt', cache_ttl=3600):
        self.translator_offline_model_name = offline_model
        self.translator_offline = None
        self.translator_online = None
        self.cache = Cache(directory=cache_dir)
        self.cache_ttl = cache_ttl
        
        if capabilities['online_translation']:
            try:
                from deep_translator import GoogleTranslator as DeepGoogleTranslator
                self.translator_online = DeepGoogleTranslator()
            except ImportError:
                pass
        
        if capabilities['offline_translation']:
            try:
                from easynmt import EasyNMT
                self.translator_offline = EasyNMT(self.translator_offline_model_name, device='cpu')
            except ImportError:
                pass

    def detect_language(self, text):
        if not capabilities['language_detection']:
            return 'en'  # Default to English if detection is not available

        try:
            languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
            detector = LanguageDetectorBuilder.from_languages(*languages).build()
            detected = detector.detect_language_of(text)
            return detected.iso_code_639_1.name.lower()
        except Exception:
            return 'en'  # Default to English if detection fails

    def translate_offline(self, text, target_lang='en'):
        if not capabilities['offline_translation'] or self.translator_offline is None:
            return text  # Return original text if offline translation is not available

        try:
            source_lang = self.detect_language(text)
            if source_lang == target_lang:
                return text
            
            cache_key = f"{source_lang}:{target_lang}:{text}"
            cached_translation = self.cache.get(cache_key)

            if cached_translation:
                return cached_translation

            translation = self.translator_offline.translate(text, source_lang=source_lang, target_lang=target_lang)
            self.cache.set(cache_key, translation, ttl=self.cache_ttl)
            return translation
        except Exception as e:
            return text

    def translate_online(self, text, target_lang='en'):
        if not capabilities['online_translation'] or self.translator_online is None:
            return text  # Return original text if online translation is not available

        try:
            source_lang = self.detect_language(text)
            if source_lang == target_lang:
                return text
        
            cache_key = f"{source_lang}:{target_lang}:{text}"
            cached_translation = self.cache.get(cache_key)

            if cached_translation:
                return cached_translation

            translation = self.translator_online.translate(text, source=source_lang, target=target_lang)
            self.cache.set(cache_key, translation, ttl=self.cache_ttl)
            return translation
        except Exception:
            return text

    def translate(self, text, target_lang='en', online=True):
        # Try online translation if requested and available
        if online and capabilities['online_translation'] and self.translator_online is not None:
            try:
                return self.translate_online(text, target_lang)
            except Exception:
                pass
                
        # Try offline translation if available
        if capabilities['offline_translation'] and self.translator_offline is not None:
            try:
                return self.translate_offline(text, target_lang)
            except Exception:
                pass
                
        # Return original text if neither translation method is available or if they fail
        return text
