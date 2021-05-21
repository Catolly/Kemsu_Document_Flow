<template>
	<roleStudent class="container">
		<form
      @submit.prevent="submit"
      class="form"
    >
      <div class="form-body">
  			<h1 class="header">Обходной лист</h1>
        <p
          v-if="errors"
          class="error-message"
        >
          Не удалось создать обходной лист. Попробуйте позже
        </p>

  			<app-select
          v-model="selectedReason"
    			:options="bypassSheetsSchemas.map(schema => schema.title)"
    			placeholder="Причина"
    			class="reason"
        />

        <div
          v-if="selectedSchema && selectedSchema.statements.length"
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

          <div class="upload-section-body">
            <div class="example-subsection">
              <span class="subheader">Образец</span>
              <div class="example-documents">
                <app-download-file
                  v-for="(file, index) in selectedSchema.statements"
                  :key="index"
                  :file="file"
                  class="example-document"
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
        >
					Отправить
				</app-button>
			</div>
		</form>
	</roleStudent>
</template>

<script>
import { mapGetters } from 'vuex'
import { FETCH_BYPASS_SHEETS_SCHEMAS_TITLES, CREATE_BYPASS_SHEET } from '~/store/actions.type'

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

    fetchSchemasTitlesError: '',
	}),

  async fetch() {
    try {
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
    selectedSchema() {
      if (this.selectedReason === '') return null
      return this.bypassSheetsSchemas.find(schema => schema.title === this.selectedReason)
    },
    ...mapGetters(['bypassSheetsSchemasTitles']),

    bypassSheetsSchemas() {
      return [
        {
          title: 'Скидка на столовую',
          statements: [ // здесь лежат файлы
            { name: 'Скидка на столовую.pdf' },
          ]
        },
        {
          title: 'Отчисление',
          statements: [ // здесь лежат файлы
            { name: 'Отчисление1.pdf' },
            { name: 'Отчисление2.pdf' },
          ]
        },
      ]
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

      if (this.$v.$invalid) return

      this.create()
    },

    create() {
      const formData = new FormData()
      formData.append('statements', this.statements)
      formData.append('title', this.selectedReason)

      // for (const [key, value] of formData) {
      //   console.log(key, value)
      // }

      BypassSheetsService.post(formData)
        .then(() => this.back())
        .catch(errors => this.errors = errors)
    },

    back() {
      const path = this.$route.path
      this.$router.push(path.substring(0, path.lastIndexOf('/')))
    }
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
