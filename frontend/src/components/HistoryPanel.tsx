interface HistoryItem {
  id: string;
  question: string;
  answer: string;
  timestamp: string;
  ai_model_used: string;
  response_time_ms: number;
}

interface HistoryPanelProps {
  history: HistoryItem[];
  onClose: () => void;
}

export default function HistoryPanel({ history, onClose }: HistoryPanelProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold text-gray-900">Query History</h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>
      {history.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No queries in history</p>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {history.map((item) => (
            <div key={item.id} className="border border-gray-200 rounded-lg p-4">
              <div className="mb-2">
                <strong className="text-gray-900">Q:</strong>
                <span className="text-gray-700 ml-2">{item.question}</span>
              </div>
              <div className="mb-2">
                <strong className="text-gray-900">A:</strong>
                <div className="text-gray-700 ml-2 mt-1 text-sm bg-gray-50 p-2 rounded whitespace-pre-wrap">
                  {item.answer}
                </div>
              </div>
              <div className="text-xs text-gray-500 flex gap-4">
                <span>⏱️ {item.response_time_ms}ms</span>
                <span>📅 {new Date(item.timestamp).toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}