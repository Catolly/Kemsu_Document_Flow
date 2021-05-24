import { UsersService, DepartmentsService, GroupsService } from "~/services/ApiService"
import {
  FETCH_ALL_DEPARTMENTS,
  FETCH_DEPARTMENTS,
  FETCH_DEPARTMENT,
  FETCH_GROUPS,
  FETCH_UNREGISTERED_STUDENTS,
  WAIT_FOR,
} from "./actions.type"
import {
  SET_ALL_DEPARTMENTS,
  SET_DEPARTMENTS,
  SET_DEPARTMENT,
  SET_GROUPS,
  SET_UNREGISTERED_STUDENTS,
  SET_ERROR,
} from "./mutations.type"

const state = () => ({
  allDepartments: [],
  departments: [],
  currentDepartment: {},
  groups: [],
  unregisteredStudents: [],
})

const getters = {
  allDepartments(state) {
    return state.allDepartments
  },
  departments(state) {
    return state.departments
  },
  currentDepartment(state) {
    return state.currentDepartment
  },
  groups(state) {
    return state.groups
  },
  unregisteredStudents(state) {
    return state.unregisteredStudents
  },
}

const actions = {
  async [FETCH_ALL_DEPARTMENTS](context) {
    const departments = context.getters.allDepartments
    if (departments.length !== 0) {
      return context.commit(SET_ALL_DEPARTMENTS, departments)
    }
    return new Promise((resolve, reject) => {
      DepartmentsService.get()
        .then(departments => {
          context.commit(SET_ALL_DEPARTMENTS, departments.data.slice())
          resolve(departments.data)
        })
        .catch(error => {
          context.commit(SET_ERROR, error)
          reject(error)
        })
    })
  },
  async [FETCH_DEPARTMENTS](context, params={}) {
    const {
      departments=[],
      institute='',
    } = params
    if (departments.length !== 0) {
      return context.commit(SET_DEPARTMENTS, departments)
    }
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          DepartmentsService.get({institute})
            .then(({ data }) => {
              context.commit(SET_DEPARTMENTS, data.slice())
              resolve(data)
            })
            .catch(error => {
              context.commit(SET_ERROR, error)
              reject(error)
            })
      })
    })
  },
  async [FETCH_DEPARTMENT](context, params={}) {
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          DepartmentsService.get(params)
            .then(({ data }) => {
              context.commit(SET_DEPARTMENT, data.slice())
              resolve(data)
            })
            .catch(error => {
              context.commit(SET_ERROR, error)
              reject(error)
            })
        })
    })
  },
  async [FETCH_GROUPS](context, prevGroups) {
    if (prevGroups.length !== 0) {
      return context.commit(SET_GROUPS, prevGroups)
    }
    return new Promise((resolve, reject) => {
      context.dispatch(WAIT_FOR, 'checkingAuth')
        .then(() => {
          GroupsService.get()
            .then(({ data }) => {
              context.commit(SET_GROUPS, data)
              resolve(data)
            })
            .catch(error => {
              context.commit(SET_ERROR, error)
              reject(error)
            })
        })
    })
  },
  async [FETCH_UNREGISTERED_STUDENTS](context, {
    search = '',
    limit = 0,
  }) {
    try {
      const { data } = await UsersService.getUnregistered({
        search,
        limit,
      })
      context.commit(SET_UNREGISTERED_STUDENTS, data.students)
    } catch(error) {
      context.commit(SET_ERROR, error)
      console.error(error)
      throw error
    }
  },
}

const mutations = {
  [SET_ALL_DEPARTMENTS](state, departments) {
    state.allDepartments = departments
  },
  [SET_DEPARTMENTS](state, departments) {
    state.departments = departments
  },
  [SET_DEPARTMENT](state, currentDepartment) {
    state.currentDepartment = currentDepartment
  },
  [SET_GROUPS](state, groups) {
    state.groups = groups
  },
  [SET_UNREGISTERED_STUDENTS](state, unregisteredStudents) {
    state.unregisteredStudents = unregisteredStudents
  },
}

export default {
  state,
  actions,
  mutations,
  getters
}
