/**
 * Race Entity API
 * Entities layer
 */

import { apiClient, API_ENDPOINTS } from '../../../shared/api/index.js';

export const raceApi = {
  // Получить все состязания
  async getRaces() {
    return await apiClient.get(API_ENDPOINTS.RACES);
  },

  // Получить состязание с участниками (Функция 1 из ТЗ)
  async getRaceWithParticipants(raceId) {
    return await apiClient.get(API_ENDPOINTS.RACE_BY_ID(raceId));
  },

  // Создать новое состязание (Функция 2 из ТЗ)
  async createRace(data) {
    return await apiClient.post(API_ENDPOINTS.RACES, data);
  },
};
