import React, { useState } from 'react';
import { useLanguage } from '../App';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Calculator, Delete, Keyboard, Languages } from 'lucide-react';

const MathKeyboard = ({ onSymbolSelect, onNumberSelect, onOperatorSelect, onAction }) => {
  const { language } = useLanguage();
  const [numberSystem, setNumberSystem] = useState('western');
  const [activeTab, setActiveTab] = useState('numbers');

  const westernNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  const easternNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];

  const inequalitySymbols = [
    { symbol: '<', label: { en: 'Less than', ar: 'أصغر من' } },
    { symbol: '>', label: { en: 'Greater than', ar: 'أكبر من' } },
    { symbol: '≤', label: { en: 'Less than or equal', ar: 'أصغر من أو يساوي' } },
    { symbol: '≥', label: { en: 'Greater than or equal', ar: 'أكبر من أو يساوي' } },
    { symbol: '=', label: { en: 'Equals', ar: 'يساوي' } },
    { symbol: '≠', label: { en: 'Not equal', ar: 'لا يساوي' } }
  ];

  const operations = [
    { symbol: '+', label: { en: 'Plus', ar: 'زائد' } },
    { symbol: '-', label: { en: 'Minus', ar: 'ناقص' } },
    { symbol: '×', label: { en: 'Multiply', ar: 'ضرب' } },
    { symbol: '÷', label: { en: 'Divide', ar: 'قسمة' } }
  ];

  const commonSymbols = [
    { symbol: 'x', label: { en: 'Variable x', ar: 'المتغير س' } },
    { symbol: '(', label: { en: 'Open parenthesis', ar: 'قوس مفتوح' } },
    { symbol: ')', label: { en: 'Close parenthesis', ar: 'قوس مغلق' } },
    { symbol: '-', label: { en: 'Negative', ar: 'سالب' } }
  ];

  const actions = [
    { id: 'clear', icon: Delete, label: { en: 'Clear', ar: 'مسح' }, color: 'bg-red-500 hover:bg-red-600' },
    { id: 'backspace', icon: '←', label: { en: 'Backspace', ar: 'مسح للخلف' }, color: 'bg-orange-500 hover:bg-orange-600' }
  ];

  const text = {
    en: {
      title: 'Math Keyboard',
      numbers: 'Numbers',
      symbols: 'Symbols', 
      operations: 'Operations',
      actions: 'Actions',
      western: 'Western (0-9)',
      eastern: 'Eastern (٠-٩)',
      voice: 'Voice'
    },
    ar: {
      title: 'لوحة المفاتيح الرياضية',
      numbers: 'الأرقام',
      symbols: 'الرموز',
      operations: 'العمليات', 
      actions: 'الإجراءات',
      western: 'غربية (0-9)',
      eastern: 'شرقية (٠-٩)',
      voice: 'صوت'
    }
  };

  const handleSymbolClick = (symbol, type) => {
    switch (type) {
      case 'number':
        if (onNumberSelect) onNumberSelect(symbol);
        break;
      case 'operator':
        if (onOperatorSelect) onOperatorSelect(symbol);
        break;
      case 'symbol':
        if (onSymbolSelect) onSymbolSelect(symbol);
        break;
      default:
        if (onSymbolSelect) onSymbolSelect(symbol);
    }
  };

  const handleActionClick = (actionId) => {
    if (onAction) {
      onAction(actionId);
    }
  };

  const TabButton = ({ id, icon: Icon, label, isActive, onClick }) => (
    <Button
      variant={isActive ? "default" : "outline"}
      size="sm"
      onClick={onClick}
      className={`flex-1 ${isActive ? 'bg-blue-600 text-white' : 'text-blue-600'}`}
    >
      {typeof Icon === 'string' ? Icon : <Icon className="w-4 h-4 mr-1" />}
      <span className="text-xs">{label}</span>
    </Button>
  );

  const SymbolButton = ({ symbol, label, onClick, className = "" }) => (
    <Button
      variant="outline"
      className={`h-12 text-lg font-mono hover:bg-blue-50 border-blue-200 ${className}`}
      onClick={() => onClick(symbol)}
      title={label}
    >
      {symbol}
    </Button>
  );

  return (
    <Card className="w-full max-w-md mx-auto border-blue-200">
      <CardHeader className="pb-3">
        <CardTitle className="text-center text-blue-900 flex items-center justify-center gap-2">
          <Calculator className="w-5 h-5" />
          {text[language].title}
        </CardTitle>
        
        {/* Tab Navigation */}
        <div className="flex gap-1 mt-2">
          <TabButton
            id="numbers"
            icon="123"
            label={text[language].numbers}
            isActive={activeTab === 'numbers'}
            onClick={() => setActiveTab('numbers')}
          />
          <TabButton
            id="symbols"
            icon={Calculator}
            label={text[language].symbols}
            isActive={activeTab === 'symbols'}
            onClick={() => setActiveTab('symbols')}
          />
          <TabButton
            id="operations"
            icon="±"
            label={text[language].operations}
            isActive={activeTab === 'operations'}
            onClick={() => setActiveTab('operations')}
          />
          <TabButton
            id="actions"
            icon={Keyboard}
            label={text[language].actions}
            isActive={activeTab === 'actions'}
            onClick={() => setActiveTab('actions')}
          />
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Numbers Tab */}
        {activeTab === 'numbers' && (
          <div className="space-y-3">
            {/* Number System Toggle */}
            <div className="flex gap-2 mb-3">
              <Button
                variant={numberSystem === 'western' ? "default" : "outline"}
                size="sm"
                onClick={() => setNumberSystem('western')}
                className="flex-1 text-xs"
              >
                <Languages className="w-3 h-3 mr-1" />
                {text[language].western}
              </Button>
              <Button
                variant={numberSystem === 'eastern' ? "default" : "outline"}
                size="sm"
                onClick={() => setNumberSystem('eastern')}
                className="flex-1 text-xs"
              >
                <Languages className="w-3 h-3 mr-1" />
                {text[language].eastern}
              </Button>
            </div>

            {/* Number Grid */}
            <div className="grid grid-cols-5 gap-1">
              {(numberSystem === 'western' ? westernNumbers : easternNumbers).map((number) => (
                <SymbolButton
                  key={number}
                  symbol={number}
                  label={number}
                  onClick={(symbol) => handleSymbolClick(symbol, 'number')}
                  className="text-center min-w-0"
                />
              ))}
            </div>
          </div>
        )}

        {/* Symbols Tab */}
        {activeTab === 'symbols' && (
          <div className="space-y-4">
            {/* Inequality Symbols */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                {language === 'ar' ? 'رموز المتباينات' : 'Inequality Symbols'}
              </h4>
              <div className="grid grid-cols-3 gap-2">
                {inequalitySymbols.map(({ symbol, label }) => (
                  <SymbolButton
                    key={symbol}
                    symbol={symbol}
                    label={label[language]}
                    onClick={(symbol) => handleSymbolClick(symbol, 'symbol')}
                    className="text-blue-600"
                  />
                ))}
              </div>
            </div>

            {/* Common Symbols */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">
                {language === 'ar' ? 'رموز شائعة' : 'Common Symbols'}
              </h4>
              <div className="grid grid-cols-4 gap-2">
                {commonSymbols.map(({ symbol, label }) => (
                  <SymbolButton
                    key={symbol}
                    symbol={symbol}
                    label={label[language]}
                    onClick={(symbol) => handleSymbolClick(symbol, 'symbol')}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Operations Tab */}
        {activeTab === 'operations' && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-2">
              {operations.map(({ symbol, label }) => (
                <SymbolButton
                  key={symbol}
                  symbol={symbol}
                  label={label[language]}
                  onClick={(symbol) => handleSymbolClick(symbol, 'operator')}
                  className="text-green-600 h-16 text-xl"
                />
              ))}
            </div>
          </div>
        )}

        {/* Actions Tab */}
        {activeTab === 'actions' && (
          <div className="space-y-3">
            <div className="grid grid-cols-1 gap-2">
              {actions.map(({ id, icon: Icon, label, color }) => (
                <Button
                  key={id}
                  onClick={() => handleActionClick(id)}
                  className={`h-12 text-white ${color}`}
                >
                  {typeof Icon === 'string' ? (
                    <span className="text-xl mr-2">{Icon}</span>
                  ) : (
                    <Icon className="w-5 h-5 mr-2" />
                  )}
                  {label[language]}
                </Button>
              ))}
            </div>

            {/* Voice Input Button */}
            <Button
              variant="outline"
              className="w-full h-12 border-blue-300 text-blue-600 hover:bg-blue-50"
              onClick={() => handleActionClick('voice')}
            >
              <div className="flex items-center justify-center gap-2">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                {text[language].voice}
              </div>
            </Button>
          </div>
        )}

        {/* Help Text */}
        <div className="mt-4 p-2 bg-gray-50 rounded text-xs text-gray-600 text-center">
          {language === 'ar' 
            ? 'اضغط على الرموز لإدخالها في حقل الإجابة'
            : 'Tap symbols to insert them into the answer field'
          }
        </div>
      </CardContent>
    </Card>
  );
};

export default MathKeyboard;