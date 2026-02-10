import { apiClient, API_ENDPOINTS } from '../../../shared/api/index.js';

export const jockeyApi = {
  async getJockeys() {
    return await apiClient.get(API_ENDPOINTS.JOCKEYS);
  },
  async getJockeyById(jockeyId) {
    return await apiClient.get(API_ENDPOINTS.JOCKEY_BY_ID(jockeyId));
  },
  async createJockey(data) {
    return await apiClient.post(API_ENDPOINTS.JOCKEYS, data);
  },
  async getJockeyRaces(jockeyId) {
    return await apiClient.get(API_ENDPOINTS.JOCKEY_RACES(jockeyId));
  },
};
