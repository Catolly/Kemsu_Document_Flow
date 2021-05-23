<template>
  <div class="app-schema-edit-student-list">
    <div class="topbar">
      <app-filter-nav
        :filterPath="filterPath"
        @setFilterDepth="$emit('setFilterDepth', $event)"
        class="filter-nav"
      />
      <app-search
        round
        small
        :value="searchText"
        @change="searchText = $event"
        class="search"
      />

      <div class="check-btns">
        <app-button
          plain
          green
          class="btn"
          @click="checkAll"
        >
          Выбрать всех
        </app-button>
        <app-button
          plain
          class="btn"
          @click="uncheckAll"
        >
          Снять выбор
        </app-button>
      </div>
      <app-pagination
        v-show="studentList.length > 0"
        :itemsAmount="usersAmount"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"

        class="pagination"
      />
    </div>

    <app-student-list
      :studentList="studentList"
      @check="check($event)"
      @uncheck="uncheck($event)"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { FETCH_USERS } from "~/store/actions.type"
import { copy } from "~/store/methods"

import AppFilterNav from '~/components/common/AppFilterNav'
import AppSearch from '~/components/common/AppSearch'
import AppButton from '~/components/common/AppButton'
import AppPagination from '~/components/common/AppPagination'
import AppStudentList from '~/components/schemas-edit/AppStudentList'

export default {
  name: 'AppSchemaEditStudentList',

  components: {
    AppFilterNav,
    AppSearch,
    AppButton,
    AppPagination,
    AppStudentList,
  },

  props: {
    schemaStudentList: {
      type: Array,
      required: true,
    },

    filterPath: {
      type: Array,
      required: true,
    },

    filters: {
      type: Array,
      required: true,
    },
  },

  data:() => ({
    searchText: '',
    page: 0,
    itemsPerPage: 0,

    studentList: [],
    checkedStudents: []
  }),

  computed: {
    ...mapGetters(['users', 'usersAmount']),
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
      this.checkedStudents = []
    },
  },

  methods: {
    check(student) {
      this.$set(student, 'checked', true)
      this.checkedStudents.push(student)
      this.schemaStudentList.push(student.id)
    },
    uncheck(unckechingStudent) {
      this.$set(unckechingStudent, 'checked', false)
      this.checkedStudents = this.checkedStudents.filter(student => student !== unckechingStudent)
      this.schemaStudentList
        .splice(this.schemaStudentList.indexOf(unckechingStudent.id), 1)
    },
    checkAll() {
      this.studentList.forEach(student => {
        if (!this.schemaStudentList.includes(student.id)) {
          this.check(student)
        }
      })
    },
    uncheckAll() {
      this.checkedStudents.forEach(student => {
        this.$set(student, 'checked', false)
      })
      this.checkedStudents = []
      this.schemaStudentList.splice(0)
      this.checkAttachedStudents()
    },
    checkAttachedStudents() {
      this.studentList.forEach(student => {
        this.$set(student, 'checked', this.schemaStudentList.includes(student.id))
      })
    },

    async findUsers() {
      try {
        const [
          institute,
          course,
          group
        ] = this.filters.map(filter => filter)
        await this.$store
          .dispatch(FETCH_USERS, {
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
        this.loadError = error
      }
    },
  },
}
</script>

<style lang="less" scoped>
.app-schema-edit-student-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.topbar {
  display: grid;
  grid-template-columns: repeat(2, max-content);
  justify-content: space-between;
  align-items: center;
  grid-gap: 16px;
}

.filter-nav {
  height: 100%;
  margin: 0;
}

.check-btns {
  display: flex;
  gap: 16px;
}

.search {
  max-width: 340px;
}

.list {
  position: relative;
}

.pagination,
.search {
  justify-self: flex-end;
}

.group-list,
.student-list {
  padding-left: 64px;
  padding-right: 64px;
}

.list-item {
  position: relative;
}

.list-body {
  display: flex;
  align-items: center;
  gap: 16px;
}

.toggle {
  .arrow();

  top: auto;

  &.open {
    transform: rotate(180deg);
  }
}
</style>
