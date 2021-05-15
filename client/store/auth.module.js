import ApiService from '~/services/ApiService'
import JwtService from '~/services/JWTService'
import UserService from '~/services/UserService'
import Role from '~/services/role'
import {
  LOGIN,
  LOGOUT,
  SIGNUP_STUDENT,
  SIGNUP_STAFF,
  CHECK_AUTH,
  CHECK_ROLE,
  REFRESH,
  FETCH_USER,
  UPDATE_USER,
  WAIT_FOR,
} from './actions.type'
import {
  PURGE_AUTH,
  SET_AUTH,
  SET_TOKEN,
  SET_CHECKING,
  SET_ERROR,
} from './mutations.type'

const state = () => ({
  errors: null,
  user: {},
  isAuthenticated: !!JwtService.getToken(),
  checkingAuth: false,
})

const getters = {
  currentUser(state) {
    return state.user
  },
  isAuthenticated(state) {
    return state.isAuthenticated
  },
  checkingAuth(state) { // идет ли сейчас процесс аутентификации пользователя
    return state.checkingAuth
  },
}

const actions = {
  [LOGIN](context, credentials) {
    return new Promise((resolve, reject) => {
      ApiService.post('login/', credentials)
        .then(({ data }) => {
          context.commit(SET_AUTH, data)
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
  [LOGOUT](context) {
    context.commit(PURGE_AUTH)
  },
  [SIGNUP_STUDENT](context, credentials) {
    return new Promise((resolve, reject) => {
      ApiService.post('signup/student/', credentials)
        .then(({ data }) => {
          context.commit(SET_AUTH, data)
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
  [SIGNUP_STAFF](context, credentials) {
    return new Promise((resolve, reject) => {
      ApiService.post('signup/staff/', credentials)
        .then(({ data }) => {
          context.commit(SET_AUTH, data)
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
  [REFRESH](context, token){
    return new Promise((resolve, reject) => {
      ApiService.setHeader()
      ApiService.post('token/refresh/', { 'refresh': token })
        .then(({ data }) => {
          context.commit(SET_TOKEN, data.tokens)
          resolve(data.tokens)
        })
        .catch(errors => {
          context.commit(PURGE_AUTH)
          reject(errors)
        })
    })
  },
  [FETCH_USER](context, id) {
    return new Promise((resolve, reject) => {
      ApiService.setHeader()
      ApiService.get(`users/${id}`)
        .then(({ data }) => {
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
  [CHECK_AUTH](context) {
    return new Promise((resolve, reject) => {
      context.commit(SET_CHECKING, true)
      const tokens = JwtService.getToken()
      const id = UserService.getId()
      if (tokens && id) {
        if (tokens.access) {
          if (tokens.expiresIn > Date.now()) {
            context.dispatch(FETCH_USER, id)
              .then(data => {
                if (data)
                  context.commit(SET_AUTH, data.user)
                else
                  context.commit(SET_TOKEN, tokens)
                resolve(data)
              })
              .catch(errors => {
                context.commit(SET_ERROR, errors)
                reject(errors)
              })
              .finally(() => {
                context.commit(SET_CHECKING, false)
              })

          } else {
            context.dispatch(REFRESH, JwtService.getToken().refresh)
              .then(data => {
                resolve(data)
              })
              .catch(errors => {
                context.commit(SET_ERROR, errors)
                reject(errors)
              })
              .finally(() => {
                context.commit(SET_CHECKING, false)
              })
          }
        }
      } else {
        context.commit(PURGE_AUTH)
        resolve()
        context.commit(SET_CHECKING, false)
      }
    })
  },
  [UPDATE_USER](context, payload) {
    return new Promise((resolve, reject) => {
      ApiService.setHeader()
      const { fullname } = payload
      const user = {
        fullname
      }
      const currentUser = context.getters.currentUser
      ApiService.patch(`users/${currentUser.id}`, user)
        .then(data => {
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
  [WAIT_FOR](context, getterName) {
    return new Promise(resolve => {
      const checkFlag = getterName => {
        const flag = !context.getters[getterName]
        if (flag) {
          resolve(flag)
        }
        else setTimeout(() => {
          checkFlag(getterName)
        }, 100)
      }
      checkFlag(getterName)
    })
  },
}

const mutations = {
  [SET_ERROR](state, error) {
    state.errors = error
  },
  [SET_AUTH](state, {tokens = null, ...user}) {
    state.isAuthenticated = true
    state.user = user
    state.errors = ''

    UserService.saveId(user.id)
    if (tokens)
      JwtService.saveToken(tokens)
  },
  [SET_TOKEN](state, tokens) {
    state.isAuthenticated = true
    state.errors = ''
    JwtService.saveToken(tokens)
  },
  [SET_CHECKING](state, checking) {
    state.checkingAuth = checking
  },
  [PURGE_AUTH](state) {
    state.isAuthenticated = false
    state.user = {}
    state.errors = ''
    UserService.destroyId()
    JwtService.destroyToken()
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
