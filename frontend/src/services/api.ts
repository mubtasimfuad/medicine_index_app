import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Change to production URL as needed
});

export default api;
