const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
      
      if (response.status === 401) {
        // Token expirado ou inválido
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_email');
        window.location.href = '/login';
        return;
      }
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
        throw new Error(errorData.detail || `Erro ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },
  
  // Métodos específicos
  async login(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro no login');
    }
    
    return await response.json();
  },
  
  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
  
  async createProduct(productData) {
    return this.request('/products/', {
      method: 'POST',
      body: JSON.stringify(productData),
    });
  },
  
  async generateEpics(data) {
    return this.request('/llm-project/generate-epics', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  async generateUserStories(data) {
    return this.request('/llm-project/generate-user-stories', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  async generateRequirements(data) {
    return this.request('/llm-project/generate-requirements', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
}; 