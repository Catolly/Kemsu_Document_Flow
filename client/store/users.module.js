import ApiService, { UsersService } from '~/services/ApiService'
import {
  CHECK_AUTH,
  FETCH_USERS,
  BAN_USER,
  UNBAN_USER,
  WAIT_FOR,
} from './actions.type'
import { SET_USERS, SET_ERROR } from './mutations.type'

const state = () => ({
  users: [],
})

const getters = {
  users(state) {
    return state.users
  },
}

const actions = {
  [FETCH_USERS](context, {
      bypassSheet='',
      point='',
      offset='',
      limit='',
    }) {
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          UsersService.get({
            title: bypassSheet,
            pointTitle: point,
            offset,
            limit,
          })
            .then(({ data })=> {
              context.commit(SET_USERS, data)
              resolve(data)
            })
            .catch(errors => {
              context.commit(SET_ERROR, errors)
              reject(errors)
            })
        })
    })
  },
  async [BAN_USER](context, id) {
    try {
      await context.dispatch(CHECK_AUTH)
      await ApiService.post(`ban/${id}/`)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [UNBAN_USER](context, id) {
    try {
      await context.dispatch(CHECK_AUTH)
      await ApiService.post(`unban/${id}`)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
}

const mutations = {
  [SET_USERS](state, users) {
    state.users = users
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
