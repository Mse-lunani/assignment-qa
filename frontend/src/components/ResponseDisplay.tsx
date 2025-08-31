interface QueryResponse {
  question: string;
  answer: string;
  timestamp: string;
  ai_model_used: string;
  response_time_ms: number;
}

interface ResponseDisplayProps {
  response: QueryResponse;
}

export default function ResponseDisplay({ response }: ResponseDisplayProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="mb-4">
        <h3 className="font-semibold text-gray-900 mb-2">Question:</h3>
        <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">{response.question}</p>
      </div>
      <div className="mb-4">
        <h3 className="font-semibold text-gray-900 mb-2">Answer:</h3>
        <div className="text-gray-700 bg-green-50 p-4 rounded-lg whitespace-pre-wrap">
          {response.answer}
        </div>
      </div>
      <div className="text-xs text-gray-500 border-t pt-3 flex flex-wrap gap-4">
        <span>⏱️ Response time: {response.response_time_ms}ms</span>
        <span>🤖 Model: {response.ai_model_used}</span>
        <span>📅 {new Date(response.timestamp).toLocaleString()}</span>
      </div>
    </div>
  );
}