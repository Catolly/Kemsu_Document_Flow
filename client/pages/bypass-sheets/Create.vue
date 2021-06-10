<template>
	<roleStudent class="container">
		<form
      @submit.prevent="submit"
      class="form"
    >
      <div class="form-body">
  			<h1 class="header">Обходной лист</h1>

        <p v-if="createError" class="error-message">
          Не удалось создать обходной лист. Попробуйте позже
        </p>

        <p v-if="fetchSchemasTitlesError" class="error-message">
          Не удалось загрузить список обходных листов. Попробуйте позже
        </p>

  			<app-select
          v-model="selectedReason"
    			:options="bypassSheetsSchemasTitles.map(schema => schema.title)"
    			placeholder="Причина"
    			class="reason"
        />

        <div
          v-if="selectedSchema.statements && selectedSchema.statements.length"
          class="upload-section"
        >
          <div class="upload-section-head">
            <h2 class="header">Необходимые документы</h2>
            <p
              v-if="$v.statements.$dirty && !$v.statements.required"
              class="error-message"
            >
              Загрузите документы
            </p>
          </div>

          <div v-if="selectedSchema" class="upload-section-body">
            <div class="example-subsection">
              <span class="subheader">Образец</span>
              <div class="example-documents">
                <app-download-file
                  v-for="(file, index) in selectedSchema.statements"
                  :key="index"
                  :file="file"
                  big
                />
              </div>
            </div>
            <div class="upload-subsection">
              <span class="subheader">Заявление</span>
              <div class="upload-wrapper">
                <app-upload
                  class="upload"
                  big
                  @upload="setStatements"
                />
                <app-upload-list
                  v-if="statements.length"
                  :documentList="statements"
                  big
                  class="upload-list"
                  @delete="deleteStatement"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

			<div class="btns-wrapper">
				<app-button class="btn btn-cancel red">
					Отмена
				</app-button>
				<app-button
          class="btn btn-submit blue filled"
          :disabled="$v.$invalid"
          :loading="createLoading"
        >
					Отправить
				</app-button>
			</div>
		</form>
	</roleStudent>
</template>

<script>
import { mapGetters } from 'vuex'
import {
  FETCH_BYPASS_SHEETS_SCHEMAS_TITLES,
  CREATE_BYPASS_SHEET,
  WAIT_FOR
} from '~/store/actions.type'

import { required } from "vuelidate/lib/validators"

import roleStudent from '~/components/roles/roleStudent'

import AppButton from '~/components/common/AppButton'
import AppSelect from '~/components/common/AppSelect'
import AppUpload from '~/components/common/AppUpload'
import AppUploadList from '~/components/common/AppUploadList'
import AppDownloadFile from '~/components/common/AppDownloadFile'


export default {
	name: 'create',

  middleware: 'authenticated',

	components: {
    roleStudent,
		AppButton,
		AppSelect,
		AppUpload,
    AppUploadList,
    AppDownloadFile,
	},

	data:() => ({
    selectedReason: '',
    statements: [],

    createError: '',
    createLoading: false,
    fetchSchemasTitlesError: '',
	}),

  async fetch() {
    try {
      await this.$store.dispatch(WAIT_FOR, 'checkingAuth')
      await this.$store.dispatch(FETCH_BYPASS_SHEETS_SCHEMAS_TITLES, {
        educationForm: this.$store.getters.currentUser.educationForm
      })
    } catch (error) {
      console.error(error)
      this.fetchSchemasTitlesError = error
    }
  },

  validations:() => ({
    selectedReason: {
      required,
    },
    statements: {
      required,
    },
  }),

  computed: {
    ...mapGetters(['bypassSheetsSchemasTitles', 'currentUser']),

    selectedSchema() {
      if (this.selectedReason === '') return {
        statements: []
      }
      return this.bypassSheetsSchemasTitles.find(schema => schema.title === this.selectedReason)
    },
  },

  watch: {
    selectedReason() {
      this.checkField(this.$v.selectedReason)
    },
    statements() {
      this.checkField(this.$v.statements)
    },
  },

  methods: {
    setStatements(statements) {
      this.statements = Array.from(statements)
    },

    deleteStatement(deletingStatement) {
      this.statements = this.statements.filter(statement =>
        statement != deletingStatement)
    },

    checkField($v) {
      $v.$touch()
    },

    submit() {
      this.$v.$touch()

      if (this.$v.$invalid || this.createLoading) return

      this.create()
    },

    async create() {
      try {
        this.createLoading = true
        await this.$store.dispatch(CREATE_BYPASS_SHEET, {
          title: this.selectedSchema.title,
          statements: this.selectedSchema.statements,
        })
        this.$router.push({ path: '..', append: true })
      } catch (error) {
        console.error(error)
        this.createError = error
      } finally {
        this.createLoading = false
      }
    },
  },
}
</script>

<style lang="less" scoped>
.container {
  padding-top: 48px;
  display: table;

  height: 100%;
  width: 100%;
}

.form {
  height: 100%;

  display: grid;
  grid-template-columns: 1fr max-content;
  grid-column-gap: 48px;
}

.reason {
	margin-top: 40px;
  max-width: 500px;
}

.upload-section {
	padding-top: 48px;

  display: flex;
  flex-direction: column;
  gap: 24px;
}

.upload-section-head {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upload-section-body {
  display: flex;
  flex-flow: wrap;
  gap: 24px;
}

.example-subsection,
.upload-subsection {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-subsection {
  min-width: 50%;
}

.example-document {
  height: 200px;
  width: 200px;
}

.example-documents,
.upload-wrapper {
  display: flex;
  gap: 16px;
}

.example-documents {
  flex-flow: wrap;
}

.upload {
  flex-shrink: 0;
}

.btns-wrapper {
	display: flex;
  gap: 16px;

  align-self: flex-end;
}
</style>
