<template>
  <roleAdmin class="container">
    <form
      @submit.prevent=""
      :class="{'step-two': step == '2'}"
      class="form"
    >
      <div class="form-wrapper">
        <h1 class="header">Создание обходного листа</h1>

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
          <nuxt-link
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
          </nuxt-link>

          <nuxt-link
            :class="{'current': step == '2'}"
            class="step"
            :to="{
              path: this.$route.path,
              query: { step: '2' }
            }"
          >
          Шаг 2
          </nuxt-link>
        </div>

        <app-schema-edit-form
          v-if="!loadError && FilterService"
          :step="step"
          :schema="schema"
          :filterPath="filterPath"
          :filters="FilterService.filterList.map(filter => filter.value)"
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
          v-if="!loadError"
          :filterList="filterList"
          @select="select"
          @clear="clear"
          class="filter"
        />

        <div class="submit-section">
          <div class="submit">
            <span
              v-if="createError"
              class="error-message"
            >
              Не удалось создать обходной лист
            </span>

            <div class="nav-btns">
              <nuxt-link
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
              </nuxt-link>

              <app-button
                filled
                blue
                class="next-step"
                :disabled="isInvalidForm"
                :loading="submitLoading"
                @click="submit"
              >
                Создать
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
  FETCH_DEPARTMENTS,
  FETCH_GROUPS,
  CREATE_BYPASS_SHEETS_SCHEMA,
} from "~/store/actions.type"

import { initFilterService } from '~/services/FilterService'

import roleAdmin from '~/components/roles/roleAdmin'

import AppSchemaEditForm from '~/components/schemas-edit/AppSchemaEditForm'
import AppFilter from '~/components/common/AppFilter'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'new',

  middleware: 'authenticated',

  components: {
    roleAdmin,
    AppSchemaEditForm,
    AppFilter,
    AppButton,
  },

  data:() => ({
    step: '1',

    loadError: '',
    createError: '',

    isInvalidForm: true,
    submitLoading: false,

    points: [],

    schema: {
      title: '',
      educationForm: '',
      studentList: [],
      statements: [],
      points: [],
    },

    FilterService: null,
  }),

  computed: {
    ...mapGetters(['departments', 'groups']),

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
      this.step = this.$route.query.step || 1
    },
  },

  methods: {
    async submit() {
      if (this.isInvalidForm || this.submitLoading) return

      await this.createSchema()
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

    async createSchema() {
      this.createError = ''
      this.submitLoading = true
      try {
        await this.$store
          .dispatch(CREATE_BYPASS_SHEETS_SCHEMA, {
            title: this.schema.title,
            educationForm: this.schema.educationForm,
            statements: this.schema.statements,
            studentList: this.schema.studentList,
            points: this.schema.points
              .filter(point => point.checked),
          })
        this.$router.push({ path: '..', append: true })
      } catch (error) {
        console.error(error)
        this.createError = error
      } finally {
        this.submitLoading = false
      }
    },

    async fetchDepartments() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_DEPARTMENTS)
            .then(() => {
              const departmentTitles = []
              this.departments
                .forEach(department => {
                  if (departmentTitles.includes(department.title)) return
                  departmentTitles.push(department.title)
                  this.schema.points.push({
                    title: department.title,
                    description: '',
                    gender: '',
                    studentUploadDocuments: [],
                    requiredDocuments: [],
                    uploadDocumentsFormat: [],
                    commonReasons: [],
                    checked: false,
                  })
                })
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
    this.fetchDepartments()
    this.fetchGrops()
      .then(() => this.FilterService = initFilterService(this.groups))
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
}

.form {
  &.step-two {
    height: 100vh;

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
  position: fixed;
  bottom: 48px;
  right: 48px;

  // border-left: 1px solid @grey-medium;
  // padding-top: 48px;
  // padding-bottom: 48px;

  // display: flex;
  // justify-content: flex-end;
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
