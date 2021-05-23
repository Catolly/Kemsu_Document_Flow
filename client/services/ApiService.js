import axios from 'axios'
import JwtService from "~/services/JWTService"
import { API_URL } from "~/services/config"

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
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
    return ApiService.post('bypass_sheets/', bypassSheet)
  },
  get(department='') {
    ApiService.setHeader()
    return ApiService.get('bypass_sheets' + (department ? `/?department=${department}` : ''))
  },
  patch(id, data) {
    ApiService.setHeader()
    return ApiService.patch(`bypass_sheets/${id}/`, data)
  },
  patchMany({
    department,
    data
  }) {
    ApiService.setHeader()
    return ApiService.patch(`bypass_sheets/?department=${department}`, data)
  },
}

export const BypassSheetsSchemasService = {
  get(id='') { //department=''
    ApiService.setHeader()
    return ApiService.get('bypass_sheets_schema', id)
  },
  getMany(department='') {
    ApiService.setHeader()
    return ApiService.get(
      'bypass_sheets_schema' + (department ? `?department=${department}` : '')
    )
  },
  getTitles(educationForm) { //department=''
    ApiService.setHeader()
    return ApiService.get(`bypass_sheets_schema`, `titles?educationForm=${educationForm}`)
  },
  post(params) {
    ApiService.setHeader()
    return ApiService.post('bypass_sheets_schema/', params)
  },
  patch(id, params) {
    ApiService.setHeader()
    return ApiService.patch(`bypass_sheets_schema/${id}/`, params)
  },
  delete(id) {
    ApiService.setHeader()
    return ApiService.delete(`bypass_sheets_schema/${id}/`)
  },
}

export const DepartmentsService = {
  get(data={}) {
    const {
      institute='',
      department='',
    } = data
    const params = Object.entries(data)
      .map(([key, value]) =>
        value ? `&${key}=${value}` : ''
      )
      .join('')
      .slice(1)
    return ApiService.get(
      `departments`
      + (params ? '/?' : '')
      + params)
  },
}

export const GroupsService = {
  get() {
    return ApiService.get('groups')
  },
}

export const UsersService = {
  get(params) {
    ApiService.setHeader()
    const paramsURL = URLfromParams(params)
    return ApiService.query(
      'users'
      + (paramsURL ? `/?${paramsURL}` : '')
    )
  },

  getUnregistered(params) {
    const paramsURL = URLfromParams(params)
    return ApiService.query(
      'unregistered_students'
      + (paramsURL ? `/?${paramsURL}` : '')
    )
  }
}

export const errorCode = error => error.toString().split(' ').reverse()[0]

const URLfromParams = params => Object.entries(params)
  .map(([key, value]) => value ? `&${key}=${value}` : '')
  .join('')
  .slice(1)
