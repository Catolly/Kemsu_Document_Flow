import axios from 'axios'
import JwtService from "~/services/JWTService"
import { API_URL } from "~/services/config"

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
})

const ApiService = {
  setHeader() {
    api.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${JwtService.getToken().access}`
  },

  query(resource, params) {
    return api.get(resource, params).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  get(resource, slug = "") {
    return api.get(`${resource}/${slug}`).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  post(resource, params) {
    return api.post(`${resource}`, params).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  update(resource, slug, params) {
    return api.put(`${resource}/${slug}`, params).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  put(resource, params) {
    return api.put(`${resource}`, params).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  patch(resource, params) {
    return api.patch(`${resource}`, params).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },

  delete(resource) {
    return api.delete(resource).catch(error => {
      throw new Error(`ApiService ${error}`)
    })
  },
}

export default ApiService

export const BypassSheetsService = {
  post(bypassSheet) {
    ApiService.setHeader()
    return ApiService.post('bypass-sheets/', bypassSheet)
  },

  get() { //department=''
    ApiService.setHeader()
    return ApiService.get('bypass-sheets')
  },

  patchMany(params) {
    const {
      department,
      bypassSheets
    } = params
    console.log(department, bypassSheets)
    ApiService.setHeader()
    return ApiService.patch(`bypass-sheets/${department}`, bypassSheets)
  },
}

export const BypassSheetsSchemasService = {
  get(id='') { //department=''
    ApiService.setHeader()
    return ApiService.get('bypass_sheets_schema', id)
  },
  post(params) {
    ApiService.setHeader()
    return ApiService.post('bypass_sheets_schema/', params)
  },
  patch(params) {
    ApiService.setHeader()
    return ApiService.patch(`bypass_sheets_schema/${params.id}/`, params)
  },
}

export const DepartmentsService = {
  get(institute='', department='') {
    ApiService.setHeader()
    return ApiService.get(
      `departments`
      + (institute ? `/${institute}` : '')
      + (department ? `/?department="${department}"`: ''))
  },
}

export const GroupsService = {
  get() {
    return ApiService.get('groups')
  },
}

export const UsersService = {
  get(params) {
    const resourseParams = params
    ? Object.entries(params).map(([name, value]) =>
      value ? `${name}=${value}&` : ''
      ).join('')
    : ''
    // console.log(resourseParams)
    return ApiService.get('users' + (resourseParams ? `/?${resourseParams.slice(0, -1)}` : ''))
  },
}
