import axios, { AxiosInstance } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TaskCreateRequest {
  title: string;
  description: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskResponse {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export const register = (data: RegisterRequest) => {
  return api.post('/api/auth/register', data);
};

export const login = (data: LoginRequest) => {
  return api.post('/api/auth/login', data);
};

export const createTask = (data: TaskCreateRequest) => {
  return api.post<TaskResponse>('/api/tasks', data);
};

export const listTasks = () => {
  return api.get<TaskResponse[]>('/api/tasks');
};

export const updateTask = (id: number, data: TaskUpdateRequest) => {
  return api.put<TaskResponse>(`/api/tasks/${id}`, data);
};

export const deleteTask = (id: number) => {
  return api.delete<void>(`/api/tasks/${id}`);
};

export default api;

// Auto-added stubs for functions a page imported but the client omitted.
export const getTask = async (id: string) => {
  const res = await api.get(`/api/tasks/${id}`);
  return res.data;
};
