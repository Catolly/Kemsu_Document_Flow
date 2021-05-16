<template>
  <roleAdmin class="container">
    <div class="main">
      <h1 class="header">Пользователи</h1>

      <div class="topbar">
        <app-filter-nav
          :filterPath="filterPath"
          @setFilterDepth="setFilterDepth"
          class="filter-nav"
        />
        <app-search
          round
          small
          v-model="searchText"
          class="search"
        />
      </div>

      <app-pagination
        v-if="searchingStudentList.length > 0"
        :itemsAmount="searchingStudentList.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"

        class="pagination"
      />

      <app-list class="student-list">
        <app-list-item
          v-for="(student, index) in studentListInPage"
          :key="index"
          class="student"
        >
          <div class="student-info">
            <span class="fullname">{{student.fullname}}</span>
            <span class="about">
              {{student.institute}},
              {{student.group}},
              {{student.courseNumber}} курс
            </span>
            <span
              v-for="(bypassSheet, index) in student.bypassSheetList"
              :key="index"
              :class="{'signed': bypassSheet.status === 'signed'}"
              class="bypass-sheets-status"
            >
              Обходной лист
              "{{bypassSheet.name}}"
              {{bypassSheet.status === 'signed' ? '' : ' не '}}
              подписан
            </span>
          </div>
          <app-button
            red
            class="ban"
            @click="ban(student)"
          >
            Заблокировать аккаунт
          </app-button>
        </app-list-item>
      </app-list>
    </div>

    <app-filter
      class="filter"
      :filterList="filterList"
      @select="select"
      @clear="clear"
    />
  </roleAdmin>
</template>

<script>
import { initFilterService } from '~/services/FilterService'

import roleAdmin from '~/components/roles/roleAdmin'

import AppFilter from '~/components/common/AppFilter'
import AppFilterNav from '~/components/common/AppFilterNav'
import AppSearch from '~/components/common/AppSearch'
import AppPagination from '~/components/common/AppPagination'
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'users',

  components: {
    AppFilter,
    AppFilterNav,
    AppSearch,
    AppPagination,
    AppList,
    AppListItem,
    AppButton,
    roleAdmin,
  },

  data:() => ({
    searchText: '',
    itemsPerPage: 0,
    page: 0,

    studentList: [
      {
        fullname: "Козырева Татьяна Андреевна",
        courseNumber: '4',
        group: "М-174",
        institute: "ИФН",
        bypassSheetList: [
          {
            name: 'Скидка на столовую',
            status: 'signed',
          },
          {
            name: 'Отчисление',
            status: 'reviewing',
          }
        ],
      },
      {
        fullname: "Сергиенко Анатолий Николаевич",
        courseNumber: '4',
        group: "М-174",
        institute: "ИФН",
        bypassSheetList: [
          {
            name: 'Скидка на столовую',
            status: 'signed',
          },
        ],
      },
      {
        fullname: "Люкшин Михаил Сергеевич",
        courseNumber: '3',
        group: "Ц-184",
        institute: "ИЦ",
        bypassSheetList: [
          {
            name: 'Скидка на столовую',
            status: 'signed',
          },
        ],
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
    studentListInPage() {
      return this.searchingStudentList.slice(this.page * this.itemsPerPage,
                                            (this.page + 1) * this.itemsPerPage)
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
      const selectedGroup = this.FilterService.get('Группа').value
      if (selectedGroup) {
        const postfix= this.FilterService.get('Курс').postfix
        const group = this.groups.find(group => group.name === selectedGroup)
        return [
          group.institute,
          group.courseNumber + postfix,
          group.name,
        ]
      }

      return this.FilterService.filterList.map(filter =>
        filter.value + (filter.value ? filter.postfix : '')
      )
    },
  },

  methods: {
    ban(student) {
      // делаем пост запрос на бан / разбан
    },

    // Методы app-filter
    select(params) {
      const [value, filter] = params
      this.FilterService.set(filter.placeholder, value)
    },
    clear() {
      this.FilterService.clear()
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
  },

  created() {
    this.FilterService = initFilterService(this.groups)
  },
}
</script>

<style lang="less" scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 30%;
  grid-column-gap: 64px;
}

.main {
  padding-top: 48px;

  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  margin-bottom: 24px;

  display: flex;
  flex-direction: column;
  gap: 16px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search {
  max-width: 340px;
}

.filter-nav {
  height: 100%;
  margin: 0;
}

.pagination {
  justify-content: flex-end;
}

.student {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.student-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .about {
    color: @grey-darkset;
  }
}

.bypass-sheets-status {
  font-size: @fz-small;
  color: @grey-darkset;
  &.signed {
    color: @green;
  }
}
</style>
