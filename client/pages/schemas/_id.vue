<template>
  <roleAdmin
    :class="{'step-two': step == '2'}"
    class="container"
  >
    <form @submit.prevent="">
      <div class="form-wrapper">
        <h1 class="header">Редактирование обходного листа</h1>

        <span
          v-if="loadError"
          class="error-message"
        >
          Не удалось загрузить форму
        </span>

        <div
          v-if="!loadError"
          class="steps"
        >
          <NuxtLink
            :class="{
              'current': step == '1',
              'has-error': isInvalidForm && step != '1'
            }"
            class="step"
            :to="{
              path: this.$route.path,
              query: { step: '1' }
            }"
          >
          Шаг 1
          </NuxtLink>

          <NuxtLink
            :class="{'current': step == '2'}"
            class="step"
            :to="{
              path: this.$route.path,
              query: { step: '2' }
            }"
          >
          Шаг 2
          </NuxtLink>
        </div>

        <app-schema-edit-form
          v-if="schema && filteredStudentList && !loadError"
          :step="step"
          :studentList="filteredStudentList"
          :schema="schema"
          :filterPath="filterPath"
          @setFilterDepth="setFilterDepth"
          @changeStep="step = $event"
          @touch="isInvalidForm = $event"
          class="edit-form"
        />
      </div>

      <div
        v-show="step == '2'"
        class="filter-section"
      >
        <app-filter
          v-if="schema && filterList && !loadError"
          :filterList="filterList"
          @select="select"
          @clear="clear"
          class="filter"
        />

        <div class="submit-section">
          <div class="submit">
            <span
              v-if="updateError"
              class="error-message"
            >
              Не удалось обновить обходной лист
            </span>

            <div v-if="!loadError" class="nav-btns">
              <NuxtLink
                class="clear"
                tabindex="-1"
                :to="{
                  path: this.$route.path,
                  query: { step: '1' }
                }"
                append
              >
                <app-button
                  cancel
                  class="back"
                >
                  Назад
                </app-button>
              </NuxtLink>

              <app-button
                filled
                blue
                class="next-step"
                :disabled="isInvalidForm"
                @click="submit"
              >
                Сохранить
              </app-button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </roleAdmin>
</template>

<script>
import { mapGetters } from "vuex"
import {
  FETCH_BYPASS_SHEETS_SCHEMA,
  FETCH_DEPARTMENTS,
  FETCH_USERS,
  FETCH_GROUPS,
  UPDATE_BYPASS_SHEETS_SCHEMA,
} from "~/store/actions.type"

import { initFilterService } from '~/services/FilterService'

import roleAdmin from '~/components/roles/roleAdmin'

import AppSchemaEditForm from '~/components/schemas-edit/AppSchemaEditForm'
import AppFilter from '~/components/common/AppFilter'
import AppButton from '~/components/common/AppButton'

export default {
  middleware: 'authenticated',

  components: {
    roleAdmin,
    AppSchemaEditForm,
    AppFilter,
    AppButton,
  },

  data:() => ({
    step: '1',

    loadDepartmentsError: '',
    loadUsersError: '',
    loadGroupsError: '',
    loadSchemaError: '',
    updateError: '',

    isInvalidForm: true,

    studentList: [],
    schema: null,
    departments: [],

    FilterService: null,
  }),

  computed: {
    ...mapGetters(['users', 'groups', 'bypassSheetsSchema']),

    loadError() {
      return this.loadDepartmentsError
      && this.loadUsersError
      && this.loadGroupsError
      && this.loadSchemaError
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
        const filterCourseNumber = this.FilterService.get('Курс')
        const postfix = filterCourseNumber ? filterCourseNumber.postfix : ''
        const group = this.groups.find(group => group.name === selectedGroup)
        return [
          group.institute || '',
          (group.courseNumber ? (group.courseNumber + postfix) : ''),
          group.name,
        ]
      }

      return this.FilterService.filterList.map(filter =>
        filter.value + (filter.value ? filter.postfix : '')
      )
    },
  },

  watch: {
    '$route.query.step'() {
      this.step = this.$route.query.step
    },
  },

  methods: {
    async submit() {
      if (this.isInvalidForm) return

      await this.updateSchema()
    },

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

    // Методы app-filter
    select(params) {
      const [value, filter] = params
      this.FilterService.set(filter.placeholder, value)
    },
    clear() {
      this.FilterService.clear()
    },
    //

    checkAttachedStudents() {
      this.studentList.forEach(student => {
        this.$set(student, 'checked',
          this.schema.studentList
          && this.schema.studentList.includes(student.id))
      })
    },

    async fetchSchema() {
      return await this.$store
        .dispatch(FETCH_BYPASS_SHEETS_SCHEMA, {id: this.$route.params.id})
          .catch(error => {
            this.loadSchemaError = error
          })
    },

    async updateSchema() {
      this.updateError = ''
      this.$store
        .dispatch(UPDATE_BYPASS_SHEETS_SCHEMA, {
          // id: this.schema.id, в ответе get/schema/id не вкладывается id
          id: this.$route.params.id,
          title: this.schema.title,
          description: this.schema.description,
          educationForm: this.schema.educationForm,
          statements: this.schema.statements,
          studentList: this.studentList
            .filter(student => student.checked)
            .map(student => student.id),
          points: this.schema.points
            .filter(point => point.checked),
        })
          .catch(error => {
            this.updateError = error
          })
    },

    async fetchDepartments() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_DEPARTMENTS, {
            institute: 'ИФН' //currentUser.institute
          })
            .then(departments => {
              this.departments = departments

              // Установка checked=true у подключенных к шаблону отделов
              this.schema.points
                .forEach(point => this.$set(
                  point, 'checked', true
                ))

              // Установка checked=false у остальных отделов
              this.departments
                .filter(department =>
                  !this.schema.points
                    .find(point =>
                      department.title === point.title
                    )
                )
                .forEach(department =>
                  this.schema.points.push({
                    title: department.title,
                    description: '',
                    gender: '',
                    studentUploadDocuments: [],
                    requiredDocuments: [],
                    uploadDocumentsFormat: [],
                    checked: false,
                  })
                )
                resolve()
            })
            .catch(error => {
              this.loadDepartmentsError = error
              reject(error)
            })
      })
    },

    async fetchUsers() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_USERS, {
            users: this.users,
            // offset: 0,
            // limit: 20,
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
                  })
                )
                resolve()
            })
            .catch(error => {
              this.loadUsersError = error
              reject(error)
            })
      })
    },

    async fetchGrops() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_GROUPS, this.groups)
            .then(() => resolve())
            .catch(error => {
              this.loadGroupsError = error
              reject(error)
            })
      })
    },
  },

  beforeMount() {
    this.fetchSchema()
      .then(schema => {
        this.schema = schema
        this.fetchDepartments()
        this.fetchUsers()
          .then(() => this.checkAttachedStudents())
        this.fetchGrops()
          .then(() => this.FilterService = initFilterService(this.groups))
      })
  },

  created() {
    if (this.$route.query.step)
      this.step = this.$route.query.step
  },
}
</script>

<style lang="less" scoped>
.container {
  padding-bottom: 0;

  &.step-two {
    display: grid;
    grid-template-columns: 1fr 30%;
    grid-gap: 48px;
  }
}

.form-wrapper {
  padding: 48px 0;
}

.error-message {
  margin-top: 8px;
  color: @red;
}

.steps {
  margin-top: 24px;

  display: flex;
  gap: 24px;
}

.step:not(.current) {
  color: @grey-darkset;
  border-color: transparent;

  &:hover {
    color: @blue-hover;
  }

  &:after,
  &:hover:after {
    border-color: transparent;
  }

  &.has-error {
    color: @red;
    &:hover {
      color: @red-hover;
    }
  }
}

.edit-form {
  margin-top: 48px;
}

.filter-section {
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.filter {
  height: fit-content;
  flex-grow: 1;
}

.submit-section {
  border-left: 1px solid @grey-medium;
  padding-top: 48px;
  padding-bottom: 48px;

  display: flex;
  justify-content: flex-end;
}

.submit {
  width: fit-content;

  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-btns {
  display: flex;
  gap: 16px;
}
</style>