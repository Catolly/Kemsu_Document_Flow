<template>
  <roleStaff class="container">
    <div class="sign-main">
      <div class="head">
        <h1 v-if="bypassSheetsSchema" class="header">{{bypassSheetsSchema.title}}</h1>
        <span
          v-if="
            fetchGroupsError
            || fetchUsersError
            || fetchSchemaError
            || updateBypassSheetsError"
          class="error-message"
        >
          {{ fetchGroupsError ? 'Не удалось загрузить список групп'  : '' }}
          {{ fetchUsersError ? 'Не удалось загрузить список студентов'  : '' }}
          {{ fetchSchemaError ? 'Не удалось загрузить обходной лист'  : '' }}
          {{ updateBypassSheetsError ? 'Не удалось сохранить обходной лист'  : '' }}
        </span>
        <app-filter-nav
          v-if="filterPath"
          :filterPath="filterPath"
          @setFilterDepth="setFilterDepth"
        />
      </div>

      <h2 v-if="!studentList.length">Обходных листов на подпись ещё нет</h2>

      <template v-if="studentList.length && !fetchUsersError && !fetchSchemaError">
        <app-sign-topbar
          :checkedPointsCount="checkedStudents.length"
          @signChecked="signChecked"
          @checkAll="checkAll"
          @uncheckAll="uncheckAll"

          :searchText="searchText"
          @search="search"

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
          :studentList="studentList"
          @check="check"
          @uncheck="uncheck"
          @sign="sign"
          @reject="openRejectForm"
        />

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
      v-if="studentList.length && !fetchGroupsError && FilterService"
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

    FilterService: null,
  }),

  async fetch() {
    try {
      await this.fetchSchema()
      await Promise.all([
        this.findUsers(),
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

    bypassSheetStatus() {
      return bypassSheetStatus
    },

    checkedStudentsId() {
      return this.checkedStudents
        .map(checkedStudent => checkedStudent.id)
    },
  },

  watch: {
    filterPath() {
      this.page = 0
      this.findUsers()
    },
    searchText() {
      this.page = 0
      this.findUsers()
    },
    page() {
      this.findUsers()
    },
    itemsPerPage() {
      if (this.itemsPerPage) {
        this.findUsers()
      }
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

    async findUsers() {
      this.fetchUsersError = ''
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
        return await this.$store
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
}

@media all and (max-width: 1800px) {
  .container {
    grid-column-gap: 32px;
  }
}
</style>
