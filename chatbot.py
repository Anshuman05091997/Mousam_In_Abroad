import re
from datetime import datetime
from typing import Dict, List, Optional

class Chatbot:
    def __init__(self):
        self.languages = {
            'en': 'english',
            'hi': 'hindi',
            'de': 'german'
        }
        self.current_language = 'en'  # Default language
        self.responses = {
            'en': {  # English responses
                'greeting': [
                    'Hello! Welcome to Mousam In Abroad. How can I help you with your Germany study journey?',
                    'Hi there! I\'m here to help you with information about studying in Germany. What would you like to know?',
                    'Welcome! I can help you with university applications, visa processes, and more. What\'s on your mind?'
                ],
                'university': [
                    'Germany has excellent universities! Popular choices include TU Munich, RWTH Aachen, and Heidelberg University. What\'s your field of study?',
                    'German universities are known for their quality education and low tuition fees. Most public universities charge only a small semester fee.',
                    'To apply to German universities, you\'ll need your academic transcripts, language certificates (German/English), and sometimes an APS certificate.'
                ],
                'visa': [
                    'For a student visa, you\'ll need: university admission letter, proof of financial resources, health insurance, and APS certificate (for Indian students).',
                    'The visa process typically takes 4-8 weeks. Make sure to apply well in advance of your intended start date.',
                    'You\'ll need to show proof of €11,208 per year in a blocked account for living expenses.'
                ],
                'language_switch': [
                    'Switched to English! How can I help you?'
                ],
                'fallback': [
                    'I\'m not sure about that specific question. Would you like to book a free consultation with our experts?',
                    'That\'s a great question! Our team can provide detailed guidance. Would you like to schedule a call?',
                    'For specific advice, I recommend booking a consultation with us. We can help you with personalized guidance.'
                ]
            },
            'hi': {  # Hindi responses
                'greeting': [
                    'नमस्ते! मौसम इन अब्रॉड में आपका स्वागत है। मैं आपकी जर्मनी में पढ़ाई की यात्रा में कैसे मदद कर सकता हूं?',
                    'नमस्कार! मैं जर्मनी में पढ़ाई के बारे में जानकारी देने के लिए यहां हूं। आप क्या जानना चाहेंगे?',
                    'स्वागत है! मैं यूनिवर्सिटी आवेदन, वीजा प्रक्रिया और बहुत कुछ में आपकी मदद कर सकता हूं। आप क्या जानना चाहते हैं?'
                ],
                'university': [
                    'जर्मनी में उत्कृष्ट विश्वविद्यालय हैं! लोकप्रिय विकल्पों में TU Munich, RWTH Aachen, और Heidelberg University शामिल हैं। आपका अध्ययन क्षेत्र क्या है?',
                    'जर्मन विश्वविद्यालय अपनी गुणवत्तापूर्ण शिक्षा और कम ट्यूशन फीस के लिए जाने जाते हैं। अधिकांश सार्वजनिक विश्वविद्यालय केवल एक छोटी सी सेमेस्टर फीस लेते हैं।',
                    'जर्मन विश्वविद्यालयों में आवेदन करने के लिए, आपको अपनी शैक्षणिक ट्रांसक्रिप्ट, भाषा प्रमाणपत्र (जर्मन/अंग्रेजी), और कभी-कभी APS प्रमाणपत्र की आवश्यकता होगी।'
                ],
                'visa': [
                    'स्टूडेंट वीजा के लिए, आपको आवश्यकता होगी: विश्वविद्यालय प्रवेश पत्र, वित्तीय संसाधनों का प्रमाण, स्वास्थ्य बीमा, और भारतीय छात्रों के लिए APS प्रमाणपत्र।',
                    'वीजा प्रक्रिया में आमतौर पर 4-8 सप्ताह लगते हैं। अपनी इच्छित शुरुआती तिथि से काफी पहले आवेदन करें।',
                    'आपको जीवन यापन खर्च के लिए एक ब्लॉक्ड अकाउंट में €11,208 प्रति वर्ष का प्रमाण दिखाना होगा।'
                ],
                'language_switch': [
                    'हिंदी में स्विच कर दिया गया है! मैं आपकी कैसे मदद कर सकता हूं?'
                ],
                'fallback': [
                    'मुझे इस विशिष्ट प्रश्न के बारे में पता नहीं है। क्या आप हमारे विशेषज्ञों के साथ एक मुफ्त परामर्श बुक करना चाहेंगे?',
                    'यह एक बढ़िया सवाल है! हमारी टीम विस्तृत मार्गदर्शन प्रदान कर सकती है। क्या आप एक कॉल शेड्यूल करना चाहेंगे?',
                    'विशिष्ट सलाह के लिए, मैं आपको हमारे साथ परामर्श बुक करने की सलाह देता हूं। हम आपको व्यक्तिगत मार्गदर्शन प्रदान कर सकते हैं।'
                ]
            },
            'de': {  # German responses
                'greeting': [
                    'Hallo! Willkommen bei Mousam In Abroad. Wie kann ich Ihnen bei Ihrem Studium in Deutschland helfen?',
                    'Hallo! Ich bin hier, um Ihnen Informationen über das Studium in Deutschland zu geben. Was möchten Sie wissen?',
                    'Willkommen! Ich kann Ihnen bei Universitätsbewerbungen, Visumsprozessen und mehr helfen. Was beschäftigt Sie?'
                ],
                'university': [
                    'Deutschland hat ausgezeichnete Universitäten! Beliebte Optionen sind TU München, RWTH Aachen und Universität Heidelberg. Was ist Ihr Studienfach?',
                    'Deutsche Universitäten sind bekannt für ihre Qualitätsausbildung und niedrigen Studiengebühren. Die meisten öffentlichen Universitäten erheben nur einen kleinen Semesterbeitrag.',
                    'Für die Bewerbung an deutschen Universitäten benötigen Sie Ihre akademischen Zeugnisse, Sprachzertifikate (Deutsch/Englisch) und manchmal ein APS-Zertifikat.'
                ],
                'visa': [
                    'Für ein Studentenvisum benötigen Sie: Zulassungsbescheid der Universität, Nachweis der finanziellen Mittel, Krankenversicherung und APS-Zertifikat (für indische Studenten).',
                    'Der Visumsprozess dauert typischerweise 4-8 Wochen. Bewerben Sie sich rechtzeitig vor Ihrem geplanten Studienbeginn.',
                    'Sie müssen einen Nachweis über €11.208 pro Jahr auf einem Sperrkonto vorlegen.'
                ],
                'language_switch': [
                    'Auf Deutsch umgestellt! Wie kann ich Ihnen helfen?'
                ],
                'fallback': [
                    'Ich bin mir bei dieser speziellen Frage nicht sicher. Möchten Sie eine kostenlose Beratung mit unseren Experten buchen?',
                    'Das ist eine gute Frage! Unser Team kann Ihnen detaillierte Beratung geben. Möchten Sie einen Termin vereinbaren?',
                    'Für spezifische Beratung empfehle ich Ihnen, eine Beratung bei uns zu buchen. Wir können Ihnen persönliche Beratung anbieten.'
                ]
            }
        }
        
        # Keywords for language detection
        self.language_keywords = {
            'en': ['english', 'switch to english', 'speak english', 'in english'],
            'hi': ['hindi', 'switch to hindi', 'speak hindi', 'in hindi', 'हिंदी', 'हिंदी में'],
            'de': ['german', 'switch to german', 'speak german', 'in german', 'deutsch', 'auf deutsch']
        }
    
    def detect_language_switch(self, message: str) -> Optional[str]:
        """Detect if user wants to switch language"""
        message = message.lower()
        for lang, keywords in self.language_keywords.items():
            if any(keyword in message for keyword in keywords):
                return lang
        return None

    def get_response(self, user_message: str) -> str:
        # Check for language switch request
        new_language = self.detect_language_switch(user_message)
        if new_language:
            self.current_language = new_language
            return self._get_random_response('language_switch')
        
        user_message = user_message.lower().strip()
        
        # Check for greetings
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'good', 'नमस्ते', 'नमस्कार', 'hallo', 'guten']):
            return self._get_random_response('greeting')
        
        # Check for university related questions
        if any(word in user_message for word in ['university', 'college', 'admission', 'विश्वविद्यालय', 'कॉलेज', 'प्रवेश', 'universität', 'hochschule', 'zulassung']):
            return self._get_random_response('university')
        
        # Check for visa related questions
        if any(word in user_message for word in ['visa', 'permit', 'वीजा', 'परमिट', 'visum', 'aufenthalt']):
            return self._get_random_response('visa')
        
        # Fallback response
        return self._get_random_response('fallback')
    
    def _get_random_response(self, category: str) -> str:
        import random
        responses = self.responses[self.current_language].get(category, self.responses[self.current_language]['fallback'])
        return random.choice(responses) 