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

      <app-student-list
        :studentList="studentListInPage"
      />
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
import { mapGetters } from "vuex"
import {
  FETCH_USERS,
  FETCH_GROUPS,
} from "~/store/actions.type"

import { initFilterService } from '~/services/FilterService'

import roleAdmin from '~/components/roles/roleAdmin'

import AppFilter from '~/components/common/AppFilter'
import AppFilterNav from '~/components/common/AppFilterNav'
import AppSearch from '~/components/common/AppSearch'
import AppPagination from '~/components/common/AppPagination'
import AppStudentList from '~/components/users/AppStudentList'

export default {
  name: 'users',

  middleware: 'authenticated',

  components: {
    AppFilter,
    AppFilterNav,
    AppSearch,
    AppPagination,
    AppStudentList,
    roleAdmin,
  },

  data:() => ({
    searchText: '',
    itemsPerPage: 0,
    page: 0,

    fetchStudentsError: '',
    fetchGroupsError: '',

    studentList: [],

    FilterService: null,
  }),

  computed: {
    ...mapGetters(['users', 'groups']),

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
      if (!this.FilterService)
        return this.studentList

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

    async fetchUsers() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_USERS, {
            users: this.users,
          })
            .then(() => {
              this.users
                .forEach(user =>
                  this.studentList.push({
                    id: user.id,
                    fullname: user.fullname,
                    courseNumber: user.courseNumber,
                    group: user.group,
                    institute: user.institute,
                    sheets: user.bypassSheets,
                  })
                )
                resolve()
            })
            .catch(error => {
              console.error(error)
              this.loadError = error
              reject()
            })
      })
    },

    async fetchGrops() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_GROUPS, this.groups)
            .then(() => resolve())
            .catch(error => {
              console.error(error)
              this.loadError = error
              reject()
            })
      })
    },
  },

  beforeMount() {
    this.fetchUsers()
    this.fetchGrops()
      .then(() => this.FilterService = initFilterService(this.groups))
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
</style>
