'use client';

interface QueryFormProps {
  question: string;
  setQuestion: (value: string) => void;
  loading: boolean;
  onSubmit: (e: React.FormEvent) => void;
}

export default function QueryForm({ question, setQuestion, loading, onSubmit }: QueryFormProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <form onSubmit={onSubmit}>
        <div className="mb-4">
          <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
            Your Question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Who is the governor of Meru County?"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none placeholder-gray-400 text-black"
            rows={3}
            maxLength={500}
            required
          />
          <div className="text-right text-xs text-gray-500 mt-1">
            {question.length}/500 characters
          </div>
        </div>
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="w-full sm:w-auto px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Getting Answer...
            </>
          ) : (
            <>
              Ask Question
            </>
          )}
        </button>
      </form>
    </div>
  );
}