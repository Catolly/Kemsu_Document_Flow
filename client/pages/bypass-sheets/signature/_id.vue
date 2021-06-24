<template>
  <roleStaff class="container">
    <div class="sign-main">
      <div class="head">
        <h1 v-if="bypassSheetsSchema" class="header">
          {{bypassSheetsSchema.title}}
        </h1>
        <span
          v-if="fetchGroupsError"
          class="error-message"
        >
          {{fetchGroupsError ? 'Не удалось загрузить список групп'  : ''}}
        </span>
        <span
          v-if="fetchUsersError"
          class="error-message"
        >
          {{fetchUsersError ? 'Не удалось загрузить список студентов'  : ''}}
        </span>
        <span
          v-if="fetchSchemaError"
          class="error-message"
        >
          {{fetchSchemaError ? 'Не удалось загрузить обходной лист'  : ''}}
        </span>
        <span
          v-if="updateBypassSheetsError"
          class="error-message"
        >
          {{updateBypassSheetsError ? 'Не удалось сохранить обходной лист'  : ''}}
        </span>

        <span v-else-if="currentPoint">
          {{currentPoint.description}}
        </span>

        <app-filter-nav
          v-if="filterPath"
          :filterPath="filterPath"
          @setFilterDepth="setFilterDepth"
        />
      </div>

      <template v-if="!fetchUsersError && !fetchSchemaError">
        <app-sign-topbar
          :checkedPointsCount="checkedStudents.length"
          @signChecked="signChecked"
          @checkAll="checkAll"
          @uncheckAll="uncheckAll"

          :searchText="searchText"
          @search="search"

          :isLoading="fetchingUsers"

          class="topbar"
        />

        <app-pagination
          v-show="studentList.length > 0"
          :itemsAmount="usersAmount"
          :page="page"
          @updateItemsPerPage="itemsPerPage = $event"
          @updatePage="page = $event"

          class="pagination"
        />

        <app-student-list
          v-if="studentList.length"
          v-show="!fetchingUsers"
          :studentList="studentList"
          @check="check"
          @uncheck="uncheck"
          @sign="sign"
          @reject="openRejectForm"
        />

        <h2
          v-else
          v-show="!fetchingUsers"
          class="empty-message"
        >
          Обходных листов не было найдено
        </h2>

        <div class="loading-spinner-inner">
          <div v-show="fetchingUsers" class="loading-spinner" />
        </div>

        <app-modal
          v-show="rejectForm.isOpen"
        >
          <app-reject-form
            v-if="rejectForm.student"
            :student="rejectForm.student"
            @close="closeRejectForm"
            @reject="reject"
          />
        </app-modal>
      </template>
    </div>

    <app-filter
      v-if="!fetchGroupsError && FilterService"
      :filterList="filterList"
      @select="select"
      @clear="clear"
      class="filter"
    />
  </roleStaff>
</template>

<script>
import _ from "lodash"
import { debounceDelay } from "~/services/config"

import { mapGetters } from "vuex"
import {
  FETCH_USERS,
  FETCH_GROUPS,
  FETCH_BYPASS_SHEETS_SCHEMA,
  UPDATE_BYPASS_SHEETS
} from "~/store/actions.type"
import { copy } from "~/store/methods"

import bypassSheetStatus from '~/services/bypassSheetStatus'
import { initFilterService } from '~/services/FilterService'

import roleStaff from '~/components/roles/roleStaff'

import AppFilter from '~/components/common/AppFilter'
import AppFilterNav from '~/components/common/AppFilterNav'
import AppSignTopbar from '~/components/bypass-sheets/signature/AppSignTopbar'
import AppPagination from '~/components/common/AppPagination'
import AppStudentList from '~/components/bypass-sheets/signature/AppStudentList'
import AppModal from '~/components/common/AppModal'
import AppRejectForm from '~/components/bypass-sheets/signature/AppRejectForm'

export default {
  middleware: 'authenticated',

  components: {
    roleStaff,
    AppFilter,
    AppFilterNav,
    AppSignTopbar,
    AppPagination,
    AppStudentList,
    AppModal,
    AppRejectForm,
  },

  data:() => ({
    searchText: '',
    page: 0,
    itemsPerPage: 0,

    rejectForm: {
      isOpen: false,
      student: null,
    },

    studentList: [],
    checkedStudents: [],
    updatingBypassSheets: new Set(),

    fetchGroupsError: '',
    fetchUsersError: '',
    fetchSchemaError: '',
    updateBypassSheetsError: '',

    fetchingUsers: false,

    FilterService: null,
  }),

  async fetch() {
    try {
      await Promise.all([
        this.fetchSchema(),
        this.fetchGroups(),
      ])
      this.FilterService = initFilterService(this.groups)
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters([
      'currentUser',
      'users',
      'usersAmount',
      'groups',
      'bypassSheetsSchema'
    ]),

    filters() {
      if (!this.FilterService) return []

      return this.FilterService.filterList
        .map(filter => filter.value)
    },

    filterList() {
      if (!this.FilterService) return []

      return this.FilterService.filterList.map(filter => ({
        selected: filter.value,
        placeholder: filter.name,
        postfix: filter.postfix,
        options: Array.from(new Set(filter.options.map(option => option.value))),
      }))
    },

    filterPath() {
      if (!this.FilterService) return []

      return this.FilterService.filterList.map(filter =>
        filter.value + (filter.value ? filter.postfix : '')
      )
    },

    checkedStudentsId() {
      return this.checkedStudents
        .map(checkedStudent => checkedStudent.id)
    },

    currentPoint() {
      if (!this.bypassSheetsSchema) return null

      return this.bypassSheetsSchema
        .points
          .find(point => point.title === this.currentUser.department)
    },

    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },

  watch: {
    filterPath() {
      this.page = 0
      this.fetchUsers()
    },
    searchText() {
      this.page = 0
      this.fetchUsersDebounced()
    },
    page() {
      this.fetchUsers()
    },
    itemsPerPage() {
      this.fetchUsers()
    },
    studentList() {
      this.checkAttachedStudents()
    },
  },

  methods: {
    // Методы app-sign-student-list
    check(student) {
      if (this.checkedStudentsId.includes(student.id)) return
      this.$set(student, 'checked', true)
      this.checkedStudents.push(student)
    },
    uncheck(student) {
      if (!this.checkedStudentsId.includes(student.id)) return
      this.$set(student, 'checked', false)
      this.checkedStudents = this.checkedStudents
        .filter(checkedStudent => checkedStudent.id !== student.id)
    },
    checkAttachedStudents() {
      this.studentList.forEach(student => {
        this.$set(student, 'checked', this.checkedStudentsId
          .includes(student.id)
        )
      })
    },
    sign(student) {
      this.uncheck(student)
      const point = student.point

      if (point.status === bypassSheetStatus.Signed) return

      point.status = bypassSheetStatus.Signed
      point.rejectReason = ''
      point.requiredDocuments = []
      point.staff = this.currentUser.fullname
      this.updatingBypassSheets.add(student.point)

      this.updateBypassSheets()
    },
    reject(student) {
      this.uncheck(student)
      const point = student.point

      if (point.status === bypassSheetStatus.Rejected) return

      point.status = bypassSheetStatus.Rejected
      point.staff = this.currentUser.fullname
      this.updatingBypassSheets.add(student.point)
      this.closeRejectForm()

      this.updateBypassSheets()
    },

    // Методы app-sign-topbar
    signChecked() {
      this.studentList.forEach(student => {
        if (this.checkedStudentsId.includes(student.id))
          this.sign(student)
        this.uncheck(student)
      })
      this.checkedStudents.forEach(this.sign)
    },
    checkAll() {
      this.studentList.forEach(this.check)
    },
    uncheckAll() {
      this.studentList.forEach(student => {
        this.$set(student, 'checked', false)
      })
      this.checkedStudents = []
    },
    search(searchText) {
      this.searchText = searchText
    },
    //

    // Методы app-filter
    select(params) {
      const [value, filter] = params
      this.FilterService.set(filter.placeholder, value)
    },
    clear() {
      this.FilterService.clear()
    },
    //

    // Методы app-reject-form
    openRejectForm(student) {
      this.rejectForm.student = student
      this.rejectForm.isOpen = true
    },
    closeRejectForm() {
      this.rejectForm.isOpen = false
    },
    //

    // Методы app-filter-nav
    setFilterDepth(depth) {
      if (depth < 0) {
        this.clear()
        return
      }

      this.FilterService.filterList.forEach((filter, index) => {
        if (index > depth) filter.value = ''
      })
    },
    //


    async fetchUsers() {
      if (!this.bypassSheetsSchema) return
      if (this.itemsPerPage === 0) return
      if (this.fetchingUsers) return

      this.fetchUsersError = ''
      this.fetchingUsers = true

      try {
        const [
          institute,
          course,
          group
        ] = this.filters.map(filter => filter)

        await this.$store
          .dispatch(FETCH_USERS, {
            bypassSheet: this.bypassSheetsSchema.title,
            point: this.currentUser.department,
            search: this.searchText,
            institute,
            course,
            group,
            offset: this.page * this.itemsPerPage,
            limit: this.itemsPerPage
          })

        this.studentList = copy(this.$store.getters.users)
      } catch (error) {
        console.error(error)
        this.fetchUsersError = error
      } finally {
        this.fetchingUsers = false
      }
    },

    async fetchGroups() {
      try {
        this.fetchGroupsError = ''
        await this.$store
          .dispatch(FETCH_GROUPS, this.groups)
      } catch (error) {
        console.error(error)
        this.fetchGroupsError = error
        throw error
      }
    },

    async fetchSchema() {
      try {
        this.fetchSchemaError = ''
        await this.$store
          .dispatch(FETCH_BYPASS_SHEETS_SCHEMA, {id: this.$route.params.id})
      } catch (error) {
        console.error(error)
        this.fetchSchemaError = error
        throw error
      }
    },

    updateBypassSheets: _.debounce(function () {
      try {
        this.updateBypassSheetsError = ''
        this.$store.dispatch(UPDATE_BYPASS_SHEETS, {
          department: this.currentUser.department,
          bypassSheets: Array.from(this.updatingBypassSheets),
        })
        this.updatingBypassSheets = new Set()
      } catch (error) {
        console.error(error)
        this.updateBypassSheetsError = error
      }
    }, debounceDelay)
  },

  beforeDestroy() {
    if (this.updatingBypassSheets.length)
      this.updateBypassSheets()
  },
}
</script>

<style lang="less" scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 30%;
  grid-column-gap: 64px;

  .sign-main {
    padding-top: 48px;

    display: flex;
    flex-direction: column;
    gap: 24px;

    position: relative;
  }

  .head {
    margin-bottom: 24px;

    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .pagination {
    justify-content: flex-end;
  }

  .empty-message {
    margin-top: 1em;
  }

  .loading-spinner-inner {
    height: 100%;

    position: relative;
    margin-bottom: 20%;
  }

  .loading-spinner {
    .spinner();
  }
}

@media all and (max-width: 1800px) {
  .container {
    grid-column-gap: 32px;
  }
}
</style>
