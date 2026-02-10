import { apiClient, API_ENDPOINTS } from '../../../shared/api/index.js';

export const ownerApi = {
  async getOwners() {
    return await apiClient.get(API_ENDPOINTS.OWNERS);
  },
  async getOwnerById(ownerId) {
    return await apiClient.get(API_ENDPOINTS.OWNER_BY_ID(ownerId));
  },
  async createOwner(data) {
    return await apiClient.post(API_ENDPOINTS.OWNERS, data);
  },
};
