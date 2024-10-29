import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const getToken = () => localStorage.getItem("access");
export const getRefreshToken = () => localStorage.getItem("refresh");

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Refresh token logic with URL adjustment
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if the error is due to token expiration
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Note: Adjusted URL to include baseURL manually
        const { data } = await axios.post(
          "/api/auth/refresh/", // Adjust if necessary
          { refresh: getRefreshToken() }
        );

        // Update localStorage and axios defaults
        localStorage.setItem("access", data.access);
        api.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

        // Retry the original request with the new access token
        originalRequest.headers["Authorization"] = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        clearTokens();
        window.location.href = "/login"; // Redirect to login on failure
      }
    }

    return Promise.reject(error);
  }
);

export const setTokens = (access: string, refresh: string) => {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
};

export const clearTokens = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};

export default api;
