<template>
  <form
    @submit.prevent=""
    class="app-reject-form"
  >
    <app-button
      icon
      square
      red
      class="close-btn"
      @click="close"
    >
      <icon-close />
    </app-button>

    <div class="head">
      <h1>Отказать</h1>

      <span>
        <span class="header">
          {{student.fullname}}
        </span>
        <br>
        <span class="student-status">
          {{student.group}},
          {{student.courseNumber}} курс.
          {{student.recruitmentForm}}.
          {{student.status}}.
        </span>
      </span>
    </div>

    <div class="reason">
      <div class="section">
        <span class="header">Загрузить документы</span>
        <div class="upload-wrapper">
          <app-upload
            small
            class="upload"
            @upload="setRequiredDocuments"
          />
          <app-upload-list
            v-if="requiredDocuments.length"
            small
            :documentList="requiredDocuments"
            class="upload-list"
            @delete="deleteRequiredDocument"
          />
        </div>
      </div>

      <div class="section">
        <span class="header">Сообщение</span>
        <app-text-field
          v-model="rejectReason"
          :rows="3"
          class="reason-text-field"
        />
        <div class="common-reason-crisps">
          <app-chips
            v-for="(reason, index) in commonReasons"
            :key="index"
            class="chips"
            @click="rejectReason = rejectReason + reason"
          >
            {{reason}}
          </app-chips>
        </div>
      </div>
    </div>

    <app-button
      class="reject-btn red filled"
      @click="reject"
    >
      Отказать
    </app-button>
  </form>
</template>

<script>
import { mapGetters } from 'vuex'

import AppButton from '~/components/common/AppButton'
import IconClose from '~/components/icons/IconClose'
import AppTextField from '~/components/common/AppTextField'
import AppChips from '~/components/common/AppChips'
import AppUpload from '~/components/common/AppUpload'
import AppUploadList from '~/components/common/AppUploadList'


export default {
  name: 'AppRejectForm',

  components: {
    AppButton,
    IconClose,
    AppTextField,
    AppChips,
    AppUpload,
    AppUploadList,
  },

  data:() => ({
    rejectReason: '',
    requiredDocuments: [],
  }),

  props: {
    student: {
      type: Object,
      required: true,

      point: {
        type: Object,
        required: true,

        rejectReason: {
          type: String,
          default: '',
        },
        requiredDocuments: {
          type: Array,
          default:() => [],
        },
      },
    },
  },

  computed: {
    ...mapGetters(['bypassSheetsSchema', 'currentUser']),

    commonReasons() {
      return this.bypassSheetsSchema.points
        .find(point => point.title === this.currentUser.department)
        .commonReasons
    }
  },

  methods: {
    clearFormData() {
      this.rejectReason = ''
      this.requiredDocuments = []
    },

    reject() {
      this.student.point.rejectReason = this.rejectReason,
      this.student.point.requiredDocuments = this.requiredDocuments,
      this.$emit('reject', this.student)

      this.clearFormData()
    },

    close() {
      this.$emit('close')
    },

    setRequiredDocuments(requiredDocuments) {
      this.requiredDocuments = Array.from(requiredDocuments)
    },

    deleteRequiredDocument(deletingDoc) {
      this.requiredDocuments = this.requiredDocuments.filter(doc =>
        doc != deletingDoc)
    },
  },
}
</script>

<style lang="less" scoped>
.app-reject-form {
  position: relative;

  display: flex;
  flex-direction: column;
  gap: 24px;

  width: 900px;

  .close-btn {
    position: absolute;
    top: 0;
    right: 0;
  }

  .header {
    font-weight: @fw-normal;
  }

  .head,
  .reason {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .student-status {
    color: @text-grey;
  }

  .section {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .upload-wrapper {
    display: flex;
    gap: 16px;
  }

  .upload {
    flex-shrink: 0;
  }

  .common-reason-crisps {
    display: flex;
    flex-flow: row wrap;
    gap: 8px;
  }
}

</style>
