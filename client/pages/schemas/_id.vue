<template>
  <roleAdmin class="container">
    <form
      @submit.prevent=""
      :class="{'step-two': step == '2'}"
      class="form"
    >
      <div class="form-wrapper">
        <div class="head">
          <h1 class="header">Редактирование обходного листа</h1>

          <app-delete-schema-dialog
            class="delete"
            :loading="deleteLoading"
            @delete="deleteSchema"
          />
        </div>

        <span
          v-if="loadError"
          class="error-message"
        >
          Не удалось загрузить шаблон
        </span>

        <span
          v-if="updateSuccess"
          class="success-message"
        >
          Шаблон сохранен!
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
          v-if="schema && FilterService && !loadError"
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
                :loading="submitLoading"
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
  FETCH_GROUPS,
  UPDATE_BYPASS_SHEETS_SCHEMA,
  DELETE_BYPASS_SHEETS_SCHEMA,
} from "~/store/actions.type"

import { initFilterService } from '~/services/FilterService'
import bypassSheetSchema from '~/services/bypassSheetSchema'

import roleAdmin from '~/components/roles/roleAdmin'

import AppSchemaEditForm from '~/components/schemas-edit/AppSchemaEditForm'
import AppDeleteSchemaDialog from '~/components/schemas-edit/AppDeleteSchemaDialog'
import AppFilter from '~/components/common/AppFilter'
import AppButton from '~/components/common/AppButton'

export default {
  middleware: 'authenticated',

  components: {
    roleAdmin,
    AppSchemaEditForm,
    AppDeleteSchemaDialog,
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
    updateSuccess: false,
    submitLoading: false,
    deleteLoading: false,

    isInvalidForm: true,

    schema: null,
    departments: [],

    FilterService: null,
  }),

  computed: {
    ...mapGetters(['groups', 'bypassSheetsSchema']),

    loadError() {
      return this.loadDepartmentsError
      && this.loadUsersError
      && this.loadGroupsError
      && this.loadSchemaError
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
      this.step = this.$route.query.step || 1
    },
  },

  methods: {
    async submit() {
      if (this.isInvalidForm || this.submitLoading) return

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

    async fetchSchema() {
      return await this.$store
        .dispatch(FETCH_BYPASS_SHEETS_SCHEMA, {id: this.$route.params.id})
          .catch(error => {
            console.error(error)
            this.loadSchemaError = error
          })
    },

    async updateSchema() {
      this.updateError = ''
      this.updateSuccess = false
      this.submitLoading = true
      this.$store
        .dispatch(UPDATE_BYPASS_SHEETS_SCHEMA, {
          id: this.schema.id,
          title: this.schema.title,
          description: this.schema.description,
          educationForm: this.schema.educationForm,
          statements: this.schema.statements,
          studentList: this.schema.studentList,
          points: this.schema.points
            .filter(point => point.checked),
        })
          .then(() => this.updateSuccess = true)
          .catch(error => {
            console.error(error)
            this.updateError = error
          })
          .finally(() => this.submitLoading = false)
    },

    async fetchDepartments() {
      return new Promise((resolve, reject) => {
        this.$store
          .dispatch(FETCH_DEPARTMENTS)
            .then(departments => {
              this.departments = departments

              // Установка checked=true у подключенных к шаблону отделов
              this.schema.points
                .forEach(point => {
                  this.$set(point, 'checked', true)
                  point.uploadDocumentsFormat = point.uploadDocumentsFormat
                    .map(format => ({
                      title: format
                    }))
                  point.gender = bypassSheetSchema.genderList[point.gender]
                })

              const departmentTitles = []
              // Установка checked=false у остальных отделов
              this.departments
                .filter(department =>
                  !this.schema.points
                    .find(point =>
                      department.title === point.title
                    )
                )
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
              this.loadDepartmentsError = error
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
              console.error(error)
              this.loadGroupsError = error
              reject(error)
            })
      })
    },

    async deleteSchema() {
      if (this.deleteLoading) return
      try {
        this.deleteLoading = true
        await this.$store
          .dispatch(DELETE_BYPASS_SHEETS_SCHEMA, this.schema.id)
        this.$router.push({ path: '..', append: true })
      } catch (error) {
        console.error(error)
      } finally {
        this.deleteLoading = false
      }
    }
  },

  async beforeMount() {
    this.schema = await this.fetchSchema()
    this.schema.statements
    this.schema.points
        .forEach(point => {
          if (!point.uploadDocumentsFormat)
            this.$set(point, 'uploadDocumentsFormat', [])
        })

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

.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-message,
.success-message {
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
