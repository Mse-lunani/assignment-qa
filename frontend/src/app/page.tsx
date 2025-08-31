'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import QueryForm from '@/components/QueryForm';
import ResponseDisplay from '@/components/ResponseDisplay';
import ExamplesPanel from '@/components/ExamplesPanel';
import HistoryPanel from '@/components/HistoryPanel';
import ErrorDisplay from '@/components/ErrorDisplay';

interface QueryResponse {
  question: string;
  answer: string;
  timestamp: string;
  ai_model_used: string;
  response_time_ms: number;
}

interface HistoryItem {
  id: string;
  question: string;
  answer: string;
  timestamp: string;
  ai_model_used: string;
  response_time_ms: number;
}

export default function Home() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [examples, setExamples] = useState<string[]>([]);
  const [showExamples, setShowExamples] = useState(false);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const fetchExamples = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/examples`);
      const data = await res.json();
      setExamples(data.examples);
      setShowExamples(true);
    } catch (err) {
      console.error('Failed to fetch examples:', err);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/history`);
      const data = await res.json();
      setHistory(data.history);
      setShowHistory(true);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  const clearHistory = async () => {
    try {
      await fetch(`${API_BASE}/api/history`, { method: 'DELETE' });
      setHistory([]);
      setShowHistory(false);
    } catch (err) {
      console.error('Failed to clear history:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to get response');
      }

      const data: QueryResponse = await res.json();
      setResponse(data);
      setQuestion('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectExample = (example: string) => {
    setQuestion(example);
    setShowExamples(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <Header
          onViewExamples={fetchExamples}
          onViewHistory={fetchHistory}
          onClearHistory={clearHistory}
          historyCount={history.length}
        />

        {showExamples && examples.length > 0 && (
          <ExamplesPanel
            examples={examples}
            onClose={() => setShowExamples(false)}
            onSelectExample={handleSelectExample}
          />
        )}

        <QueryForm
          question={question}
          setQuestion={setQuestion}
          loading={loading}
          onSubmit={handleSubmit}
        />

        {error && <ErrorDisplay error={error} />}

        {response && <ResponseDisplay response={response} />}

        {showHistory && (
          <HistoryPanel
            history={history}
            onClose={() => setShowHistory(false)}
          />
        )}

        <footer className="text-center mt-8 text-gray-500 text-sm">
          <p>Powered by Google Gemini 2.0 Flash • Built with Next.js & FastAPI</p>
        </footer>
      </div>
    </div>
  );
}
