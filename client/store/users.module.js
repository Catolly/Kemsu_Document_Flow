import { UsersService } from '~/services/ApiService'
// import Role from '~/services/role'
import {
  CHECK_AUTH,
  // CHECK_ROLE,
  FETCH_USERS,
  // UPDATE_BYPASS_SHEETS
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
  [FETCH_USERS](context, params) {
    const {
      users: prevUsers,
      bypassSheetName,
      pointName,
      offset,
      limit,
    } = params
    if (prevUsers.length !== 0) {
      return context.commit(SET_USERS, prevUsers)
    }
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          UsersService.get({
            bypassSheetName,
            pointName,
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
