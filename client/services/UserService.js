const ID_USER_ID_KEY = "id_user_id"

export const getId = () => {
  if (process.browser) {
    const id = localStorage.getItem(ID_USER_ID_KEY)
    if (id && id !== 'undefined') {
      return JSON.parse(id)
    }
    else return null
  }
  else return null
}

export const saveId = id => {
  if (process.browser) {
    localStorage.setItem(ID_USER_ID_KEY, JSON.stringify(id))
  }
}

export const destroyId = () => {
  if (process.browser) {
    localStorage.removeItem(ID_USER_ID_KEY)
  }
}

export default { getId, saveId, destroyId }
