export const BASE_URL = process.env.NODE_ENV === 'production'
                                              ? 'http://mydoc.kemsu.ru'
                                              : 'http://25.35.74.172:8000'
export const API_URL = `${BASE_URL}/api/`

export const debounceDelay = 1500
export const adminEmail = 'admin@email.com'
