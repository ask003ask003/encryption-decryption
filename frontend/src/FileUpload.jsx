import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';
import useAuth from './useAuth';
import './FileUpload.css';

const FileUpload = () => {
    useAuth();
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [encryptionMethod, setEncryptionMethod] = useState('rsa');
    const [chatInput, setChatInput] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [fileContent, setFileContent] = useState('');

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleMethodChange = (event) => {
        setEncryptionMethod(event.target.value);
    };

    const handleUpload = async (action) => {
        if (!selectedFile) {
            setUploadStatus('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        const endpoint = action === 'encrypt'
            ? `http://localhost:8000/encrypt/${encryptionMethod}`
            : `http://localhost:8000/decrypt/${encryptionMethod}`;

        try {
            const response = await axios.post(endpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob'
            });

            const blob = new Blob([response.data]);
            const text = await blob.text();

            console.log(text);
            if (text == '\"Hashed succesfully\"') {
                setUploadStatus(`hashed successfully`);
            }
            else
                if (text == '\"match\"') {
                    setUploadStatus(`match`);
                }
                else
                    if (text == '\"mismatch\"') {
                        setUploadStatus(`mismatch`);
                    }
                    else
                        if (text === '\"error decrypting\"') {
                            setUploadStatus(`Error ${action}ing file`);
                        } else {
                            const url = window.URL.createObjectURL(blob);
                            const link = document.createElement('a');
                            link.href = url;

                            const contentDisposition = response.headers['content-disposition'];
                            let filename = action === 'encrypt' ? 'encrypted_file.txt' : 'decrypted_file.txt';
                            if (contentDisposition) {
                                const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
                                if (filenameMatch.length === 2) {
                                    filename = filenameMatch[1];
                                }
                            }

                            link.setAttribute('download', filename);
                            document.body.appendChild(link);
                            link.click();
                            link.remove();

                            setUploadStatus(`File ${action}ed successfully. Download should start automatically.`);
                            setFileContent(''); // Clear any previous error messages
                        }
        } catch (error) {
            setUploadStatus(`Error ${action}ing file`);
            console.error(`Error ${action}ing file:`, error);
        }
    };

    const handleChatSubmit = async (event) => {
        event.preventDefault();
        if (!chatInput) return;

        try {
            const response = await axios.post(`http://localhost:8000/post-query/${chatInput}`);

            const newChat = { user: chatInput, bot: response.data.Chatbot };
            setChatHistory([...chatHistory, newChat]);
            setChatInput('');
        } catch (error) {
            console.error('Error in chat:', error);
        }
    };

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container-fluid">
                    <Link className="navbar-brand" to="/">Encrypt/Decrypt App</Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <Link className="nav-link" to="/comparison">View Comparison Graph</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/logout">Logout</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div className="container mt-5">
                <div className="row">
                    <div className="col-md-8">
                        <h2 className="mb-4">File Upload</h2>
                        <div className="mb-3">
                            <input className="form-control" type="file" onChange={handleFileChange} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Select Encryption Method:</label>
                            <select className="form-select" onChange={handleMethodChange} value={encryptionMethod}>
                                <option value="rsa">RSA</option>
                                <option value="aes">AES</option>
                                <option value="des">DES</option>
                                <option value="sha256">sha256</option>
                            </select>
                        </div>
                        <div className="mb-3">
                            <button className="btn btn-primary me-2" onClick={() => handleUpload('encrypt')}>Encrypt and Upload</button>
                            <button className="btn btn-secondary me-2" onClick={() => handleUpload('decrypt')}>Decrypt and Upload</button>
                        </div>
                        {uploadStatus && <div className="alert alert-info mt-3">{uploadStatus}</div>}
                        {fileContent && <div className="alert alert-danger mt-3">{fileContent}</div>}
                    </div>
                    <div className="col-md-4">
                        <h2 className="mb-4">Chatbot</h2>
                        <div className="chat-history mb-3">
                            {chatHistory.map((chat, index) => (
                                <div key={index} className="chat-message">
                                    <div className="user-message"><strong>User:</strong> {chat.user}</div>
                                    <div className="bot-message"><strong>Bot:</strong> {chat.bot}</div>
                                </div>
                            ))}
                        </div>
                        <form onSubmit={handleChatSubmit}>
                            <div className="mb-3">
                                <input
                                    className="form-control"
                                    type="text"
                                    value={chatInput}
                                    onChange={(e) => setChatInput(e.target.value)}
                                    placeholder="Ask something..."
                                />
                            </div>
                            <button type="submit" className="btn btn-primary">Send</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FileUpload;
