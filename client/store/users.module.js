import ApiService, { UsersService } from '~/services/ApiService'
import {
  CHECK_AUTH,
  FETCH_USERS,
  BAN_USER,
  UNBAN_USER,
  WAIT_FOR,
} from './actions.type'
import { SET_USERS, SET_USERS_AMOUNT, SET_ERROR } from './mutations.type'

const state = () => ({
  users: [],
  usersAmount: 0,
})

const getters = {
  users(state) {
    return state.users
  },
  usersAmount(state) {
    return state.usersAmount
  },
}

const actions = {
  async [FETCH_USERS](context, {
    bypassSheet='',
    point='',
    search='',
    institute='',
    course='',
    group='',
    offset='',
    limit='',
  }) {
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      await context.dispatch(CHECK_AUTH)
      const { data } = await UsersService.get({
        title: bypassSheet,
        pointTitle: point,
        search,
        institute,
        course,
        group,
        offset,
        limit,
      })
      const { students, studentsAmount } = data
      context.commit(SET_USERS, students)
      context.commit(SET_USERS_AMOUNT, studentsAmount)
      return students
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
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
  [SET_USERS_AMOUNT](state, usersAmount) {
    state.usersAmount = usersAmount
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
