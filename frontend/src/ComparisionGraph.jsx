import React from 'react';
import { Link } from 'react-router-dom';
import tableImage from './table.png';
import graphImage from './graph.png';
import './ComparisionGraph.css';

const ComparisonGraph = () => {
    return (
        <div className="container mt-5">
            <h2 className="mb-4">Algorithm Comparison</h2>
            <img src={tableImage} alt="Algorithm Comparison Table" className="small-image img-fluid mb-4" />
            <img src={graphImage} alt="Algorithm Comparison Graph" className="large-image img-fluid mb-4" />

            <div className="algorithm-info">
                <h3>AES (Advanced Encryption Standard)</h3>
                <p>
                    AES is a symmetric encryption algorithm standardized by NIST. It encrypts data in fixed blocks of 128 bits using keys of 128, 192, or 256 bits. AES operates on a 4x4 column-major order matrix of bytes.
                </p>
                <p><strong>Formula:</strong> <code>C = E_k(P)</code>, where <code>C</code> is the ciphertext, <code>P</code> is the plaintext, and <code>E_k</code> is the encryption function with key <code>k</code>.</p>

                <h3>DES (Data Encryption Standard)</h3>
                <p>
                    DES is a symmetric-key algorithm for the encryption of digital data. It uses a 56-bit key and operates on 64-bit blocks. DES has been largely superseded by AES due to its shorter key length and vulnerabilities.
                </p>
                <p><strong>Formula:</strong> <code>C = E_k(P)</code>, where <code>C</code> is the ciphertext, <code>P</code> is the plaintext, and <code>E_k</code> is the encryption function with key <code>k</code>.</p>

                <h3>RSA (Rivest–Shamir–Adleman)</h3>
                <p>
                    RSA is an asymmetric encryption algorithm widely used for secure data transmission. It uses a pair of keys, a public key for encryption, and a private key for decryption. RSA relies on the mathematical difficulty of factoring large prime numbers.
                </p>
                <p><strong>Formula:</strong> <code>C = P^e \mod n</code> and <code>P = C^d \mod n</code>, where <code>(e, n)</code> is the public key and <code>(d, n)</code> is the private key.</p>
            </div>

            <Link to="/upload" className="btn btn-secondary mt-3">Back to File Upload</Link>
        </div>
    );
};

export default ComparisonGraph;
