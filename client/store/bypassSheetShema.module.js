import { BypassSheetsSchemasService } from '~/services/ApiService'
import bypassSheetSchema from '~/services/bypassSheetSchema'
import {
  FETCH_BYPASS_SHEETS_SCHEMAS,
  FETCH_BYPASS_SHEETS_SCHEMA,
  CREATE_BYPASS_SHEETS_SCHEMA,
  UPDATE_BYPASS_SHEETS_SCHEMA,
  WAIT_FOR,
} from './actions.type'
import {
  SET_BYPASS_SHEETS_SCHEMAS,
  SET_BYPASS_SHEETS_SCHEMA,
  SET_ERROR
} from './mutations.type'

const genderReqValues = bypassSheetSchema.genderReqValues

const state = () => ({
  bypassSheetsSchemas: [],
  bypassSheetsSchema: null,
})

const getters = {
  bypassSheetsSchemas(state) {
    return state.bypassSheetsSchemas
  },
  bypassSheetsSchema(state) {
    return state.bypassSheetsSchema
  },
}

const actions = {
  [FETCH_BYPASS_SHEETS_SCHEMAS](context, data) {
    const {
      bypassSheetsSchemas: prevBypassSheetsSchemas,
      department,
    } = data
    if (prevBypassSheetsSchemas.length !== 0) {
      return context.commit(SET_BYPASS_SHEETS_SCHEMAS, prevBypassSheetsSchemas)
    }
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          BypassSheetsSchemasService.get(department || '')
            .then(({ data }) => {
              context.commit(SET_BYPASS_SHEETS_SCHEMAS, data)
              resolve(data)
            })
            .catch(error => {
              context.commit(SET_ERROR, error)
              reject(error)
            })
        })
    })
  },
  async [FETCH_BYPASS_SHEETS_SCHEMA](context, {id, prevSchema=null}) {
    if (prevSchema) {
      context.commit(SET_BYPASS_SHEETS_SCHEMA, prevSchema)
      return prevSchema
    }
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const { data: schema } = await BypassSheetsSchemasService.get(id)
      context.commit(SET_BYPASS_SHEETS_SCHEMA, JSON.parse(JSON.stringify(schema)))
      return schema
    } catch (error) {
      context.commit(SET_ERROR, error)
      return error
    }
  },
  async [CREATE_BYPASS_SHEETS_SCHEMA](context, data) {
    data.points = data.points
      .map(point => ({
        title: point.title,
        description: point.description,
        requiredDocuments: point.requiredDocuments,
        gender: genderReqValues[point.gender],
        uploadDocumentsFormat: point.uploadDocumentsFormat
          .filter(doc => doc.title)
          .map(doc => ({
            title: doc.title,
          })),
      }))

    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      return await BypassSheetsSchemasService.post(data)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [UPDATE_BYPASS_SHEETS_SCHEMA](context, data) {
    data.points = data.points
      .map(point => ({
        title: point.title,
        description: point.description,
        requiredDocuments: point.requiredDocuments,
        gender: genderReqValues[point.gender],
        uploadDocumentsFormat: point.uploadDocumentsFormat
          .filter(doc => doc.title)
          .map(doc => ({
            title: doc.title,
          })),
      }))

    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      return await BypassSheetsSchemasService.patch(data)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
}

const mutations = {
  [SET_BYPASS_SHEETS_SCHEMAS](state, bypassSheetsSchemas) {
    state.bypassSheetsSchemas = bypassSheetsSchemas
  },
  [SET_BYPASS_SHEETS_SCHEMA](state, bypassSheetsSchema) {
    state.bypassSheetsSchema = bypassSheetsSchema
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
