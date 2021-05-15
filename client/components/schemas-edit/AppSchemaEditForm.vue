<template>
  <div class="app-schema-edit-form">
      <app-schema-edit-settings
        v-if="schema && schema.points"
        v-show="step === '1'"
        :schema="schema"
        :points="schema.points"
        :genderList="genderList"
        @touch="isInvalidForm = $event"
      />
      <app-schema-edit-student-list
        v-if="studentList"
        v-show="step === '2'"
        :filterPath="filterPath"
        :studentList="studentList"
        @setFilterDepth="$emit('setFilterDepth', $event)"
        class="edit-student-list"
      />
  </div>
</template>

<script>
import bypassSheetSchema from '~/services/bypassSheetSchema'

import AppSchemaEditSettings from '~/components/schemas-edit/AppSchemaEditSettings'
import AppSchemaEditStudentList from '~/components/schemas-edit/AppSchemaEditStudentList'

export default {
  name: 'AppSchemaEditForm',

  components: {
    AppSchemaEditSettings,
    AppSchemaEditStudentList,
  },

  data:() => ({
    isInvalidForm: true,
  }),

  props: {
    step: {
      type: String,
      required: true,
    },

    studentList: {
      type: Array,
      default:() => [],
    },

    schema: {
      type: Object,
      required: true,
    },

    filterPath: {
      type: Array,
      required: true,
    },
  },

  computed: {
    bypassSheetSchema() {
      return bypassSheetSchema
    },

    genderList() {
      return Object.values(bypassSheetSchema.genderList)
    },
  },

  watch: {
    isInvalidForm() {
      this.$emit('touch', this.isInvalidForm)
    },
  },
}
</script>
