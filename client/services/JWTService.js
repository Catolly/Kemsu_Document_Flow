const ID_TOKEN_KEY = "id_token"

export const getToken = () => {
  if (process.browser) {
    const token = localStorage.getItem(ID_TOKEN_KEY)
    if (token && token !== 'undefined') {
      return JSON.parse(token)
    }
    else return null
  }
  else return null
}

export const saveToken = token => {
  if (process.browser) {
    localStorage.setItem(ID_TOKEN_KEY, JSON.stringify(token))
  }
}

export const destroyToken = () => {
  if (process.browser) {
    localStorage.removeItem(ID_TOKEN_KEY)
  }
}

export default { getToken, saveToken, destroyToken }
