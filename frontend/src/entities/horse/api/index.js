import { apiClient, API_ENDPOINTS } from '../../../shared/api/index.js';

export const horseApi = {
  async getHorses() {
    return await apiClient.get(API_ENDPOINTS.HORSES);
  },
  async getHorseById(horseId) {
    return await apiClient.get(API_ENDPOINTS.HORSE_BY_ID(horseId));
  },
  async createHorse(data) {
    return await apiClient.post(API_ENDPOINTS.HORSES, data);
  },
  async getHorseRaces(horseId) {
    return await apiClient.get(API_ENDPOINTS.HORSE_RACES(horseId));
  },
};
