<template>
  <div class="container">
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
  </div>
</template>

<script>
import _ from "lodash"
import { debounceDelay } from "~/services/config"

import { mapGetters } from "vuex"
import { FETCH_USERS, UPDATE_BYPASS_SHEETS } from "~/store/actions.type"

import bypassSheetStatus from '~/services/bypassSheetStatus'
import FilterService from '~/services/FilterService'

import AppFilter from '~/components/common/AppFilter'
import AppFilterNav from '~/components/common/AppFilterNav'
import AppSignTopbar from '~/components/bypass-sheets/signature/AppSignTopbar'
import AppPagination from '~/components/common/AppPagination'
import AppStudentList from '~/components/bypass-sheets/signature/AppStudentList'
import AppModal from '~/components/common/AppModal'
import AppRejectForm from '~/components/bypass-sheets/signature/AppRejectForm'

export default {

  components: {
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

    title: 'Скидка на столовую',

    fetchUsersError: '',
    updateBypassSheetsError: '',

    studentList: [
      {
        id: 1,
        fullname: "Козырева Татьяна Андреевна",
        email: "example1@gmail.com",
        recruitmentForm: "Бюджет",
        educationForm: "Заочная",
        status: "Учится",
        checked: false,
        courseNumber: '4',
        group: "М-174",
        institute: "ИФН",
        point: {
          bypassSheetId: 1,
          name: "Библиотека",
          status: "reviewing", // или "rejected" или "signed"
          documentList: [
            {
              name: "Фото/скан паспорта",
              // file: type File",
            },
            {
              name: "Заполненный документ",
              // file: type File",
            },
          ],
          staff: "Иванов И.И.",
          rejectReason: "Сообщение 1", // если status="rejected"
          requiredDocuments: [],
        },
      },
      {
        id: 2,
        fullname: "Сергиенко Анатолий Николаевич",
        email: "exmaple2@gmail.com",
        recruitmentForm: "Бюджет",
        educationForm: "Очная",
        status: "Учится",
        checked: false,
        courseNumber: '4',
        group: "М-174",
        institute: "ИФН",
        point: {
          bypassSheetId: 2,
          name: "Библиотека",
          status: "reviewing", // или "rejected" или "signed"
          documentList: [
            {
              name: "Фото/скан паспорта",
              // file: type File",
            },
            {
              name: "Заполненный документ",
              // file: type File",
            },
          ],
          staff: "Иванов И.И.",
          rejectReason: "Сообщение 2", // если status="rejected"
          requiredDocuments: [],
        },
      },
      {
        id: 3,
        fullname: "Люкшин Михаил Сергеевич",
        email: "example3@gmail.com",
        recruitmentForm: "Бюджет",
        educationForm: "Очная",
        status: "В академ. отпуске",
        checked: false,
        courseNumber: '3',
        group: "Ц-184",
        institute: "ИЦ",
        point: {
          bypassSheetId: 3,
          name: "Библиотека",
          status: "rejected", // или "rejected" или "signed"
          documentList: [
            {
              name: "Фото/скан паспорта",
              // file: type File",
            },
            {
              name: "Заполненный документ",
              // file: type File",
            },
          ],
          staff: "Иванов И.И.",
          rejectReason: "Сообщение 3", // если status="rejected"
          requiredDocuments: [],
        },
      },
    ],

    groups: [
      {
        name: "М-174",
        institute: "ИФН",
        courseNumber: '4',
      },
      {
        name: "М-184",
        institute: "ИФН",
        courseNumber: '3',
      },
      {
        name: "Ц-184",
        institute: "ИЦ",
        courseNumber: '3',
      },
    ],

    FilterService: null,
  }),

  computed: {
    ...mapGetters(['users']),


    staff() {
      // const [firstname, lastname, middlename] = currentUser.fullname.split(' ')
      // return firstname + lastname[0] + '.' + (middlename ? middlename + '.' : '')
      return 'Неиванов И.И.'
    },

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
      if (this.FilterService.filterList.every(filter => filter.value === ''))
        return this.studentList

      return this.studentList
      .filter(student => this.FilterService.filterList
        .filter(filter => filter.value != '')
        .every(filter => {
          return student[filter.filteringPropName] === filter.value
        }))
    },

    filterList() {
      return this.FilterService.filterList.map(filter => ({
        selected: filter.value,
        placeholder: filter.name,
        postfix: filter.postfix,
        options: Array.from(new Set(filter.options.map(option => option.value))),
      }))
    },

    filterPath() {
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
      this.$store
        .dispatch(FETCH_USERS, {
          users: this.users,
        })
        .then(() => this.studentList = this.users)
        .catch(error => this.fetchUsersError = error)
    },

    async fetchGroups() {

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
        }
      })

      this.$store
        .dispatch(UPDATE_BYPASS_SHEETS, {
            department: 'Библиотека', // currentUser.department
            bypassSheets: updatingBypassSheets,
          })
        .catch(error => this.updateBypassSheetsError = error)
    }, debounceDelay)
  },

  created() {
    this.fetchStudentList()
    this.fetchGroups()
    // .then(() => this.initFilterService())
    this.FilterService = initFilterService(this.groups)
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
    gap: 16px;
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
