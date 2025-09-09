import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Mic, MicOff, Volume2, VolumeX, Loader2 } from 'lucide-react';

const VoiceInput = ({ onResult, onError, disabled = false }) => {
  const { language } = useLanguage();
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef(null);

  // Mathematical term mappings for voice recognition
  const mathTerms = {
    en: {
      'plus': '+',
      'add': '+',
      'added to': '+',
      'sum': '+',
      'minus': '-',
      'subtract': '-',
      'subtracted from': '-',
      'difference': '-',
      'times': '*',
      'multiply': '*',
      'multiplied by': '*',
      'product': '*',
      'divide': '/',
      'divided by': '/',
      'quotient': '/',
      'equals': '=',
      'equal to': '=',
      'is': '=',
      'greater than': '>',
      'less than': '<',
      'greater than or equal to': '≥',
      'less than or equal to': '≤',
      'not equal to': '≠',
      'x': 'x',
      'variable x': 'x',
      'unknown': 'x'
    },
    ar: {
      'زائد': '+',
      'جمع': '+',
      'مضاف إلى': '+',
      'ناقص': '-',
      'طرح': '-',
      'مطروح من': '-',
      'ضرب': '*',
      'مضروب في': '*',
      'ضرب في': '*',
      'قسمة': '/',
      'مقسوم على': '/',
      'يساوي': '=',
      'يساوى': '=',
      'أكبر من': '>',
      'أصغر من': '<',
      'أكبر من أو يساوي': '≥',
      'أصغر من أو يساوي': '≤',
      'لا يساوي': '≠',
      'س': 'x',
      'المتغير س': 'x',
      'المجهول': 'x'
    }
  };

  const numberWords = {
    en: {
      'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
      'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
      'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
      'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
      'eighteen': '18', 'nineteen': '19', 'twenty': '20'
    },
    ar: {
      'صفر': '0', 'واحد': '1', 'اثنان': '2', 'ثلاثة': '3', 'أربعة': '4',
      'خمسة': '5', 'ستة': '6', 'سبعة': '7', 'ثمانية': '8', 'تسعة': '9',
      'عشرة': '10', 'عشرون': '20'
    }
  };

  const text = {
    en: {
      startListening: 'Start Voice Input',
      stopListening: 'Stop Voice Input',
      listening: 'Listening...',
      processing: 'Converting...',
      notSupported: 'Voice input not supported',
      transcript: 'What you said:',
      converted: 'Converted to:',
      tryAgain: 'Try Again',
      clear: 'Clear'
    },
    ar: {
      startListening: 'ابدأ الإدخال الصوتي',
      stopListening: 'أوقف الإدخال الصوتي',
      listening: 'أستمع...',
      processing: 'تحويل...',
      notSupported: 'الإدخال الصوتي غير مدعوم',
      transcript: 'ما قلته:',
      converted: 'تم التحويل إلى:',
      tryAgain: 'جرب مرة أخرى',
      clear: 'مسح'
    }
  };

  useEffect(() => {
    // Check for Web Speech API support
    const SpeechRecognition = window.SpeechRecognition || 
                            window.webkitSpeechRecognition || 
                            window.mozSpeechRecognition || 
                            window.msSpeechRecognition;

    if (SpeechRecognition) {
      setIsSupported(true);
      
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      
      // Set language based on app language
      recognition.lang = language === 'ar' ? 'ar-SA' : 'en-US';
      
      recognition.onstart = () => {
        setIsListening(true);
        setTranscript('');
      };

      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setTranscript(interimTranscript || finalTranscript);

        if (finalTranscript) {
          setIsProcessing(true);
          const converted = convertMathExpression(finalTranscript.trim());
          setTimeout(() => {
            setIsProcessing(false);
            if (onResult) {
              onResult(converted);
            }
          }, 500);
        }
      };

      recognition.onerror = (event) => {
        setIsListening(false);
        setIsProcessing(false);
        let errorMessage = 'Voice recognition error';
        
        switch (event.error) {
          case 'no-speech':
            errorMessage = language === 'ar' ? 'لم يتم اكتشاف صوت' : 'No speech detected';
            break;
          case 'audio-capture':
            errorMessage = language === 'ar' ? 'فشل في التقاط الصوت' : 'Audio capture failed';
            break;
          case 'not-allowed':
            errorMessage = language === 'ar' ? 'تم رفض إذن الميكروفون' : 'Microphone permission denied';
            break;
          default:
            errorMessage = language === 'ar' ? 'خطأ في التعرف على الصوت' : 'Voice recognition error';
        }
        
        if (onError) {
          onError(errorMessage);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
        setIsProcessing(false);
      };

      recognitionRef.current = recognition;
    } else {
      setIsSupported(false);
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [language, onResult, onError]);

  const convertMathExpression = (spokenText) => {
    let result = spokenText.toLowerCase();
    const currentLang = language === 'ar' ? 'ar' : 'en';
    
    // Enhanced Arabic mathematical vocabulary
    const arabicMathVocab = {
      'س زائد': 'x +',
      'س ناقص': 'x -',
      'س أكبر من': 'x >',
      'س أصغر من': 'x <',
      'س يساوي': 'x =',
      'س أكبر من أو يساوي': 'x ≥',
      'س أصغر من أو يساوي': 'x ≤',
      'ثمانية': '8',
      'سبعة': '7',
      'ستة': '6',
      'خمسة': '5',
      'أربعة': '4',
      'ثلاثة': '3',
      'اثنان': '2',
      'واحد': '1',
      'صفر': '0'
    };

    // Enhanced English mathematical expressions  
    const englishMathExpressions = {
      'x plus': 'x +',
      'x minus': 'x -',
      'x greater than': 'x >',
      'x less than': 'x <',
      'x equals': 'x =',
      'x greater than or equal': 'x ≥',
      'x less than or equal': 'x ≤',
      'x plus eight': 'x + 8',
      'x plus seven': 'x + 7',
      'x plus six': 'x + 6',
      'x plus five': 'x + 5',
      'x plus four': 'x + 4',
      'x plus three': 'x + 3',
      'x plus two': 'x + 2',
      'x plus one': 'x + 1',
      'x minus eight': 'x - 8',
      'x minus seven': 'x - 7',
      'x minus six': 'x - 6',
      'x minus five': 'x - 5',
      'x minus four': 'x - 4',
      'x minus three': 'x - 3',
      'x minus two': 'x - 2',
      'x minus one': 'x - 1'
    };

    // Apply language-specific expressions first
    if (currentLang === 'ar') {
      Object.entries(arabicMathVocab).forEach(([phrase, symbol]) => {
        const regex = new RegExp(phrase, 'gi');
        result = result.replace(regex, symbol);
      });
    } else {
      Object.entries(englishMathExpressions).forEach(([phrase, symbol]) => {
        const regex = new RegExp(phrase, 'gi');
        result = result.replace(regex, symbol);
      });
    }
    
    // Convert number words to digits
    Object.entries(numberWords[currentLang]).forEach(([word, digit]) => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi');
      result = result.replace(regex, digit);
    });
    
    // Convert math terms to symbols
    Object.entries(mathTerms[currentLang]).forEach(([term, symbol]) => {
      const regex = new RegExp(`\\b${term}\\b`, 'gi');
      result = result.replace(regex, symbol);
    });
    
    // Clean up extra spaces around operators
    result = result.replace(/\s*([+\-=<>≤≥])\s*/g, ' $1 ');
    result = result.replace(/\s+/g, ' ').trim();
    
    return result;
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      try {
        recognitionRef.current.start();
      } catch (error) {
        if (onError) {
          onError(language === 'ar' ? 'فشل في بدء التعرف على الصوت' : 'Failed to start voice recognition');
        }
      }
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const clearTranscript = () => {
    setTranscript('');
  };

  if (!isSupported) {
    return (
      <Card className="border-red-200 bg-red-50">
        <CardContent className="p-4 text-center">
          <VolumeX className="w-8 h-8 mx-auto mb-2 text-red-500" />
          <p className="text-red-700">{text[language].notSupported}</p>
          <p className="text-sm text-red-600 mt-1">
            {language === 'ar' 
              ? 'استخدم متصفح Chrome للحصول على أفضل تجربة'
              : 'Please use Chrome browser for best experience'
            }
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-blue-200 bg-blue-50">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Volume2 className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-blue-900">
              {language === 'ar' ? 'الإدخال الصوتي' : 'Voice Input'}
            </span>
          </div>
          
          <div className="flex gap-2">
            {!isListening ? (
              <Button
                onClick={startListening}
                disabled={disabled || isProcessing}
                variant="default"
                size="sm"
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Mic className="w-4 h-4 mr-1" />
                {text[language].startListening}
              </Button>
            ) : (
              <Button
                onClick={stopListening}
                variant="destructive"
                size="sm"
                className="animate-pulse"
              >
                <MicOff className="w-4 h-4 mr-1" />
                {text[language].stopListening}
              </Button>
            )}
            
            {transcript && (
              <Button
                onClick={clearTranscript}
                variant="outline"
                size="sm"
              >
                {text[language].clear}
              </Button>
            )}
          </div>
        </div>

        {isListening && (
          <div className="mb-3 p-2 bg-yellow-100 border border-yellow-300 rounded text-center">
            <div className="flex items-center justify-center gap-2">
              <div className="animate-pulse w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="text-yellow-800">{text[language].listening}</span>
            </div>
          </div>
        )}

        {isProcessing && (
          <div className="mb-3 p-2 bg-blue-100 border border-blue-300 rounded text-center">
            <div className="flex items-center justify-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
              <span className="text-blue-800">{text[language].processing}</span>
            </div>
          </div>
        )}

        {transcript && (
          <div className="space-y-2">
            <div className="p-2 bg-gray-100 border rounded">
              <div className="text-sm font-medium text-gray-600 mb-1">
                {text[language].transcript}
              </div>
              <div className="text-gray-800">{transcript}</div>
            </div>
          </div>
        )}

        <div className="mt-3 text-xs text-gray-500">
          {language === 'ar' 
            ? 'قل تعبيرات رياضية مثل "س أكبر من خمسة" أو "اثنان س زائد ثلاثة"'
            : 'Say math expressions like "x greater than five" or "two x plus three"'
          }
        </div>
      </CardContent>
    </Card>
  );
};

export default VoiceInput;