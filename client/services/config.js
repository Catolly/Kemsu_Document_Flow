export const BASE_URL = process.env.NODE_ENV === 'production'
                                              ? 'http://mydoc.kemsu.ru'
                                              : 'http://25.35.74.172:8000'
export const API_URL = `${BASE_URL}/api/`
export const REQUEST_TIMEOUT = 60*1000*1000

export const debounceDelay = 1500
export const throttleDelay = 500
export const adminEmail = 'mydockemsu@gmail.com'
export const telegramHelpUrl = 'https://t.me/kemsu_mydoc_help'
