from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests
import json
from openai import OpenAI
import pycountry
from langdetect import detect, LangDetectException
from gtts import gTTS
import io
import speech_recognition as sr
import threading
import time

class EnhancedAgriAssistant:
    def __init__(self, api_key, base_url):
        """
        Initialize the enhanced agricultural assistant
        
        Args:
            api_key (str): Your API key
            base_url (str): API base URL
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.conversation_history = []
        self.current_language = 'en'
        self.voice_enabled = True
        self.reset_conversation()
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = [
            {"role": "system", "content": self._get_system_message()}
        ]
    
    def _get_system_message(self):
        """Get system message based on current language"""
        messages = {
            'en': "You are an expert agricultural assistant helping Indian farmers. Provide practical, actionable advice. Be friendly and supportive.",
            'hi': "आप एक विशेषज्ञ कृषि सहायक हैं जो भारतीय किसानों की मदद करते हैं। व्यावहारिक और कार्यान्वयन योग्य सलाह दें। दोस्ताना और सहायक बनें।",
            'ta': "நீங்கள் இந்திய விவசாயிகளுக்கு உதவும் நிபுணர் விவசாய உதவியாளர். நடைமுறை, செயல்படுத்தக்கூடிய ஆலோசனையை வழங்குங்கள். நட்பு மற்றும் ஆதரவு அளிக்குங்கள்.",
            'te': "మీరు భారతీయ రైతులకు సహాయపడే నిపుణుడు వ్యవసాయ సహాయకుడు. ఆచరణాత్మక, చర్య తీసుకోదగిన సలహాలను అందించండి. స్నేహపూర్వకంగా మరియు సహాయకంగా ఉండండి.",
            'bn': "আপনি একজন বিশেষজ্ঞ কৃষি সহকারী যিনি ভারতীয় কৃষকদের সাহায্য করেন। ব্যবহারিক, কার্যকরী পরামর্শ দিন। বন্ধুত্বপূর্ণ এবং সহায়ক হন।",
            'mr': "तुम्ही भारतीय शेतकऱ्यांना मदत करणारे तज्ज्ञ शेती सहाय्यक आहात. व्यावहारिक, कृती करण्यायोग्य सल्ला द्या. मैत्रीपूर्ण आणि सहाय्यक व्हा.",
            'gu': "તમે ભારતીય ખેડૂતોને મદદ કરતા નિષ્ણાત કૃષિ સહાયક છો. વ્યવહારિક, કાર્યવાહક સલાહ આપો. મૈત્રીપૂર્ણ અને સહાયક રહો.",
            'kn': "ನೀವು ಭಾರತೀಯ ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡುವ ಪರಿಣತ ಕೃಷಿ ಸಹಾಯಕ. ಪ್ರಾಯೋಗಿಕ, ಕ್ರಿಯಾತ್ಮಕ ಸಲಹೆ ನೀಡಿ. ಸ್ನೇಹಪೂರ್ವಕ ಮತ್ತು ಸಹಾಯಕರಾಗಿರಿ.",
            'ml': "നിങ്ങൾ ഇന്ത്യൻ കർഷകർക്ക് സഹായിക്കുന്ന വിദഗ്ധ കാർഷിക സഹായിയാണ്. പ്രായോഗിക, പ്രവർത്തനക്ഷമമായ ഉപദേശം നൽകുക. സൗഹൃദപരവും സഹായകരവുമായിരിക്കുക.",
            'pa': "ਤੁਸੀਂ ਭਾਰਤੀ ਕਿਸਾਨਾਂ ਦੀ ਮਦਦ ਕਰਨ ਵਾਲੇ ਮਾਹਿਰ ਖੇਤੀਬਾੜੀ ਸਹਾਇਕ ਹੋ। ਵਿਹਾਰਕ, ਕਾਰਜਸ਼ੀਲ ਸਲਾਹ ਦਿਓ। ਦੋਸਤਾਨਾ ਅਤੇ ਸਹਾਇਕ ਰਹੋ।",
            'ur': "آپ بھارتی کسانوں کی مدد کرنے والے ماہر زرعی معاون ہیں۔ عملی، قابل عمل مشورہ دیں۔ دوستانہ اور مددگار رہیں۔"
        }
        return messages.get(self.current_language, messages['en'])
    
    def set_language(self, language_code):
        """Set the preferred language for responses"""
        self.current_language = language_code
        self.reset_conversation()
        return self._get_language_name(language_code)
    
    def detect_language(self, text):
        """Detect the language of input text"""
        try:
            lang_code = detect(text)
            return lang_code
        except LangDetectException:
            return 'en'
    
    def _get_language_name(self, lang_code):
        """Get language name from code"""
        try:
            language = pycountry.languages.get(alpha_2=lang_code)
            return language.name if language else f"Unknown ({lang_code})"
        except:
            return f"Unknown ({lang_code})"
    
    def generate_response(self, user_input, force_language=None):
        """Generate AI response with multilingual support"""
        # Detect input language
        input_lang = self.detect_language(user_input)
        input_lang_name = self._get_language_name(input_lang)
        
        # Determine response language
        response_lang = force_language if force_language else self.current_language
        response_lang_name = self._get_language_name(response_lang)
        
        # Add user message to conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Generate response
            response = self.client.chat.completions.create(
                model="dhenu2-in-8b-preview",
                messages=self.conversation_history,
                max_tokens=800,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content.strip()
            
            # Translate if needed
            if response_lang != input_lang:
                assistant_response = self._translate_text(assistant_response, response_lang)
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return {
                "response": assistant_response,
                "input_language": input_lang_name,
                "response_language": response_lang_name,
                "input_lang_code": input_lang,
                "response_lang_code": response_lang,
                "confidence": 0.95
            }
            
        except Exception as e:
            # Log the detailed error server-side, but return a clean message to the user
            print(f"AI generate_response error: {e}")
            return {
                "response": "Sorry, I'm having trouble reaching the AI service right now. Please try again in a moment.",
                "input_language": input_lang_name,
                "response_language": "English",
                "input_lang_code": input_lang,
                "response_lang_code": "en",
                "confidence": 0.0
            }
    
    def _translate_text(self, text, target_lang):
        """Translate text to target language"""
        try:
            lang_name = self._get_language_name(target_lang)
            prompt = f"Translate the following text to {lang_name}: {text}"
            
            response = self.client.chat.completions.create(
                model="dhenu2-in-8b-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def get_voice_response(self, text, language_code):
        """Generate voice response using ElevenLabs TTS with gTTS fallback"""
        # Try ElevenLabs first
        try:
            api_key = getattr(settings, 'ELEVENLABS_API_KEY', None)
            voice_id = getattr(settings, 'ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
            if api_key:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                headers = {
                    'xi-api-key': api_key,
                    'Content-Type': 'application/json'
                }
                payload = {
                    'text': text,
                    'model_id': 'eleven_multilingual_v2',
                    'voice_settings': {
                        'stability': 0.4,
                        'similarity_boost': 0.7
                    }
                }
                r = requests.post(url, headers=headers, json=payload, timeout=30)
                if r.status_code == 200:
                    return r.content
                else:
                    print(f"ElevenLabs TTS error {r.status_code}: {r.text}")
        except Exception as e:
            print(f"ElevenLabs TTS exception: {e}")
        
        # Fallback to gTTS
        try:
            tts = gTTS(text=text, lang=language_code, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()
        except Exception as e:
            print(f"gTTS error: {e}")
            return None

# Global assistant instance
assistant_instance = None

def get_assistant():
    """Get or create the global assistant instance"""
    global assistant_instance
    if assistant_instance is None:
        assistant_instance = EnhancedAgriAssistant(
            api_key="dh-Y8AQ9LD4qyPk61FKtSW1zTFx8ag49oVEeHR1uebn4aM",
            base_url="https://api.dhenu.ai/v1"
        )
    return assistant_instance

@login_required
def unified_assistant(request):
    """Unified voice assistant and chatbot interface"""
    return render(request, 'voice/unified_assistant.html')

@login_required
def chat_with_ai(request):
    """Handle AI conversations with enhanced multilingual support"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            language = data.get('language') or data.get('target_language')
            voice_enabled = data.get('voice_enabled', False)

            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)

            assistant = get_assistant()

            lower_msg = message.lower()
            if lower_msg.startswith('set language '):
                lang_code = message.split(' ')[-1].strip()
                lang_name = assistant.set_language(lang_code)
                response_text = f'Language set to {lang_name}. I will now respond in this language.'
                return JsonResponse({
                    'response': response_text,
                    'language_info': {
                        'input_language': 'English',
                        'response_language': lang_name,
                        'input_lang_code': 'en',
                        'response_lang_code': lang_code
                    },
                    'command_type': 'language_set'
                })

            if lower_msg in ['reset', 'clear', 'new conversation']:
                assistant.reset_conversation()
                response_text = 'Conversation reset. How can I help you with agriculture today?'
                return JsonResponse({
                    'response': response_text,
                    'language_info': {
                        'input_language': 'English',
                        'response_language': assistant._get_language_name(assistant.current_language),
                        'input_lang_code': 'en',
                        'response_lang_code': assistant.current_language
                    },
                    'command_type': 'reset'
                })

            response_data = assistant.generate_response(message, language)

            suggestions = {
                'weather': '💡 Check real-time weather data in the Weather section.',
                'crop': '💡 Get detailed crop recommendations in the Crop Recommendations section.',
                'soil': '💡 Analyze your soil in the Soil Test section.',
                'scheme': '💡 Find government schemes in the Government Schemes section.',
                'pesticide': '💡 Browse pesticides in the Pesticides Guide section.',
                'export': '💡 Check export opportunities in the Exports section.',
                'disease': '💡 Get disease management advice in the Pesticides section.',
                'fertilizer': '💡 Learn about soil fertility in the Soil Test section.'
            }

            additional_info = ""
            for keyword, suggestion in suggestions.items():
                if keyword in lower_msg:
                    additional_info = f"\n\n{suggestion}"
                    break

            response_text = response_data['response'] + additional_info

            return JsonResponse({
                'response': response_text,
                'language_info': {
                    'input_language': response_data['input_language'],
                    'response_language': response_data['response_language'],
                    'input_lang_code': response_data['input_lang_code'],
                    'response_lang_code': response_data['response_lang_code']
                },
                'confidence': response_data['confidence'],
                'command_type': 'ai_response'
            })

        except Exception as e:
            print(f"AI Assistant Error: {e}")
            return JsonResponse({
                'response': 'I apologize, but I\'m having trouble processing your request right now. Please try again in a moment.',
                'error': str(e)
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_supported_languages(request):
    """Get list of supported languages"""
    languages = [
        {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
        {'code': 'hi', 'name': 'Hindi', 'flag': '🇮🇳'},
        {'code': 'ta', 'name': 'Tamil', 'flag': '🇮🇳'},
        {'code': 'te', 'name': 'Telugu', 'flag': '🇮🇳'},
        {'code': 'bn', 'name': 'Bengali', 'flag': '🇮🇳'},
        {'code': 'mr', 'name': 'Marathi', 'flag': '🇮🇳'},
        {'code': 'gu', 'name': 'Gujarati', 'flag': '🇮🇳'},
        {'code': 'kn', 'name': 'Kannada', 'flag': '🇮🇳'},
        {'code': 'ml', 'name': 'Malayalam', 'flag': '🇮🇳'},
        {'code': 'pa', 'name': 'Punjabi', 'flag': '🇮🇳'},
        {'code': 'ur', 'name': 'Urdu', 'flag': '🇮🇳'},
        {'code': 'es', 'name': 'Spanish', 'flag': '🇪🇸'},
        {'code': 'fr', 'name': 'French', 'flag': '🇫🇷'},
        {'code': 'de', 'name': 'German', 'flag': '🇩🇪'},
        {'code': 'it', 'name': 'Italian', 'flag': '🇮🇹'},
        {'code': 'pt', 'name': 'Portuguese', 'flag': '🇵🇹'},
        {'code': 'ru', 'name': 'Russian', 'flag': '🇷🇺'},
        {'code': 'zh', 'name': 'Chinese', 'flag': '🇨🇳'},
        {'code': 'ja', 'name': 'Japanese', 'flag': '🇯🇵'},
        {'code': 'ko', 'name': 'Korean', 'flag': '🇰🇷'},
        {'code': 'ar', 'name': 'Arabic', 'flag': '🇸🇦'}
    ]
    return JsonResponse({'languages': languages})

@login_required
def process_voice_input(request):
    """Process voice input and return text"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            audio_data = data.get('audio')
            language = data.get('language', 'en-IN')

            # No server-side STT implemented; return benign success so UI can silently continue
            return JsonResponse({
                'text': '',
                'note': 'stt_unavailable'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_voice_response(request):
    """Generate voice response for text"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            language = data.get('language', 'en')
            
            if not text:
                return JsonResponse({'error': 'Text is required'}, status=400)
            
            assistant = get_assistant()
            voice_data = assistant.get_voice_response(text, language)
            
            if voice_data:
                return HttpResponse(voice_data, content_type='audio/mpeg')
            else:
                return JsonResponse({'error': 'Failed to generate voice'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_assistant_status(request):
    """Get current assistant status and settings"""
    assistant = get_assistant()
    return JsonResponse({
        'current_language': assistant.current_language,
        'language_name': assistant._get_language_name(assistant.current_language),
        'voice_enabled': assistant.voice_enabled,
        'conversation_length': len(assistant.conversation_history) - 1  # Exclude system message
    })

@login_required
def get_quick_commands(request):
    """Get list of quick commands for users"""
    commands = [
        {
            'category': 'Weather & Climate',
            'commands': [
                'What\'s the weather like today?',
                'Show me the 7-day forecast',
                'Is it good weather for planting?',
                'When will the monsoon arrive?'
            ]
        },
        {
            'category': 'Crop Management',
            'commands': [
                'What crops should I plant this season?',
                'How to treat crop diseases?',
                'Best time to harvest wheat',
                'Organic pest control methods'
            ]
        },
        {
            'category': 'Soil & Fertilizer',
            'commands': [
                'How to improve soil fertility?',
                'What fertilizer should I use?',
                'Soil testing methods',
                'Natural soil enrichment'
            ]
        },
        {
            'category': 'Government Support',
            'commands': [
                'Available government schemes',
                'Subsidy information for farmers',
                'Loan facilities for agriculture',
                'Insurance schemes for crops'
            ]
        }
    ]
    return JsonResponse({'commands': commands})

# Legacy views for backward compatibility
@login_required
def voice_assistant(request):
    """Legacy voice assistant view - redirects to unified interface"""
    return render(request, 'voice/unified_assistant.html')

@login_required
def chatbot(request):
    """Legacy chatbot view - redirects to unified interface"""
    return render(request, 'voice/unified_assistant.html')

