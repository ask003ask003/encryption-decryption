import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './style.css';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [signupStatus, setSignupStatus] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleSignup = async () => {
        try {
            const response = await axios.post('http://localhost:8000/register', { email, username, password });
            if (response.status === 200) {
                setSignupStatus('Signup successful! Redirecting to login...');
                setTimeout(() => {
                    navigate('/login');
                }, 1500);
            }
        } catch (error) {
            setSignupStatus('Signup failed. Please try again.');
            console.error('Signup error:', error);
        }
    };

    return (
        <div className="row-full-height">
            <div className="image-container"></div>
            <div className="form-container">
                <h2>Signup</h2>
                <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
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
                <button className="btn btn-primary" onClick={handleSignup}>Signup</button>
                <p>Already have an account? <Link to="/login">Login</Link></p>
                {signupStatus && <div className="alert alert-info mt-3">{signupStatus}</div>}
            </div>
        </div>
    );
};

export default Signup;
