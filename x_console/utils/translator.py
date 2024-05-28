# x_console/utils/translator.py

import warnings
from x_console import capabilities
from cache import Cache

# Ignore all warnings from the huggingface_hub.file_download module
warnings.filterwarnings("ignore", module="huggingface_hub.file_download")

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
            from deep_translator import GoogleTranslator as DeepGoogleTranslator
            self.translator_online = DeepGoogleTranslator()
        
        if capabilities['offline_translation']:
            self._load_translator_offline()

    def _load_translator_offline(self):
        """Load the offline translator model only when needed."""
        if self.translator_offline is None:
            from easynmt import EasyNMT
            self.translator_offline = EasyNMT(self.translator_offline_model_name, device='cpu')

    def detect_language(self, text):
        if not capabilities['language_detection']:
            raise RuntimeError("Language detection capability is not available")

        languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
        detector = LanguageDetectorBuilder.from_languages(*languages).build()
        detected = detector.detect_language_of(text)
        return detected.iso_code_639_1.name.lower()

    def translate_offline(self, text, target_lang='en'):
        if not capabilities['offline_translation']:
            raise RuntimeError("Offline translation capability is not available")

        try:
            self._load_translator_offline()
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
        if not capabilities['online_translation']:
            raise RuntimeError("Online translation capability is not available")

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

    def translate(self, text, target_lang='en', online=True):
        if online and capabilities['online_translation']:
            try:
                translation = self.translate_online(text, target_lang)
                if translation == text:
                    return self.translate_offline(text, target_lang)
                return translation
            except Exception:
                return self.translate_offline(text, target_lang)
        elif capabilities['offline_translation']:
            return self.translate_offline(text, target_lang)
        return text
