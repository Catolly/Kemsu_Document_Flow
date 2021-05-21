import { BypassSheetsSchemasService } from '~/services/ApiService'
import bypassSheetSchema from '~/services/bypassSheetSchema'
import {
  FETCH_BYPASS_SHEETS_SCHEMA,
  FETCH_BYPASS_SHEETS_SCHEMAS,
  FETCH_BYPASS_SHEETS_SCHEMAS_TITLES,
  CREATE_BYPASS_SHEETS_SCHEMA,
  UPDATE_BYPASS_SHEETS_SCHEMA,
  DELETE_BYPASS_SHEETS_SCHEMA,
  WAIT_FOR,
  CHECK_AUTH,
} from './actions.type'
import {
  SET_BYPASS_SHEETS_SCHEMA,
  SET_BYPASS_SHEETS_SCHEMAS,
  SET_BYPASS_SHEETS_SCHEMAS_TITLES,
  SET_ERROR
} from './mutations.type'

const genderReqValues = bypassSheetSchema.genderReqValues

const state = () => ({
  bypassSheetsSchemas: [],
  bypassSheetsSchema: null,
  bypassSheetsSchemasTitles: [],
})

const getters = {
  bypassSheetsSchemas(state) {
    return state.bypassSheetsSchemas
  },
  bypassSheetsSchema(state) {
    return state.bypassSheetsSchema
  },
  bypassSheetsSchemasTitles(state) {
    return state.bypassSheetsSchemasTitles
  },
}

const actions = {
  async [FETCH_BYPASS_SHEETS_SCHEMAS](context, department='') {
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const response = await BypassSheetsSchemasService.getMany(department)
      const data = response.data
      context.commit(SET_BYPASS_SHEETS_SCHEMAS, data)
      return data
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [FETCH_BYPASS_SHEETS_SCHEMA](context, {
      id,
      prevSchema=null
    }) {
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const { data: schema } = await BypassSheetsSchemasService.get(id)
      context.commit(SET_BYPASS_SHEETS_SCHEMA, JSON.parse(JSON.stringify(schema)))
      return schema
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [FETCH_BYPASS_SHEETS_SCHEMAS_TITLES](context, {
      educationForm,
    }) {
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const {
        data: schemasTitles
      } = await BypassSheetsSchemasService.getTitles(educationForm)
      context.commit(SET_BYPASS_SHEETS_SCHEMAS_TITLES, schemasTitles)
      return schemasTitles
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [CREATE_BYPASS_SHEETS_SCHEMA](context, data) {
    try {
      await context.dispatch(CHECK_AUTH)

      data.points = data.points
        .map(point => ({
          title: point.title,
          description: point.description,
          requiredDocuments: point.requiredDocuments,
          commonReasons: point.commonReasons,
          gender: genderReqValues[point.gender],
          uploadDocumentsFormat: point.uploadDocumentsFormat
            .filter(doc => doc.title)
            .map(doc => ({
              title: doc.title,
            }))
        }))

      const formData = new FormData()
      formData.append('title', data.title)
      formData.append('educationForm', data.educationForm)
      data.studentList.forEach(id => {
        formData.append('studentList', id)
      })
      data.statements.forEach(file => {
        formData.append('statements', file)
      })

      data.points.
        forEach((point, index) => {
          formData.append(
            `points[${index}]title`,
            point.title
          )
          formData.append(
            `points[${index}]description`,
            point.description
          )
          formData.append(
            `points[${index}]gender`,
            point.gender
          )
          point.uploadDocumentsFormat
            .forEach((format, fileIndex) => {
              formData.append(`points[${index}]uploadDocumentsFormat[${fileIndex}]title`,
               format.title)
            })
          point.commonReasons
            .forEach((reason, fileIndex) => {
              formData.append(`points[${index}]commonReasons[${fileIndex}]`, reason)
            })
          point.requiredDocuments
            .forEach((file, fileIndex) => {
              formData.append(
                `points[${index}]requiredDocuments[${fileIndex}]`, file)
            })
        })

      return await BypassSheetsSchemasService.post(formData)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [UPDATE_BYPASS_SHEETS_SCHEMA](context, data) {
    try {
      await context.dispatch(CHECK_AUTH)

      data.points = data.points
        .map(point => ({
          id: point.id,
          title: point.title,
          description: point.description,
          requiredDocuments: point.requiredDocuments,
          commonReasons: point.commonReasons,
          gender: genderReqValues[point.gender],
          uploadDocumentsFormat: point.uploadDocumentsFormat
            .filter(doc => doc.title)
            .map(doc => ({
              title: doc.title,
            })),
        }))

      const formData = new FormData()
      formData.append('title', data.title)
      formData.append('educationForm', data.educationForm)
      formData.append('commonReasons', data.commonReasons)
      data.studentList.forEach((id, index) => {
        formData.append(`studentList[${index}]`, id)
      })
      data.statements.forEach((file, index) => {
        if (file.img) file = file.img
        formData.append(`statements[${index}]`, file)
      })

      data.points.
        forEach((point, index) => {
          if (point.id)
            formData.append(
              `points[${index}]id`,
              point.id
            )
          formData.append(
            `points[${index}]title`,
            point.title
          )
          formData.append(
            `points[${index}]description`,
            point.description
          )
          formData.append(
            `points[${index}]gender`,
            point.gender
          )
          point.uploadDocumentsFormat
            .forEach((format, fileIndex) => {
              formData.append(`points[${index}]uploadDocumentsFormat[${fileIndex}]title`,
               format.title)
            })
          point.commonReasons
            .forEach((reason, fileIndex) => {
              formData.append(`points[${index}]commonReasons[${fileIndex}]`,
               reason)
            })
          point.requiredDocuments
            .forEach((file, fileIndex) => {
              if (file.img) file = file.img
              formData.append(
                `points[${index}]requiredDocuments[${fileIndex}]`,
                 file)
            })
        })

      return await BypassSheetsSchemasService.patch(data.id, formData)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [DELETE_BYPASS_SHEETS_SCHEMA](context, id) {
    try {
      await context.dispatch(CHECK_AUTH)
      return await BypassSheetsSchemasService.delete(id)
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  }
}

const mutations = {
  [SET_BYPASS_SHEETS_SCHEMAS](state, bypassSheetsSchemas) {
    state.bypassSheetsSchemas = bypassSheetsSchemas
  },
  [SET_BYPASS_SHEETS_SCHEMA](state, bypassSheetsSchema) {
    state.bypassSheetsSchema = bypassSheetsSchema
  },
  [SET_BYPASS_SHEETS_SCHEMAS_TITLES](state, bypassSheetsSchemasTitles) {
    state.bypassSheetsSchemasTitles = bypassSheetsSchemasTitles
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
