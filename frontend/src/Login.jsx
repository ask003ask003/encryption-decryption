import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './style.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginStatus, setLoginStatus] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        sessionStorage.removeItem('accessToken');
    }, []);

    const handleLogin = async () => {
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const response = await axios.post('http://localhost:8000/token', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.status === 200) {
                const accessToken = response.data.access_token;
                sessionStorage.setItem('accessToken', accessToken);
                navigate('/upload');
            }
        } catch (error) {
            setLoginStatus('Login failed. Please try again.');
            console.error('Login error:', error);
        }
    };

    return (
        <div className="row-full-height">
            <div className="image-container"></div>
            <div className="form-container">
                <h2>Login</h2>
                <div className="mb-3">
                    <label className="form-label">Username</label>
                    <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <div className="password-toggle">
                        <input
                            type={showPassword ? "text" : "password"}
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <input
                            type="checkbox"
                            checked={showPassword}
                            onChange={() => setShowPassword(!showPassword)}
                        />
                        Show Password
                    </div>
                </div>
                <button className="btn btn-primary" onClick={handleLogin}>Login</button>
                <p>Don't have an account? <Link to="/signup">Signup</Link></p>
                {loginStatus && <div className="alert alert-info mt-3">{loginStatus}</div>}
            </div>
        </div>
    );
};

export default Login;
