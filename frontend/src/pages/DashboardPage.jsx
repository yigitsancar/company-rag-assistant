import { useEffect, useState } from "react";
import api from "../api/api";

function DashboardPage({ token }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.get("/dashboard/stats", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setStats(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (!stats) {
    return <div className="card">Dashboard yükleniyor...</div>;
  }

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Kullanıcılar</h3>
          <p>{stats.total_users}</p>
        </div>

        <div className="stat-card">
          <h3>Belgeler</h3>
          <p>{stats.total_documents}</p>
        </div>

        <div className="stat-card">
          <h3>Chunklar</h3>
          <p>{stats.total_chunks}</p>
        </div>

        <div className="stat-card">
          <h3>Sorular</h3>
          <p>{stats.total_questions}</p>
        </div>
      </div>

      <div className="card">
        <h3>Son Belgeler</h3>

        {stats.recent_documents.map((doc) => (
          <p key={doc.id}>{doc.filename}</p>
        ))}
      </div>

      <div className="card">
        <h3>Son Kullanıcılar</h3>

        {stats.recent_users.map((user) => (
          <p key={user.id}>
            {user.email} ({user.role})
          </p>
        ))}
      </div>
    </div>
  );
}

export default DashboardPage;
