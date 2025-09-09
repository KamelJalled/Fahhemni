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
      
      // Only create recognition if it doesn't exist
      if (!recognitionRef.current) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        
        // Set language based on app language
        recognition.lang = language === 'ar' ? 'ar-SA' : 'en-US';
        
        recognition.onstart = () => {
          setIsListening(true);
          setTranscript('');
          console.log('🎤 Microphone started - listening for 10 seconds minimum');
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
              errorMessage = language === 'ar' ? 'لم يتم اكتشاف صوت - حاول مرة أخرى' : 'No speech detected - try again';
              break;
            case 'audio-capture':
              errorMessage = language === 'ar' ? 'فشل في التقاط الصوت - تحقق من الميكروفون' : 'Audio capture failed - check microphone';
              break;
            case 'not-allowed':
              errorMessage = language === 'ar' ? 'يرجى السماح بإذن الميكروفون في المتصفح' : 'Please allow microphone permission in browser';
              break;
            case 'network':
              errorMessage = language === 'ar' ? 'خطأ في الشبكة - تحقق من الاتصال' : 'Network error - check connection';
              break;
            default:
              errorMessage = language === 'ar' ? 'خطأ في التعرف على الصوت' : 'Voice recognition error';
          }
          
          console.error('Voice recognition error:', event.error, errorMessage);
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
        // Update language if it changed
        recognitionRef.current.lang = language === 'ar' ? 'ar-SA' : 'en-US';
      }
    } else {
      setIsSupported(false);
    }

    // Cleanup on unmount
    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {
          console.log('🎤 Recognition cleanup completed');
        }
      }
    };
  }, [language, onResult, onError]);

  const convertMathExpression = (spokenText) => {
    console.log(`🎤 Converting speech: "${spokenText}"`);
    let result = spokenText.toLowerCase();
    const currentLang = language === 'ar' ? 'ar' : 'en';
    
    // Enhanced Arabic mathematical vocabulary with multiple variations
    const arabicMathVocab = {
      'س زائد ثمانية': 'x + 8',
      'س زائد سبعة': 'x + 7', 
      'س زائد ستة': 'x + 6',
      'س زائد خمسة': 'x + 5',
      'س زائد أربعة': 'x + 4',
      'س زائد ثلاثة': 'x + 3',
      'س زائد اثنان': 'x + 2',
      'س زائد واحد': 'x + 1',
      'س ناقص ثمانية': 'x - 8',
      'س ناقص سبعة': 'x - 7',
      'س ناقص ستة': 'x - 6',
      'س ناقص خمسة': 'x - 5',
      'س ناقص أربعة': 'x - 4',
      'س ناقص ثلاثة': 'x - 3',
      'س ناقص اثنان': 'x - 2',
      'س ناقص واحد': 'x - 1',
      'س زائد': 'x +',
      'س ناقص': 'x -',
      'س أكبر من': 'x >',
      'س أصغر من': 'x <',
      'س يساوي': 'x =',
      'س أكبر من أو يساوي': 'x ≥',
      'س أكبر من او يساوي': 'x ≥',
      'س أكبر أو يساوي': 'x ≥',
      'س أصغر من أو يساوي': 'x ≤',
      'س أصغر من او يساوي': 'x ≤',
      'س أصغر أو يساوي': 'x ≤',
      'أصغر من أو يساوي': '≤',
      'أصغر من او يساوي': '≤',
      'أصغر أو يساوي': '≤',
      'أكبر من أو يساوي': '≥',
      'أكبر من او يساوي': '≥',
      'أكبر أو يساوي': '≥',
      'أصغر من أو يساوى': '≤',
      'أكبر من أو يساوى': '≥',
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

    // Enhanced English mathematical expressions with exact phrase matching
    const englishMathExpressions = {
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
      'x minus one': 'x - 1',
      'x times eight': 'x × 8',
      'x times seven': 'x × 7',
      'x times six': 'x × 6',
      'x times five': 'x × 5',
      'x times four': 'x × 4',
      'x times three': 'x × 3',
      'x times two': 'x × 2',
      'x divided by eight': 'x ÷ 8',
      'x divided by seven': 'x ÷ 7',
      'x divided by six': 'x ÷ 6',
      'x divided by five': 'x ÷ 5',
      'x divided by four': 'x ÷ 4',
      'x divided by three': 'x ÷ 3',
      'x divided by two': 'x ÷ 2',
      'x plus': 'x +',
      'x minus': 'x -',
      'x times': 'x ×',
      'x divided by': 'x ÷',
      'x greater than': 'x >',
      'x less than': 'x <',
      'x equals': 'x =',
      'x greater than or equal to': 'x ≥',
      'x greater than or equal': 'x ≥',
      'x greater or equal to': 'x ≥',
      'x greater or equal': 'x ≥',
      'x less than or equal to': 'x ≤',
      'x less than or equal': 'x ≤',
      'x less or equal to': 'x ≤',
      'x less or equal': 'x ≤',
      'greater than or equal to': '≥',
      'greater than or equal': '≥',
      'greater or equal to': '≥',
      'greater or equal': '≥',
      'less than or equal to': '≤',
      'less than or equal': '≤',
      'less or equal to': '≤',
      'less or equal': '≤',
      'variable x': 'x',
      'the variable x': 'x'
    };

    // First pass: Apply language-specific complete expressions
    console.log(`🎤 Before conversion: "${result}"`);
    
    if (currentLang === 'ar') {
      Object.entries(arabicMathVocab).forEach(([phrase, symbol]) => {
        const regex = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        if (result.includes(phrase)) {
          result = result.replace(regex, symbol);
          console.log(`🎤 Arabic conversion: "${phrase}" → "${symbol}"`);
        }
      });
    } else {
      // Sort by length descending to match longer phrases first
      const sortedExpressions = Object.entries(englishMathExpressions)
        .sort((a, b) => b[0].length - a[0].length);
        
      sortedExpressions.forEach(([phrase, symbol]) => {
        const regex = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        if (result.includes(phrase)) {
          result = result.replace(regex, symbol);
          console.log(`🎤 English conversion: "${phrase}" → "${symbol}"`);
        }
      });
    }
    
    // Second pass: Convert remaining number words to digits
    Object.entries(numberWords[currentLang]).forEach(([word, digit]) => {
      const regex = new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
      result = result.replace(regex, digit);
    });
    
    // Third pass: Convert remaining math terms to symbols
    Object.entries(mathTerms[currentLang]).forEach(([term, symbol]) => {
      const regex = new RegExp(`\\b${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
      result = result.replace(regex, symbol);
    });
    
    // Clean up extra spaces around operators
    result = result.replace(/\s*([+\-=<>≤≥×÷])\s*/g, ' $1 ');
    result = result.replace(/\s+/g, ' ').trim();
    
    console.log(`🎤 Final conversion result: "${result}"`);
    return result;
  };

  const startListening = async () => {
    if (recognitionRef.current && !isListening) {
      try {
        // Request microphone permission explicitly with enhanced error handling
        console.log('🎤 Requesting microphone permission...');
        const stream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
          }
        });
        
        // Start with audio stream active
        console.log('🎤 Microphone permission granted, starting recognition...');
        
        // Ensure recognition is properly configured
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.maxAlternatives = 1;
        
        // Set minimum recognition time to prevent immediate shutoff - INCREASED TO 10 SECONDS
        let recognitionStarted = false;
        let minTimeElapsed = false;
        
        const startTimeout = setTimeout(() => {
          minTimeElapsed = true;
          console.log('🎤 Minimum recognition time elapsed (10 seconds)');
        }, 10000);
        
        recognitionRef.current.onstart = () => {
          recognitionStarted = true;
          setIsListening(true);
          setTranscript('');
          console.log('🎤 Voice recognition started successfully');
        };
        
        recognitionRef.current.onend = () => {
          clearTimeout(startTimeout);
          if (recognitionStarted && !minTimeElapsed) {
            console.log('🎤 Recognition ended too early, restarting...');
            // Restart if ended before minimum time
            setTimeout(() => {
              if (!isListening) {
                try {
                  recognitionRef.current.start();
                } catch (e) {
                  console.log('🎤 Could not restart recognition:', e);
                  setIsListening(false);
                  setIsProcessing(false);
                }
              }
            }, 100);
          } else {
            console.log('🎤 Voice recognition ended normally');
            setIsListening(false);
            setIsProcessing(false);
          }
        };
        
        recognitionRef.current.start();
        
        // Clean up the stream after starting recognition
        stream.getTracks().forEach(track => track.stop());
        
      } catch (error) {
        console.error('🎤 Microphone access error:', error);
        let errorMessage = 'Failed to start voice recognition';
        
        if (error.name === 'NotAllowedError') {
          errorMessage = language === 'ar' 
            ? 'يرجى السماح بإذن الميكروفون في إعدادات المتصفح. قد تحتاج إلى إعادة تحميل الصفحة بعد السماح بالإذن.' 
            : 'Please allow microphone access in browser settings. You may need to reload the page after granting permission.';
        } else if (error.name === 'NotFoundError') {
          errorMessage = language === 'ar' 
            ? 'لم يتم العثور على ميكروفون - تأكد من توصيل ميكروفون' 
            : 'No microphone found - please ensure a microphone is connected';
        } else if (error.name === 'NotReadableError') {
          errorMessage = language === 'ar' 
            ? 'الميكروفون قيد الاستخدام في تطبيق آخر' 
            : 'Microphone is being used by another application';
        }
        
        if (onError) {
          onError(errorMessage);
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