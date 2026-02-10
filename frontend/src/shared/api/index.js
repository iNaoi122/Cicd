/**
 * API Configuration and HTTP Client
 * Shared layer - конфигурация доступа к Backend API
 */

// Используем относительный путь для работы в Docker и локально
const API_BASE_URL = "/api";
const API_VERSION = "v1";
const API_URL = `${API_BASE_URL}/${API_VERSION}`;

const API_ENDPOINTS = {
  // Races (Состязания)
  RACES: "/races",
  RACE_BY_ID: (id) => `/races/${id}`,

  // Jockeys (Жокеи)
  JOCKEYS: "/jockeys",
  JOCKEY_BY_ID: (id) => `/jockeys/${id}`,
  JOCKEY_RACES: (id) => `/jockeys/${id}/races`,

  // Horses (Лошади)
  HORSES: "/horses",
  HORSE_BY_ID: (id) => `/horses/${id}`,
  HORSE_RACES: (id) => `/horses/${id}/races`,

  // Owners (Владельцы)
  OWNERS: "/owners",
  OWNER_BY_ID: (id) => `/owners/${id}`,

  // Participants (Участники)
  PARTICIPANTS: "/participants",
};

const API_TIMEOUT = 10000;

/**
 * Простой HTTP клиент
 */
class ApiClient {
  constructor(baseURL, timeout = 10000) {
    this.baseURL = baseURL;
    this.timeout = timeout;
    this.cache = new Map();
  }

  async request(method, endpoint, data = null) {
    const url = `${this.baseURL}${endpoint}`;
    const cacheKey = `${method}:${url}`;

    // Кеширование для GET запросов
    if (method === "GET" && this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    const options = {
      method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (data && (method === "POST" || method === "PUT")) {
      options.body = JSON.stringify(data);
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      options.signal = controller.signal;

      const response = await fetch(url, options);
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();

      // Кешируем GET запросы
      if (method === "GET") {
        this.cache.set(cacheKey, result);
      }

      return result;
    } catch (error) {
      console.error("API Request Error:", error);
      throw error;
    }
  }

  get(endpoint) {
    return this.request("GET", endpoint);
  }

  post(endpoint, data) {
    this.invalidateCache();
    return this.request("POST", endpoint, data);
  }

  put(endpoint, data) {
    this.invalidateCache();
    return this.request("PUT", endpoint, data);
  }

  invalidateCache() {
    this.cache.clear();
  }
}

const apiClient = new ApiClient(API_URL, API_TIMEOUT);

export { API_URL, API_ENDPOINTS, apiClient };
