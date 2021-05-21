<template>
  <form class="upload-form" @submit.prevent="submit">
    <template v-if="point.requiredDocuments.length">
      <h2>Отправить документы</h2>
      <div class="upload-section">
        <div
          v-for="(format, index) in point.uploadDocumentsFormat"
          :key="index"
          class="upload-body"
        >
          <span class="title">
            {{format.title}}
          </span>

          <div class="upload-wrapper">
            <app-upload
              class="upload"
              @upload="setRequiredDocuments(format, $event)"
            />
            <app-upload-list
              v-if="format.uploadedDocuments.length"
              :documentList="format.uploadedDocuments"
              class="upload-list"
              @delete="deleteRequiredDocument(format, $event)"
            />
          </div>
        </div>
      </div>
    </template>

    <h2 v-else>Отправить на подписание</h2>

    <div class="submit-section">
      <span v-if="updateError" class="error-message">
        Не удалось отправить данные
      </span>
      <app-button blue filled class="submit">
        Отправить
      </app-button>
    </div>
  </form>
</template>

<script>
import { UPDATE_BYPASS_SHEET } from '~/store/actions.type'

import AppUpload from '~/components/common/AppUpload'
import AppUploadList from '~/components/common/AppUploadList'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppBypassSheetPointForm',

  components: {
    AppUpload,
    AppUploadList,
    AppButton,
  },

  data:() => ({
    updateError: '',
  }),

  props: {
    point: {
      type: Object,
      required: true,

      uploadedDocuments: {
        type: Array,
      },
      uploadDocumentsFormat: {
        type: Array,
      },
    },
  },

  methods: {
    async submit() {
      try {
        this.updateError = ''
        await this.$store.dispatch(UPDATE_BYPASS_SHEET, {
          point: this.point,
          id: this.$route.params.id,
        })
        this.$emit('success')
      } catch (error) {
        console.error(error)
        this.updateError = error
      }
    },

    reduceFiles() {
      this.point.uploadedDocuments = this.point.uploadDocumentsFormat
        .reduce((allFiles, format) => {
          return [...allFiles, ...format.uploadedDocuments]
        }, [])
    },

    setRequiredDocuments(point, uploadedDocuments) {
      point.uploadedDocuments = Array.from(uploadedDocuments)
    },

    deleteRequiredDocument(point, deletingDoc) {
      point.uploadedDocuments = point.uploadedDocuments.filter(doc =>
        doc != deletingDoc)
    },
  },

  beforeMount() {
    if (
      typeof this.point.uploadDocumentsFormat === 'undefined'
      || !this.point.uploadDocumentsFormat.length
    ) {
      this.$set(this.point, 'uploadDocumentsFormat', [
          { title: 'Необходимые документы' },
        ])
    }

    this.point.uploadDocumentsFormat.forEach(format => {
      this.$set(format, 'uploadedDocuments', [])
    })

    this.$watch('point.uploadDocumentsFormat', this.reduceFiles, { deep: true })
  },
}
</script>

<style lang="less" scoped>
.upload-form,
.upload-section,
.upload-body,
.submit-section {
  display: flex;
  flex-direction: column;
}

.upload-form {
  gap: 24px;
}

.upload-section {
  gap: 16px;
}

.upload-body {
  gap: 8px;
}

.upload-wrapper {
  display: flex;
  gap: 16px;
}

.upload {
  flex-shrink: 0;
}

.submit-section {
  gap: 8px;
}
</style>
