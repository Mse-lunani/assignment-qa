interface ExamplesPanelProps {
  examples: string[];
  onClose: () => void;
  onSelectExample: (example: string) => void;
}

export default function ExamplesPanel({ examples, onClose, onSelectExample }: ExamplesPanelProps) {
  return (
    <div className="mb-6 p-4 bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="flex justify-between items-center mb-3">
        <h3 className="font-semibold text-gray-900">Example Questions</h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>
      <div className="grid gap-2 sm:grid-cols-2">
        {examples.map((example, index) => (
          <button
            key={index}
            onClick={() => onSelectExample(example)}
            className="text-left p-2 text-sm text-gray-700 hover:bg-gray-50 rounded border border-gray-100 transition-colors"
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}