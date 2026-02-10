import { apiClient, API_ENDPOINTS } from '../../../shared/api/index.js';

export const participantApi = {
  async getParticipants() {
    return await apiClient.get(API_ENDPOINTS.PARTICIPANTS);
  },
  async addParticipant(data) {
    return await apiClient.post(API_ENDPOINTS.PARTICIPANTS, data);
  },
};
