import ApiService from '~/services/ApiService'
import JwtService from '~/services/JWTService'
import {
  WAIT_FOR,
  CHECK_ROLE,
  ROLE_IS,
} from './actions.type'
import {
  SET_IS_STUDENT,
  SET_IS_STAFF,
  SET_IS_ADMIN,
  PURGE_ROLES,
  SET_ERROR,
} from './mutations.type'

const state = () => ({
  Role: {
    isStudent: false,
    isStaff: false,
    isAdmin: false,

    Student: 'Студент',
    Staff: 'Работник',
    Admin: 'Администратор',
  },
})

const getters = {
  Role(state) {
    return state.Role
  },
}

const actions = {
  async [ROLE_IS](context, roles) {
    if (typeof roles === 'string') roles = [roles]
    try {
      await context.dispatch(WAIT_FOR, 'checkingAuth')
      const hasAccess = await context.dispatch(CHECK_ROLE, roles)
      if (hasAccess && (roles.length === 1))
        switch(roles[0]) {
          case context.getters.Role.Student:
            context.commit(SET_IS_STUDENT, true)
            break
          case context.getters.Role.Staff:
            context.commit(SET_IS_STAFF, true)
            break
          case context.getters.Role.Admin:
            context.commit(SET_IS_ADMIN, true)
            break
        }
      return hasAccess
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
  async [CHECK_ROLE](context, roles) {
    if (!roles) throw `Error roles: roles missing`
    if (!roles.length) throw `Error roles format: roles inputed - ${roles}`

    if (!JwtService.getToken()) return false
    ApiService.setHeader()
    try {
      const res = await ApiService.post('checkAccess', {
        role: roles,
        accessToken: JwtService.getToken().access,
      })
      return res.data.hasAccess
    } catch (error) {
      context.commit(SET_ERROR, error)
      throw error
    }
  },
}

const mutations = {
  [SET_IS_STUDENT](state, isStudent) {
    state.Role.isStudent = isStudent
  },
  [SET_IS_STAFF](state, isStaff) {
    state.Role.isStaff = isStaff
  },
  [SET_IS_ADMIN](state, isAdmin) {
    state.Role.isAdmin = isAdmin
  },
  [PURGE_ROLES](state) {
    state.Role.isStudent = false
    state.Role.isStaff = false
    state.Role.isAdmin = false
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
