<template>
  <div class="app-schema-edit-main-settings">
    <div class="title">
      <span class="header">Причина</span>
      <app-input
        class="title-field"
        v-model="schema.title"
        :messages="['Обязательное поле']"
        :errorMessages="[
          ... $v.schema.title.$dirty
              && !$v.schema.title.required
              ? ['Поле должно быть заполнено']
              : [],
        ]"
        @input="reset($v.schema.title)"
        @change="checkField($v.schema.title)"
      />
    </div>

    <div class="education-form">
      <span class="header">Форма обучения</span>
      <app-radio-group
        :optionList="educationFormList"
        v-model="schema.educationForm"
      />
    </div>

    <div class="required-documents">
      <span class="header">Документы для создания заявления:</span>
      <div class="upload-wrapper">
        <app-upload
          class="upload"
          @upload="schema.statements = Array.from($event)"
        />
        <app-upload-list
          v-if="schema.statements.length"
          :documentList="schema.statements"
          class="upload-list"
          @delete="deleteDocument"
        />
      </div>
    </div>
  </div>
</template>

<script>
import bypassSheetSchema from '~/services/bypassSheetSchema'

import { required } from "vuelidate/lib/validators"

import AppInput from '~/components/common/AppInput'
import AppRadioGroup from '~/components/common/AppRadioGroup'
import AppUpload from '~/components/common/AppUpload'
import AppUploadList from '~/components/common/AppUploadList'

export default {
  name: 'AppSchemaEditMainSettings',

  components: {
    AppInput,
    AppRadioGroup,
    AppUpload,
    AppUploadList,
  },

  validations: {
    schema: {
      title: { required },
    },
  },

  props: {
    schema: {
      type: Object,
      required: true,
    },
  },

  computed: {
    educationFormList() {
      return Object.values(bypassSheetSchema.educationFormList)
    },
  },

  methods: {
    deleteDocument(deletingDoc) {
      this.schema.statements = this.schema.statements.filter(doc => doc != deletingDoc)
    },

    reset($v) {
      if (!$v.required) return

      $v.$reset()
    },

    checkField($v) {
      $v.$model = $v.$model.trim()

      $v.$touch()
    },
  },

  created(){
    this.$watch('$v.$invalid', () => {
        this.$emit('touch', this.$v.$invalid)
    }, {
      deep: true,
      immediate: true,
    })
  },
}
</script>

<style lang="less" scoped>
.app-schema-edit-main-settings {
  display: flex;
  flex-direction: column;
  gap: 32px;

  & > * {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
}

.header {
  font-weight: @fw-normal;
}

.title-field {
  max-width: 500px;
}

.upload-wrapper {
  display: flex;
  gap: 16px;
}

.upload {
  flex-shrink: 0;
}
</style>
