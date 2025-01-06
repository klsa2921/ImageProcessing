import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setOutput('');  // Clear the output when a new file is selected
    setError('');  // Clear any previous error messages
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');
    setOutput('');

    try {
      const response = await axios.post('http://192.168.1.249:11200/extract_text', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setLoading(false);
      if (response.data.text) {
        setOutput(response.data.text);  // Display only the extracted text
      } else {
        setError('No text extracted from the file.');
      }
    } catch (err) {
      setLoading(false);
      setError('Error uploading file. Please try again.');
    }
  };

  return (
    <div>
      <h1>File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {output && (
        <div>
          <h3>Extracted Text:</h3>
          <pre>{output}</pre> {/* Display extracted text */}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
