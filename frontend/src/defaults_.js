import { apiClient } from "./axios"
export const PHOTO_URL_PREFIX = apiClient.defaults.baseURL + '/'
export const DEFAULT_PHOTO_URL = 'https://api.dicebear.com/6.x/lorelei/svg?seed='
export const DEFAULT_PROFILE_PHOTO_SIZE = 150