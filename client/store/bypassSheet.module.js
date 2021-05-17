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
  async [FETCH_BYPASS_SHEETS](context, {
    bypassSheets=[],
    department=''
  }) {
    if (bypassSheets.length !== 0) {
      return context.commit(SET_BYPASS_SHEETS, bypassSheets)
    }
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const response = await BypassSheetsService.get(department)
      const data = response.data
      context.commit(SET_BYPASS_SHEETS, data)
      return data
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [UPDATE_BYPASS_SHEETS](context, {
      bypassSheets,
      department,
    }) {
    try {
      await context.dispatch(CHECK_AUTH)
      return await BypassSheetsService.patchMany({
        department,
        bypassSheets,
      })
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
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
