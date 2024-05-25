# translator.py
from deep_translator import GoogleTranslator as DeepGoogleTranslator
from lingua import Language, LanguageDetectorBuilder
from cache import Cache
import warnings

# Ignore all warnings from the huggingface_hub.file_download module
warnings.filterwarnings("ignore", module="huggingface_hub.file_download")

class TranslationService:
    def __init__(self, cache_dir=None, offline_model='opus-mt', cache_ttl=3600):
        self.translator_offline_model_name = offline_model
        self.translator_offline = None
        self.translator_online = DeepGoogleTranslator()
        self.cache = Cache(directory=cache_dir)
        self.cache_ttl = cache_ttl

    def _load_translator_offline(self):
        """Load the offline translator model only when needed."""
        if self.translator_offline is None:
            from easynmt import EasyNMT
            self.translator_offline = EasyNMT(self.translator_offline_model_name, device='cpu')

    def detect_language(self, text):
        languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
        detector = LanguageDetectorBuilder.from_languages(*languages).build()
        detected = detector.detect_language_of(text)
        return detected.iso_code_639_1.name.lower()

    def translate_offline(self, text, target_lang='en'):
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
            #print(f"!source language: {source_lang}, target language: {target_lang}")
            #print(f"!source text: {text}")
            #print(f"!offline translated text: {translation}")
            return translation
        except Exception as e:
            return text

    def translate_online(self, text, target_lang='en'):
        source_lang = self.detect_language(text)
        if source_lang == target_lang:
            return text
    
        cache_key = f"{source_lang}:{target_lang}:{text}"
        cached_translation = self.cache.get(cache_key)

        #if cached_translation:
        #    return cached_translation

        translation = self.translator_online.translate(text, source=source_lang, target=target_lang)
        self.cache.set(cache_key, translation, ttl=self.cache_ttl)
        #print(f"source language: {source_lang}, target language: {target_lang}")
        #print(f"source text: {text}")
        #print(f"online translated text: {translation}")
        return translation

    def translate(self, text, target_lang='en', online=True):
        if online:
            try:
                tmp = self.translate_online(text, target_lang)
                if tmp == text:
                    #print("Translating offline")
                    tmp2 = self.translate_offline(text, target_lang)
                    return tmp2
                #print("Translating online")
                return tmp
            except Exception:
                #print("Translating offline", Exception)
                return self.translate_offline(text, target_lang)
        else:
            #print("Translating offline OK")
            return self.translate_offline(text, target_lang)