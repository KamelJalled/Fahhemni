import React from 'react';
import { X, BookOpen, AlertTriangle, CheckCircle, HelpCircle } from 'lucide-react';
import { useLanguage } from '../App';

const RulesModal = ({ isOpen, onClose }) => {
  const { language } = useLanguage();

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="rules-modal bg-white rounded-xl max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-6 flex justify-between items-center rounded-t-xl">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-3">
            <BookOpen className="text-blue-600" size={28} />
            {language === 'ar' ? 'قواعد حل المتباينات' : 'Inequality Solving Rules'}
          </h2>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={24} className="text-gray-600" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Rule 1: Writing Negative Numbers */}
          <div className="rule-section bg-blue-50 p-5 rounded-lg border-l-4 border-blue-500">
            <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center gap-2">
              <CheckCircle size={20} />
              {language === 'ar' ? '1. كتابة الأعداد السالبة' : '1. Writing Negative Numbers'}
            </h3>
            <p className="text-gray-700 mb-3">
              {language === 'ar' 
                ? 'يمكنك كتابة الأعداد السالبة بطريقتين:' 
                : 'You can write negative numbers in two ways:'}
            </p>
            <div className="examples bg-gray-900 text-green-400 p-4 rounded-md font-mono text-sm">
              <div className="mb-2">k ≤ -5 ✓  {language === 'ar' ? 'أو' : 'or'}  k ≤ (-5) ✓</div>
              <div className="mb-2">m {'>'} -0.5 ✓  {language === 'ar' ? 'أو' : 'or'}  m {'>'} (-0.5) ✓</div>
              <div>-3m/(-3) ✓  {language === 'ar' ? 'أو' : 'or'}  -3m/-3 ✓</div>
            </div>
          </div>

          {/* Rule 2: Flipping Inequality Signs */}
          <div className="rule-section bg-amber-50 p-5 rounded-lg border-l-4 border-amber-500">
            <h3 className="text-lg font-semibold text-amber-800 mb-3 flex items-center gap-2">
              <AlertTriangle size={20} />
              {language === 'ar' ? '2. قلب إشارة المتباينة' : '2. Flipping Inequality Signs'}
            </h3>
            <p className="text-gray-700 mb-3">
              {language === 'ar' 
                ? 'عند القسمة أو الضرب في عدد سالب، اقلب الإشارة:' 
                : 'When dividing or multiplying by a negative, flip the sign:'}
            </p>
            <div className="examples bg-gray-900 text-green-400 p-4 rounded-md font-mono text-sm">
              <div className="mb-2">-3m &lt; 15 → m {'>'} -5 ✓</div>
              <div className="mb-2">&lt; {language === 'ar' ? 'يصبح' : 'becomes'} {'>'} ✓</div>
              <div>≤ {language === 'ar' ? 'يصبح' : 'becomes'} ≥ ✓</div>
            </div>
          </div>

          {/* Rule 3: Accepted Answer Formats */}
          <div className="rule-section bg-green-50 p-5 rounded-lg border-l-4 border-green-500">
            <h3 className="text-lg font-semibold text-green-800 mb-3 flex items-center gap-2">
              <CheckCircle size={20} />
              {language === 'ar' ? '3. صيغ الإجابات المقبولة' : '3. Accepted Answer Formats'}
            </h3>
            <div className="overflow-x-auto">
              <table className="formats-table w-full border-collapse bg-white rounded-md overflow-hidden shadow-sm">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="p-3 text-left border border-gray-200">
                      {language === 'ar' ? 'صيغ مقبولة' : 'Accepted Formats'}
                    </th>
                    <th className="p-3 text-center border border-gray-200">
                      {language === 'ar' ? 'جميعها صحيحة' : 'All Correct'}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="p-3 border border-gray-200 font-mono text-sm">x {'>'} 5</td>
                    <td rowSpan="4" className="p-3 border border-gray-200 text-center text-green-600 text-xl font-bold">✓</td>
                  </tr>
                  <tr>
                    <td className="p-3 border border-gray-200 font-mono text-sm">x&gt;5</td>
                  </tr>
                  <tr>
                    <td className="p-3 border border-gray-200 font-mono text-sm">5 &lt; x</td>
                  </tr>
                  <tr>
                    <td className="p-3 border border-gray-200 font-mono text-sm">س {'>'} ٥</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Rule 4: Mathematical Symbols */}
          <div className="rule-section bg-purple-50 p-5 rounded-lg border-l-4 border-purple-500">
            <h3 className="text-lg font-semibold text-purple-800 mb-3 flex items-center gap-2">
              <HelpCircle size={20} />
              {language === 'ar' ? '4. الرموز الرياضية' : '4. Mathematical Symbols'}
            </h3>
            <div className="symbols-grid grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="bg-white p-3 rounded border border-purple-200">
                <span className="font-mono text-lg text-purple-700">≥</span> {language === 'ar' ? 'أو' : 'or'} <span className="font-mono text-lg text-purple-700">&gt;=</span>
                <div className="text-sm text-gray-600 mt-1">
                  {language === 'ar' ? 'أكبر من أو يساوي' : 'Greater than or equal'}
                </div>
              </div>
              <div className="bg-white p-3 rounded border border-purple-200">
                <span className="font-mono text-lg text-purple-700">≤</span> {language === 'ar' ? 'أو' : 'or'} <span className="font-mono text-lg text-purple-700">&lt;=</span>
                <div className="text-sm text-gray-600 mt-1">
                  {language === 'ar' ? 'أصغر من أو يساوي' : 'Less than or equal'}
                </div>
              </div>
              <div className="bg-white p-3 rounded border border-purple-200">
                <span className="font-mono text-lg text-purple-700">&gt;</span>
                <div className="text-sm text-gray-600 mt-1">
                  {language === 'ar' ? 'أكبر من' : 'Greater than'}
                </div>
              </div>
              <div className="bg-white p-3 rounded border border-purple-200">
                <span className="font-mono text-lg text-purple-700">&lt;</span>
                <div className="text-sm text-gray-600 mt-1">
                  {language === 'ar' ? 'أصغر من' : 'Less than'}
                </div>
              </div>
            </div>
          </div>

          {/* Tips Section */}
          <div className="tips-section bg-gradient-to-r from-yellow-50 to-orange-50 p-5 rounded-lg border-l-4 border-yellow-500">
            <h3 className="text-lg font-semibold text-yellow-800 mb-3">
              💡 {language === 'ar' ? 'نصائح مفيدة' : 'Helpful Tips'}
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-yellow-600 mt-1">•</span>
                {language === 'ar' ? 'المسافات غير مهمة' : 'Spaces don\'t matter'}
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-600 mt-1">•</span>
                {language === 'ar' ? 'يمكن استخدام الأرقام العربية أو الإنجليزية' : 'Use Arabic or English numbers'}
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-600 mt-1">•</span>
                {language === 'ar' ? 'تأكد من قلب الإشارة مع الأعداد السالبة' : 'Remember to flip signs with negatives'}
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-600 mt-1">•</span>
                {language === 'ar' ? 'الأقواس حول الأعداد السالبة اختيارية' : 'Parentheses around negative numbers are optional'}
              </li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 p-4 rounded-b-xl border-t">
          <button 
            onClick={onClose}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            {language === 'ar' ? 'فهمت، شكراً!' : 'Got it, Thanks!'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RulesModal;