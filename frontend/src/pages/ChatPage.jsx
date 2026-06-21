import { useEffect, useState } from "react";
import api from "../api/api";

function ChatPage({ token }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const authHeaders = {
    Authorization: `Bearer ${token}`,
  };

  const loadHistory = async () => {
    try {
      const response = await api.get("/chat/history", {
        headers: authHeaders,
      });

      setMessages(response.data.reverse());
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        question: currentQuestion,
        answer: "Cevaplanıyor..."
      }
    ]);

    setQuestion("");
    setLoading(true);
    setSources([]);

    try {
      const response = await api.post(
        "/query",
        {
          question: currentQuestion,
        },
        {
          headers: authHeaders,
        }
      );

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          question: response.data.question,
          answer: response.data.answer,
        };
        return updated;
      });

      setSources(response.data.sources);
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          question: currentQuestion,
          answer: "Bir hata oluştu.",
        };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Soru Sor</h2>

      <div className="chat-box">
        {messages.map((message, index) => (
          <div className="chat-message" key={index}>
            <div className="user-message">
              <strong>Sen:</strong>
              <p>{message.question}</p>
            </div>

            <div className="assistant-message">
              <strong>Company RAG:</strong>
              <p>{message.answer}</p>
            </div>
          </div>
        ))}
      </div>

      <textarea
        placeholder="Belge hakkında soru sor..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Cevaplanıyor..." : "Sor"}
      </button>

      {sources.length > 0 && (
        <div className="answer">
          <h3>Son Cevabın Kaynakları</h3>

          {sources.map((source, index) => (
            <div className="source" key={index}>
              📄 {source.filename} — Sayfa {source.page_number}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default ChatPage;
