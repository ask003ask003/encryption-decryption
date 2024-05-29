import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Signup from './Signup';
import Login from './Login';
import FileUpload from './FileUpload';
import ComparisonGraph from './ComparisionGraph';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    return (
        <Router>
            <div className="container mt-5">
                <Routes>
                    <Route path="/signup" element={<Signup />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/upload" element={<FileUpload />} />
                    <Route path="/comparison" element={<ComparisonGraph />} />
                    <Route path="*" element={<Navigate to="/signup" />} />

                </Routes>
            </div>
        </Router>
    );
};

export default App;
