<template>
  <div class="app-schema-edit-point-settings">
    <div class="required-settings">
      <h2 class="title">{{point.title}}</h2>

      <div class="description">
        <span class="header">Сообщение для выбранного пункта</span>
        <app-text-field
          v-model="point.description"
        />
      </div>

      <div class="upload-section">
        <span class="header">Прикрепить документы к пункту</span>
        <div class="upload-wrapper">
          <app-upload
            class="upload"
            @upload="point.requiredDocuments = Array.from($event)"
          />
          <app-upload-list
            v-if="point.requiredDocuments.length"
            :documentList="point.requiredDocuments"
            class="upload-list"
            @delete="deleteDocument"
          />
        </div>
      </div>
    </div>

    <div class="optional-settings">
      <h2>Дополнительные настройки</h2>

      <div class="gender">
        <span class="header">Пол</span>
        <app-radio-group
          :optionList="genderList"
          v-model="point.gender"
        />
      </div>

      <div class="common-reasons">
        <span class="header">Частые причины отказа</span>
        <div class="new-reason">
          <app-input
            v-model="commonReason"
            :placeholder="'Например, вы сдали не все документы'"
            class="field"
          />
          <app-button
            big
            square
            class="add-btn"
            @click="addCommonReason(commonReason)"
          >
            <div class="plus" />
          </app-button>
        </div>
        <div class="chipses">
          <app-chips
            v-for="(reason, index) in point.commonReasons"
            :key="index"
            small
            semi-round
            class="chips"
            @click="deleteCommonReason(reason)"
          >
            {{reason}}
            <div class="delete-chips-btn">
              <div class="minus" />
            </div>
          </app-chips>
        </div>
      </div>

      <div class="student-upload-documents">
        <span class="header">Загружаемые студентом документы</span>
        <span v-if="!point.uploadDocumentsFormat.length">
          Нет обязательных для заполнения документов к этому пункту
          <br>
          Добавить документ:
        </span>
        <div
          v-for="(doc, index) in point.uploadDocumentsFormat"
          :key="index"
          class="document"
        >
          <span>Документ {{index+1}}</span>
          <div class="document-body">
            <app-input
              v-model="doc.title"
              :placeholder="'Название документа'"
              class="field"
            />
            <app-button
              big
              square
              filled
              class="delete-btn"
              @click="deleteUploadDocumentsFormat(doc)"
            >
              <div class="minus" />
            </app-button>
          </div>
        </div>
        <app-button
          big
          round
          class="add-btn"
          @click="addUploadDocumentsFormat"
        >
          <div class="plus" />
        </app-button>
      </div>
    </div>
  </div>
</template>

<script>
import AppTextField from '~/components/common/AppTextField'
import AppUpload from '~/components/common/AppUpload'
import AppUploadList from '~/components/common/AppUploadList'
import AppRadioGroup from '~/components/common/AppRadioGroup'
import AppInput from '~/components/common/AppInput'
import AppButton from '~/components/common/AppButton'
import AppChips from '~/components/common/AppChips'

export default {
  name: 'AppSchemaEditPointSettings',

  components: {
    AppTextField,
    AppUpload,
    AppUploadList,
    AppRadioGroup,
    AppButton,
    AppInput,
    AppChips,
  },

  data:() => ({
    commonReason: '',
  }),

  props: {
    point: {
      type: Object,
      required: true,
    },

    genderList: {
      type: Array,
      required: true,
    }
  },

  methods: {
    deleteCommonReason(commonReason) {
      this.point.commonReasons = this.point.commonReasons
        .filter(reason => reason !== commonReason)
    },

    addCommonReason(commonReason) {
      if (!commonReason) return
      this.point.commonReasons.push(commonReason)
      this.commonReason = ''
    },

    deleteUploadDocumentsFormat(deletingDoc) {
      this.point.uploadDocumentsFormat =
      this.point.uploadDocumentsFormat
      .filter(doc => doc != deletingDoc)
    },

    addUploadDocumentsFormat() {
      this.point.uploadDocumentsFormat =
      this.point.uploadDocumentsFormat
      .concat([{ title: '' }])
    },

    deleteDocument(deletingDoc) {
      this.point.requiredDocuments =
      this.point.requiredDocuments
      .filter(doc => doc != deletingDoc)
    },
  },
}
</script>

<style lang="less" scoped>
.app-schema-edit-point-settings {
  display: flex;
  flex-direction: column;
  gap: 48px;

  & > * {
    display: flex;
    flex-direction: column;
    gap: 32px;

    & > * {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
  }
}

.title {
  max-width: 80%;
}

.header {
  font-weight: @fw-normal;
}

.upload-section {
  display: flex;
  gap: 16px;
}

.upload-wrapper {
  display: flex;
  grid-gap: 16px;
  gap: 16px;
}

.upload {
  flex-shrink: 0;
}

.plus {
  .plus();
}

.minus {
  .minus();
}

.field {
  max-width: 500px;
}

.document {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chipses {
  flex-flow: wrap;
  max-width: 500px;
}

.document-body,
.new-reason,
.chipses {
  display: flex;
  gap: 8px;
}

.add-btn,
.delete-btn {
  background: @grey-bright;
  border: 1px solid @grey-light;
}

.add-btn {
  &:hover {
    background: @grey-light;
    border-color: @blue;
  }
}

.delete-btn {
  &:hover {
    border-color: @red;

    .minus:before,
    .minus:after {
      background: @red;
    }
  }
}

.chips {
  display: flex;
  gap: 8px;
  transition: 0.1s;

  .delete-chips-btn {
    position: relative;
    height: 24px;
    width: 24px;
  }
  &:hover {
    .minus:before,
    .minus:after {
      background: @white;
    }
  }
}
</style>
