import { BypassSheetsService } from '~/services/ApiService'
import {
  CHECK_AUTH,
  FETCH_BYPASS_SHEETS,
  UPDATE_BYPASS_SHEETS,
  WAIT_FOR,
} from './actions.type'
import { SET_BYPASS_SHEETS, SET_ERROR } from './mutations.type'

const state = () => ({
  bypassSheets: [],
})

const getters = {
  bypassSheets(state) {
    return state.bypassSheets
  },
}

const actions = {
  [FETCH_BYPASS_SHEETS](context, data) {
    const {
      bypassSheets: prevBypassSheets,
      department = '',
    } = data
    if (prevBypassSheets.length !== 0) {
      return context.commit(SET_BYPASS_SHEETS, prevBypassSheets)
    }
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          BypassSheetsService.get(department)
            .then(({ data }) => {
              context.commit(SET_BYPASS_SHEETS, data)
              resolve(data)
            })
            .catch(errors => {
              context.commit(SET_ERROR, errors)
              reject(errors)
            })
        })
    })
  },
  [UPDATE_BYPASS_SHEETS](context, data) {
    return new Promise((resolve, reject) => {
      const {
        department,
        bypassSheets,
      } = data
      BypassSheetsService.patchMany({
        department,
        bypassSheets,
      })
        .then(data => {
          resolve(data)
        })
        .catch(errors => {
          context.commit(SET_ERROR, errors)
          reject(errors)
        })
    })
  },
}

const mutations = {
  [SET_BYPASS_SHEETS](state, bypassSheets) {
    state.bypassSheets = bypassSheets
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
