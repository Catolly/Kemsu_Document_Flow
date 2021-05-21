<template>
  <roleStaff class="container">
    <div class="sign-main">
      <div class="head">
        <h1 class="header">{{title}}</h1>
        <app-filter-nav
          :filterPath="filterPath"
          @setFilterDepth="setFilterDepth"
        />
      </div>

      <app-sign-topbar
        :checkedPointsCount="checkedStudentList.length"
        @signChecked="signChecked"
        @checkAll="checkAll"
        @uncheckAll="uncheckAll"

        :searchText="searchText"
        @search="search"

        class="topbar"
      />

      <app-pagination
        v-if="searchingStudentList.length > 0"
        :itemsAmount="searchingStudentList.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"

        class="pagination"
      />

      <app-student-list
        :studentList="studentListInPage"
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
    </div>

    <app-filter
      class="filter"
      :filterList="filterList"
      @select="select"
      @clear="clear"
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
        this.fetchStudentList(),
        this.fetchGroups(),
      ])
      this.FilterService = initFilterService(this.groups)
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters(['currentUser', 'users', 'groups', 'bypassSheetsSchema']),

    studentListInPage() {
      return this.searchingStudentList.slice(this.page * this.itemsPerPage,
                                            (this.page + 1) * this.itemsPerPage)
    },
    checkedStudentList() {
      return this.searchingStudentList.filter(student => student.checked)
    },
    searchingStudentList() {
      if (this.searchText === '') return this.filteredStudentList

      return this.filteredStudentList.filter(student =>
        student.fullname.toLowerCase().includes(this.searchText.toLowerCase())
      )
    },
    filteredStudentList() {
      if (
        !this.FilterService ||
        this.FilterService.filterList.every(filter => filter.value === '')
      ) return this.studentList

      return this.studentList
      .filter(student => this.FilterService.filterList
        .filter(filter => filter.value != '')
        .every(filter => {
          return student[filter.filteringPropName] === filter.value
        }))
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
  },

  methods: {
    // Методы app-sign-student-list
    check(student) {
      student.checked = true
    },
    uncheck(student) {
      student.checked = false
    },
    sign(student) {
      const point = student.point
      point.status = bypassSheetStatus.Signed
      point.rejectReason = ''
      point.requiredDocuments = []
      point.staff = this.staff
      this.uncheck(student)

      this.updateBypassSheets()
    },
    reject(student) {
      const point = student.point
      point.status = bypassSheetStatus.Rejected
      point.staff = this.staff
      this.uncheck(student)
      this.closeRejectForm()

      this.updateBypassSheets()
    },

    // Методы app-sign-topbar
    signChecked() {
      this.checkedStudentList.forEach(this.sign)
    },
    checkAll() {
      this.searchingStudentList.forEach(this.check)
    },
    uncheckAll() {
      this.checkedStudentList.forEach(this.uncheck)
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

    async fetchStudentList() {
      try {
        this.fetchUsersError = ''
        await this.$store
          .dispatch(FETCH_USERS, {
            users: this.users,
            bypassSheet: this.bypassSheetsSchema.title,
            point: this.currentUser.department,
          })
          this.studentList = copy(this.users)
            .filter(student => Object.values(student.point)
              .some(value => value))
            .filter(student =>
              student.point.status
              && (student.point.status != bypassSheetStatus.NotSent))
          this.studentList
            .forEach(student => {
              this.$set(student, 'checked', false)
            })
      } catch (error) {
        console.error(error)
        this.fetchUsersError = error
        throw error
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

    updateBypassSheets: _.debounce(function () {
      const updatingBypassSheets = this.studentList
      .filter(student =>
        [
          bypassSheetStatus.Rejected,
          bypassSheetStatus.Signed
        ]
        .includes(student.point.status)
      )
      .map(student => {
        const requiredDocuments = new FormData()

        student.point.requiredDocuments
        .forEach(doc =>
          requiredDocuments.append('requiredDocuments', doc)
        )

        return {
          id: student.point.bypassSheetId, //id листа
          title: student.point.name,
          status: student.point.status, // 'rejected' или "signed"
          rejectReason: student.point.rejectReason, // сообщение отказа (опционально)
          staff: student.point.staff, // Инициалы сотрудника
          requiredDocuments: Array.from(requiredDocuments), // Загруженные сотрудником документы
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

      this.$store
        .dispatch(UPDATE_BYPASS_SHEETS, {
            department: 'Библиотека', // currentUser.department
            bypassSheets: updatingBypassSheets,
          })
        .catch(error => this.updateBypassSheetsError = error)
    }, debounceDelay)
  },

  beforeDestroy() {
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
