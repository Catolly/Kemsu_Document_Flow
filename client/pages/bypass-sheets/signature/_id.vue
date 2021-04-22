<template>
  <div class="container">

    <!-- Завернуть все в компонент app-sign-main-->
    <div class="sign-main">

      <h1 class="header">{{title}}</h1>

      <app-filter-nav
        :filterNames="selectedFilterNames"
      />

      <app-sign-topbar
        :checkedPointsCount="checkedStudentList.length"
        @signChecked="signChecked"
        @checkAll="checkAll"
        @uncheckAll="uncheckAll"

        :searchText="searchText"
        @search="search"
      />

      <app-student-list
        :studentList="searchingStudentList"
        @check="check"
        @uncheck="uncheck"
        @sign="sign"
        @reject="openRejectForm"
      />

      <app-modal
        v-if="rejectForm.isOpen"
      >
        <app-reject-form
          @close="closeRejectForm"
          @reject="reject"
        />
      </app-modal>

    </div>
    <!--  -->

    <app-filter
      class="filter"
      :filterList="filterList"
      @select="select"
      @clear="clear"
    />

  </div>
</template>

<script>
import AppFilter from '~/components/common/AppFilter'
import AppFilterNav from '~/components/common/AppFilterNav'
import AppSignTopbar from '~/components/bypass-sheets/signature/AppSignTopbar'
import AppStudentList from '~/components/bypass-sheets/signature/AppStudentList'
import AppModal from '~/components/common/AppModal'
import AppRejectForm from '~/components/bypass-sheets/signature/AppRejectForm'

export default {

  components: {
    AppFilter,
    AppFilterNav,
    AppSignTopbar,
    AppStudentList,
    AppModal,
    AppRejectForm,
  },

  data:() => ({
    title: 'Скидка на столовую',

    searchText: '',

    rejectForm: {
      // добавить текст отказа
      isOpen: false,
      student: null,
    },

    // Изменить структуру - студент наверху, в себе содержит обходные листы, инфу о группах/институтах
    studentList: [
    {
      "id": 1,
      "fullName": "Козырева Татьяна Андреевна",
      "email": "example1@gmail.com",
      "educationForm": "Бюджет",
      "status": "Учится",
      "checked": false,
      "courseNumber": 3,
      "group": {
         "name": "M-174",
         "institute": "Институт Фундаментальных Наук",
      },
      "point": {
        "name": "Библиотека",
        "status": "reviewing", // или "rejected" или "signed"
        "rejectReason": "Необходимо сдать ключ от комнаты", // если status="rejected"
        "staffName": "Иванов И.И.",
        "documentList": [
          {
            name: "Фото/скан паспорта",
            url: "http://mydoc.kemsu/...",
          },
          {
            name: "Заполненный документ",
            url: "http://mydoc.kemsu/...",
          },
        ],
      },
    },
    {
      "id": 2,
      "fullName": "Сергиенко Анатолий Николаевич",
      "email": "exmaple2@gmail.com",
      "educationForm": "Бюджет",
      "status": "Учится",
      "checked": false,
      "courseNumber": 3,
      "group": {
        "name": "M-174",
        "institute": "Институт Фундаментальных Наук",
      },
     "point": {
        "name": "Библиотека",
        "status": "reviewing", // или "rejected" или "signed"
        "rejectReason": "Необходимо сдать ключ от комнаты", // если status="rejected"
        "staffName": "Иванов И.И.",
        "documentList": [
          {
            name: "Фото/скан паспорта",
            url: "http://mydoc.kemsu/...",
          },
          {
            name: "Заполненный документ",
            url: "http://mydoc.kemsu/...",
          },
        ],
      },
    },
    {
      "id": 3,
      "fullName": "Люкшин Михаил Сергеевич",
      "email": "example3@gmail.com",
      "educationForm": "Бюджет",
      "status": "В академ. отпуске",
      "checked": false,
      "courseNumber": 2,
      "group": {
        "name": "Ц-184",
        "institute": "Институт Цифры",
      },
      "point": {
        "name": "Библиотека",
        "status": "rejected", // или "rejected" или "signed"
        "rejectReason": "Необходимо сдать ключ от комнаты", // если status="rejected"
        "staffName": "Иванов И.И.",
        "documentList": [
          {
            name: "Фото/скан паспорта",
            url: "http://mydoc.kemsu/...",
          },
          {
            name: "Заполненный документ",
            url: "http://mydoc.kemsu/...",
          },
        ],
      },
    },
    ],

    // app-filter
    filterList: [
      {
        name: 'institute',
        selected: '',

        placeholder: 'Институт',
        options: [
          'Институт Фундаментальных Наук',
          'Институт Цифры',
          'Институт Образования',
        ],
      },
      {
        name: 'courseNumber',
        selected: '',

        placeholder: 'Курс',
        options: [
          1,
          2,
          3,
          4,
          5,
          6,
        ],
      },
      {
        name: 'group',
        selected: '',

        placeholder: 'Группа',
        options: [
          'М-174',
          'М-175',
          'М-240',
        ],
      },
    ],
  }),

  computed: {
    checkedStudentList() {
      return this.searchingStudentList.filter(student => student.checked)
    },

    searchingStudentList() {
      if (this.searchText === '') return this.filteredStudentList

      return this.filteredStudentList.filter(student =>
        student.fullName.toLowerCase().includes(this.searchText.toLowerCase())
      )
    },

    filteredStudentList() {
      if (this.filterList.every(filter => filter.selected === ''))
        return this.studentList

      return this.studentList.filter(student =>
             this.filterList.filter(filter => filter.selected != '')
                            .every(filter => student[filter.name] === filter.selected))
    },

    selectedFilterNames() {
      return this.filterList.map(filter => filter.selected)
    },
  },

  methods: {
    // Методы AppSignStudentList
    check(student) {
      student.checked = true
    },
    uncheck(student) {
      student.checked = false
    },
    sign(student) {
      student.point.status = 'signed'
      this.uncheck(student)
    },
    reject(student) {
      // student.point.status = 'rejected'
      // this.uncheck(student)
      this.closeRejectForm()
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

    // Методы app-filter
    select(selected, filter) {
      filter.selected = selected
    },
    clear() {
      this.filterList.forEach(filter => filter.selected = '')
    },

    // Принимает на вход student
    openRejectForm() {
      // this.rejectModal.student = student
      this.rejectForm.isOpen = true
    },
    closeRejectForm() {
      this.rejectForm.isOpen = false
    },
  },
}
</script>

<style lang="less" scoped>

.container {
  // Настроить grid
  display: grid;
  grid-template-columns: 1fr 35%;
  grid-column-gap: 64px;

  .sign-main {
    padding-top: 48px;
  }
}


@media all and (max-width: 1800px) {

  .container {
    grid-column-gap: 32px;
  }

}

</style>
