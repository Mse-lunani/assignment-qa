interface HeaderProps {
  onViewExamples: () => void;
  onViewHistory: () => void;
  onClearHistory: () => void;
  historyCount: number;
}

export default function Header({ onViewExamples, onViewHistory, onClearHistory, historyCount }: HeaderProps) {
  return (
    <div className="text-center mb-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-2">
        🇰🇪 Kenyan Leaders Q&A System
      </h1>
      <p className="text-gray-600 text-lg">
        Ask questions about Kenyan political leaders, counties, and government positions
      </p>
      <div className="mt-4 flex flex-wrap gap-2 justify-center">
        <button
          onClick={onViewExamples}
          className="px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-lg text-sm transition-colors"
        >
          View Examples
        </button>
        <button
          onClick={onViewHistory}
          className="px-4 py-2 bg-green-100 hover:bg-green-200 text-green-800 rounded-lg text-sm transition-colors"
        >
          Query History
        </button>
        {historyCount > 0 && (
          <button
            onClick={onClearHistory}
            className="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 rounded-lg text-sm transition-colors"
          >
            Clear History
          </button>
        )}
      </div>
    </div>
  );
}