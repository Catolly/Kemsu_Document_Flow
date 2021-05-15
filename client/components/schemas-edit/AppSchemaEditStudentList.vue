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
        v-model="searchText"
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
        v-if="searchingStudentList.length > 0"
        :itemsAmount="searchingStudentList.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"

        class="pagination"
      />
    </div>

    <app-student-list
      :studentList="studentList"
    />
  </div>
</template>

<script>
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
    filterPath: {
      type: Array,
      required: true,
    },

    studentList: {
      type: Array,
      required: true,
    },
  },

  data:() => ({
    searchText: '',
    page: 0,
    itemsPerPage: 0,
  }),

  computed: {
    studentListInPage() {
      return this.searchingStudentList.slice(this.page * this.itemsPerPage,
                                            (this.page + 1) * this.itemsPerPage)
    },
    checkedStudentList() {
      return this.searchingStudentList.filter(student => student.checked)
    },
    searchingStudentList() {
      if (this.searchText === '') return this.studentList

      return this.studentList.filter(student =>
        student.fullname.toLowerCase().includes(this.searchText.toLowerCase())
      )
    },
  },

  methods: {
    check(student) {
      // student.checked = true
      this.$set(student, 'checked', true)
    },
    uncheck(student) {
      // student.checked = false
      this.$set(student, 'checked', false)
    },
    checkAll() {
      this.searchingStudentList.forEach(this.check)
    },
    uncheckAll() {
      this.checkedStudentList.forEach(this.uncheck)
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
