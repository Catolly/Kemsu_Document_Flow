import { BypassSheetsService } from '~/services/ApiService'
import {
  CHECK_AUTH,
  CREATE_BYPASS_SHEET,
  FETCH_BYPASS_SHEETS,
  UPDATE_BYPASS_SHEET,
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
  async [UPDATE_BYPASS_SHEET](context, {
    point,
    id, //id листа
  }) {
    try {
      await context.dispatch(CHECK_AUTH)

      const formData = new FormData()
      formData.append('title', point.title)
      point.uploadedDocuments.forEach(file => {
        formData.append('uploadedDocuments', file)
      })

      return await BypassSheetsService.patch(id, formData)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
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

      const formData = new FormData()
      bypassSheets.forEach((sheet, index) => {
        [
          'status',
          'rejectReason',
          'staff',
        ].forEach(propName => {
          formData.append(
            ` [${index}]${propName}`, sheet[propName])
        })
        formData.append(
          ` [${index}]id`, sheet.bypassSheetId)
        if (sheet.requiredDocuments)
          sheet.requiredDocuments.forEach((file, fileIndex) => {
            formData.append(
              ` [${index}]requiredDocuments[${fileIndex}]`, file)
          })
      })

      return await BypassSheetsService.patchMany({
        department,
        data: formData,
      })
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [CREATE_BYPASS_SHEET](context, {
      title,
      statements
    }) {
    try {
      await context.dispatch(CHECK_AUTH)

      const formData = new FormData()
      statements.forEach(file => {
        formData.append('statements', file)
      })
      formData.append('title', title)

      return await BypassSheetsService.post(formData)
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
