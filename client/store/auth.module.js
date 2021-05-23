import ApiService from '~/services/ApiService'
import JwtService from '~/services/JWTService'
import UserService from '~/services/UserService'
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
  PURGE_ROLES,
  SET_AUTH,
  SET_CHECKING,
  SET_ERROR,
  SET_FULLNAME,
  SET_TOKEN,
} from './mutations.type'

import _ from 'lodash'

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
    context.commit(PURGE_ROLES)
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
          context.commit(PURGE_ROLES)
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
  async [CHECK_AUTH](context) {
    try {
      context.commit(SET_CHECKING, true)
      const tokens = JwtService.getToken()
      const id = UserService.getId()
      if (tokens && id) {
        if (!tokens.access || (tokens.expiresIn < Date.now())) {
          await context.dispatch(REFRESH, JwtService.getToken().refresh)
        }
        if (_.isEmpty(context.getters.currentUser)) {
          const user = await context.dispatch(FETCH_USER, id)
          if (user) {
            context.commit(SET_AUTH, user)
          }
        }
        context.commit(SET_CHECKING, false)
      }
      else {
        context.commit(PURGE_AUTH)
        context.commit(PURGE_ROLES)
        context.commit(SET_CHECKING, false)
      }
    } catch (error) {
      console.error(error)
      context.commit(SET_ERROR, error)
      context.commit(PURGE_AUTH)
      context.commit(PURGE_ROLES)
      context.commit(SET_CHECKING, false)
      throw error
    }
  },
  async [UPDATE_USER](context, {fullname}) {
    ApiService.setHeader()
    const user = {
      fullname
    }
    const currentUser = context.getters.currentUser
    try {
      await context.dispatch(CHECK_AUTH)
      context.commit(SET_FULLNAME, fullname)
      return await ApiService.patch(`users/${currentUser.id}/`, user)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
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
  [SET_FULLNAME](state, fullname) {
    state.user.fullname = fullname
  },
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
