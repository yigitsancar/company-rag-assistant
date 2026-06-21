import { useState } from "react";
import api from "../api/api";

function RegisterPage({ onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");

  const register = async () => {
    try {
      await api.post("/auth/register", {
        full_name: fullName,
        email,
        password,
      });

      alert("Kayıt başarılı.");
      onSwitch();
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Kayıt başarısız."
      );
    }
  };

  return (
    <div className="auth-card">
      <h2>Hesap Oluştur</h2>

      <input
        placeholder="Ad Soyad"
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
      />

      <input
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

      <button onClick={register}>
        Kayıt Ol
      </button>

      <p>
        Zaten hesabın var mı?
        <span
          className="link-btn"
          onClick={onSwitch}
        >
          Giriş Yap
        </span>
      </p>
    </div>
  );
}

export default RegisterPage;
