// api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Adjust as needed for production
});

const getToken = () => localStorage.getItem('access');
const getRefreshToken = () => localStorage.getItem('refresh');

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
export const searchMedicines = async (query: string) => {
  const response = await api.get('/medicines/search/', { params: { q: query } });
  return response.data.data;  // Ensure it matches the expected response structure
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const { data } = await axios.post('/refresh/', {
          refresh: getRefreshToken(),
        });
        localStorage.setItem('access', data.access);  // Update the access token
        api.defaults.headers.common.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.clear();  // Clear tokens on failure
        window.location.href = '/login';  // Redirect to login
      }
    }
    return Promise.reject(error);
  }
);

export const setTokens = (access: string, refresh: string) => {
  localStorage.setItem('access', access);
  localStorage.setItem('refresh', refresh);
};

export const clearTokens = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};

export default api;
