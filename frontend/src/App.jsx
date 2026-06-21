import { useState } from "react";

import "./App.css";

import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import ChatPage from "./pages/ChatPage";
import DocumentsPage from "./pages/DocumentsPage";
import LoginPage from "./pages/LoginPage";
import UsersPage from "./pages/UsersPage";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [role, setRole] = useState(localStorage.getItem("role") || "");
  const [activePage, setActivePage] = useState("chat");
  const [authPage, setAuthPage] = useState("login");

  const canManageDocuments = role === "ADMIN" || role === "MANAGER";
  const canManageUsers = role === "ADMIN";

  const handleLogin = (accessToken, userRole) => {
    localStorage.setItem("token", accessToken);
    localStorage.setItem("role", userRole);

    setToken(accessToken);
    setRole(userRole);
    setActivePage(userRole === "ADMIN" ? "dashboard" : "chat");
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    setToken("");
    setRole("");
    setActivePage("chat");
    setAuthPage("login");
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div>
          <div className="brand">
            <div className="brand-icon">C</div>

            <div>
              <h2>Company RAG</h2>
              <p>AI Knowledge Assistant</p>
            </div>
          </div>

          {token && (
            <nav className="nav">
              {canManageUsers && (
                <button
                  className={
                    activePage === "dashboard" ? "nav-item active" : "nav-item"
                  }
                  onClick={() => setActivePage("dashboard")}
                >
                  Dashboard
                </button>
              )}

              <button
                className={activePage === "chat" ? "nav-item active" : "nav-item"}
                onClick={() => setActivePage("chat")}
              >
                Sohbet
              </button>

              {canManageDocuments && (
                <button
                  className={
                    activePage === "documents" ? "nav-item active" : "nav-item"
                  }
                  onClick={() => setActivePage("documents")}
                >
                  Belgeler
                </button>
              )}

              {canManageUsers && (
                <button
                  className={activePage === "users" ? "nav-item active" : "nav-item"}
                  onClick={() => setActivePage("users")}
                >
                  Kullanıcılar
                </button>
              )}
            </nav>
          )}
        </div>

        {token && (
          <div className="profile-card">
            <span className="role-badge">{role}</span>

            <button className="secondary-btn" onClick={logout}>
              Çıkış Yap
            </button>
          </div>
        )}
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>Company RAG Assistant</h1>
            <p>Şirket belgelerinizi güvenli şekilde sorgulayın.</p>
          </div>
        </header>

        {!token ? (
          authPage === "login" ? (
            <LoginPage
              onLogin={handleLogin}
              onSwitch={() => setAuthPage("register")}
            />
          ) : (
            <RegisterPage onSwitch={() => setAuthPage("login")} />
          )
        ) : (
          <>
            {activePage === "dashboard" && canManageUsers && (
              <DashboardPage token={token} />
            )}

            {activePage === "chat" && <ChatPage token={token} />}

            {activePage === "documents" && canManageDocuments && (
              <DocumentsPage token={token} role={role} />
            )}

            {activePage === "users" && canManageUsers && (
              <UsersPage token={token} />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
