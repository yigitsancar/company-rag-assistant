import { useState } from "react";
import api from "../api/api";

function DocumentsPage({ token, role }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [documents, setDocuments] = useState([]);

  const authHeaders = {
    Authorization: `Bearer ${token}`,
  };

  const loadDocuments = async () => {
    try {
      const response = await api.get("/documents", {
        headers: authHeaders,
      });

      setDocuments(response.data);
      setMessage("Belgeler yüklendi.");
    } catch (error) {
      setMessage("Belgeler alınamadı.");
    }
  };

  const uploadDocument = async () => {
    if (!file) {
      setMessage("Dosya gerekli.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/documents/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          ...authHeaders,
        },
      });

      setMessage(
        `${response.data.filename} yüklendi. Chunk: ${response.data.chunk_count}`
      );

      setFile(null);
      loadDocuments();
    } catch (error) {
      setMessage("Yükleme başarısız.");
    }
  };

  const deleteDocument = async (documentId) => {

    const confirmDelete = window.confirm(
      "Bu belgeyi silmek istediğine emin misin?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`/documents/${documentId}`, {
        headers: authHeaders,
      });

      setMessage("Belge silindi.");
      loadDocuments();
    } catch (error) {
      setMessage("Belge silinemedi.");
    }
  };

  return (
    <section className="card">
      <h2>Belge Yönetimi</h2>

      <div className="upload-row">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadDocument}>Belge Yükle</button>
      </div>

      <button className="secondary-btn" onClick={loadDocuments}>
        Belgeleri Listele
      </button>

      {message && <p className="message">{message}</p>}

      {documents.length > 0 && (
        <div className="documents-list">
          <h3>Yüklü Belgeler</h3>

          {documents.map((document) => (
            <div className="document-item" key={document.id}>
              <div>
                <strong>{document.filename}</strong>
                <small>ID: {document.id}</small>
              </div>
               <button
		 className="danger-btn"
		onClick={() => deleteDocument(document.id)}
		>
		 Sil
		</button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default DocumentsPage;
