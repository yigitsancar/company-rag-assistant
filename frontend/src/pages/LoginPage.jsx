import { useState } from "react";
import api from "../api/api";

function LoginPage({ onLogin, onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const login = async () => {
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      onLogin(response.data.access_token, response.data.role);
      setError("");
    } catch (err) {
      setError("Giriş başarısız.");
    }
  };

  return (
    <section className="card login-card">
      <h2>Giriş Yap</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Şifre"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={login}>Giriş Yap</button>

      {error && <p className="message">{error}</p>}

      <p className="auth-switch">
        Hesabın yok mu?
        <span className="link-btn" onClick={onSwitch}>
          Kayıt Ol
        </span>
      </p>
    </section>
  );
}

export default LoginPage;
