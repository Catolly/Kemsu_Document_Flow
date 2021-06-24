<template>
  <roleStaff class="deadlines">
    <div class="header">
      <h1>Сроки</h1>
      <span v-if="fetchDeadlinesError" class="error-message">
        Не удалось загрузить обходные листы
      </span>
      <span v-if="patchDeadlinesError" class="error-message">
        Не удалось сохранить данные. Попробуйте еще раз
      </span>
      <span v-if="patchDeadlinesSuccess" class="success-message">
        Данные успешно сохранены
      </span>
    </div>

    <app-deadlines-form
      v-show="!fetchingDeadlines"
      :submiting="patchingDeadlines"
      :sheets="sheets"
      @submit="submit"
      class="deadlines-form"
    />

    <div
      v-show="fetchingDeadlines"
      class="loading-spinner"
    />
  </roleStaff>
</template>

<script>
import { BypassSheetsSchemasService } from '~/services/ApiService'

import roleStaff from '~/components/roles/roleStaff'
import AppDeadlinesForm from '~/components/deadlines/AppDeadlinesForm'

export default {
  name: 'deadlines',

  middleware: 'authenticated',

  components: {
    roleStaff,
    AppDeadlinesForm,
  },

  data:() => ({
    fetchDeadlinesError: '',
    patchDeadlinesError: '',

    fetchingDeadlines: false,
    patchingDeadlines: false,

    patchDeadlinesSuccess: false,

    sheets: [],
  }),

  async fetch() {
    try {
      this.fetchingDeadlines = true
      const { data } = await this.fetchSheetsDeadlines()
      this.sheets = data
    } catch (error) {
      console.error(error)
    } finally {
      this.fetchingDeadlines = false
    }
  },

  computed: {
    BypassSheetsSchemasService() {
      return BypassSheetsSchemasService
    },
  },

  methods: {
    fetchSheetsDeadlines() {
      try {
        return this.BypassSheetsSchemasService.getDeadlines()
      } catch (error) {
        this.fetchDeadlinesError = error
        throw error
      }
    },

    async submit(sheet) {
      this.patchingDeadlines = true
      this.patchDeadlinesSuccess = false
      this.patchDeadlinesError = ''
      try {
        await this.BypassSheetsSchemasService.patchDeadlines(
          sheet.id,
          {data: sheet.deadlines}
        )
        this.patchDeadlinesSuccess = true
      } catch (error) {
        this.patchDeadlinesError = error
      } finally {
        this.patchingDeadlines = false
      }
    },
  }
}
</script>

<style scoped lang="less">
.deadlines,
.header {
  display: flex;
  flex-direction: column;
}

.deadlines {
  padding-top: 3em;

  display: flex;
  flex-direction: column;
  gap: 2em;
}

.header {
  gap: .5em;
}

.loading-spinner {
  .spinner();
}

.deadlines-form {
  width: 1200px;
}
</style>
