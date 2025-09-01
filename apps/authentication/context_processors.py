from .translations import get_translation, translate_text

def site_language(request):
    lang = request.session.get('site_lang') or request.COOKIES.get('site_lang') or 'en'
    
    def t(key):
        """Template function to get translation"""
        return get_translation(key, lang)
    
    def translate(text):
        """Template function to translate text"""
        return translate_text(text, lang)
    
    return {
        'site_lang': lang,
        't': t,
        'translate': translate
    }
