# localizer.py
import os, polib, gettext
from translator import TranslationService

class Localizer:
    def __init__(self, locale_path='translations', domain='messages', cache_dir=None, cache_ttl=3600, target_lang='en', online=True):
        self.locale_path = locale_path
        self.domain = domain
        self.translator = TranslationService(cache_dir=cache_dir, cache_ttl=cache_ttl)
        self.target_lang = target_lang
        self.online = online

        # Configure gettext
        gettext.bindtextdomain(domain, locale_path)
        gettext.textdomain(domain)

    def translate(self, text):
        """Translate the given text using gettext with fallback translation."""
        #translated_text = gettext.gettext(text)f
        translated_text = self.searchTranslation(text)
        #print(f"Translated text: {translated_text}",text)

        if not translated_text or translated_text == text: # No translation found in .mo files
            #print(f"Translating text: {text} to '{self.target_lang}'")
            translated_text = self.translator.translate(text, target_lang=self.target_lang, online=self.online)
            #print(f"!!Translated text: {translated_text}")
            translation_method = "Online" if self.online else "Offline"
            self.update_po_file(text, translated_text, self.target_lang, translation_method)

        return translated_text

    def _(self, text, *args, **kwargs):
        """Format the translated string with dynamic parameters, keeping placeholders intact."""
        if not args and not kwargs:
            # Translate the modified text
            return self.translate(text)
        
        # Temporarily replace placeholders with unique identifiers
        temp_text, unique_to_placeholder = self._replace_placeholders_with_unique(text, **kwargs)
        
        # Translate the modified text
        translated_temp_text = self.translate(temp_text)
        
        # Restore original placeholders
        translated_text = self._restore_placeholders(translated_temp_text, unique_to_placeholder)
        
        return translated_text.format(*args, **kwargs)

    def _replace_placeholders_with_unique(self, text, **kwargs):
        """Replace placeholders with unique identifiers."""
        unique_to_placeholder = {}
        for i, placeholder in enumerate(kwargs.keys()):
            #unique_key = f'_PLACEHOLDER_{i}_'
            unique_key = f'{{v{i}}}'
            text = text.replace(f'{{{placeholder}}}', unique_key)
            unique_to_placeholder[unique_key] = f'{{{placeholder}}}'
        return text, unique_to_placeholder

    def _restore_placeholders(self, text, unique_to_placeholder):
        """Restore unique identifiers back to original placeholders."""
        for unique_key, placeholder in unique_to_placeholder.items():
            text = text.replace(unique_key, placeholder)
        return text

    def searchTranslation(self, text):
        """Search for a translation in the .po file."""
        po_dir = os.path.join(self.locale_path, self.target_lang, 'LC_MESSAGES')
        po_file_path = os.path.join(po_dir, f'{self.domain}.po')

        if os.path.exists(po_file_path):
            po = polib.pofile(po_file_path)
            entry = po.find(text)
            if entry:
                return entry.msgstr
        return None

    def update_po_file(self, original_text, translation, target_lang, method):
        """Update the .po file with the original placeholders intact."""
        po_dir = os.path.join(self.locale_path, target_lang, 'LC_MESSAGES')
        po_file_path = os.path.join(po_dir, f'{self.domain}.po')
        #mo_file_path = os.path.join(po_dir, f'{self.domain}.mo')

        # Ensure the directory exists
        os.makedirs(po_dir, exist_ok=True)

        try:
            # Load or create the .po file
            if os.path.exists(po_file_path):
                po = polib.pofile(po_file_path)
            else:
                po = polib.POFile()
                po.metadata = {
                    'Project-Id-Version': '1.0',
                    'Report-Msgid-Bugs-To': '',
                    'POT-Creation-Date': '',
                    'PO-Revision-Date': '',
                    'Last-Translator': '',
                    'Language-Team': '',
                    'MIME-Version': '1.0',
                    'Content-Type': 'text/plain; charset=UTF-8',
                    'Content-Transfer-Encoding': '8bit',
                    'Language': target_lang,
                }

            # Find or create the entry
            entry = po.find(original_text)
            if entry is None:
                entry = polib.POEntry(msgid=original_text, msgstr=translation)
                po.append(entry)
            else:
                entry.msgstr = translation

            # Add translation method as a comment
            entry.comment = f'Translated using {method} translation.'

            # Save the updated .po file
            po.save(po_file_path)

            # Compile to .mo file
            #po.save_as_mofile(mo_file_path)

        except Exception as e:
            print(f"Error updating .po or .mo files: {e}")
