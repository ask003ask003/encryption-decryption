import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const useAuth = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const accessToken = sessionStorage.getItem('accessToken');
        console.log(accessToken);
        console.log("inside");
        if (!accessToken) {
            navigate('/login');
        }
    }, [navigate]);

    return true; // You can return any data you need for your component
};

export default useAuth;
