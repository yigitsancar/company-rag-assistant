import { useState } from "react";
import api from "../api/api";

function UsersPage({ token }) {
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");

  const authHeaders = {
    Authorization: `Bearer ${token}`,
  };

  const loadUsers = async () => {
    try {
      const response = await api.get("/users", {
        headers: authHeaders,
      });

      setUsers(response.data);
      setMessage("Kullanıcılar yüklendi.");
    } catch (error) {
      setMessage("Kullanıcılar alınamadı.");
    }
  };

  const updateRole = async (userId, role) => {
    try {
      await api.patch(
        `/users/${userId}/role`,
        { role },
        { headers: authHeaders }
      );

      setMessage("Rol güncellendi.");
      loadUsers();
    } catch (error) {
      setMessage("Rol güncellenemedi.");
    }
  };

  const deleteUser = async (userId) => {
    const confirmDelete = window.confirm(
      "Bu kullanıcıyı silmek istediğine emin misin?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`/users/${userId}`, {
        headers: authHeaders,
      });

      setMessage("Kullanıcı silindi.");
      loadUsers();
    } catch (error) {
      setMessage("Kullanıcı silinemedi.");
    }
  };

  return (
    <section className="card">
      <h2>Kullanıcı Yönetimi</h2>

      <button onClick={loadUsers}>Kullanıcıları Listele</button>

      {message && <p className="message">{message}</p>}

      <div className="users-list">
        {users.map((user) => (
          <div className="user-item" key={user.id}>
            <div>
              <strong>{user.email}</strong>
              <small>ID: {user.id}</small>
            </div>

            <select
              value={user.role}
              onChange={(e) => updateRole(user.id, e.target.value)}
            >
              <option value="ADMIN">ADMIN</option>
              <option value="MANAGER">MANAGER</option>
              <option value="EMPLOYEE">EMPLOYEE</option>
            </select>

            <button
              className="danger-btn"
              onClick={() => deleteUser(user.id)}
            >
              Sil
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}

export default UsersPage;
