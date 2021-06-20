<template>
  <form
    @submit.prevent=""
    class="app-deadlines-form"
  >
    <app-deadlines-topbar
      :allGroupsDeadline="allGroupsDeadline"
      @update:allGroupsDeadline="inputAllGroupsDeadline"
      @applyAllGroupsDeadline="applyAllGroupsDeadline"

      :searchText.sync="searchText"

      :page.sync="page"
      :itemsPerPage.sync="groupsPerPage"

      :sheetsTitle="sheetsTitle"
      :currentSheetTitle="currentSheetTitle"
      @changeSheet="changeSheet"

      :groupsAmount="searchingGroups.length"

      class="deadlines-topbar"
    />

    <template v-if="groupsInPage.length">
      <app-deadlines-table
        :currentSheet="currentSheet"
        :groups="groupsInPage"

        class="deadlines-table"
      />

      <app-button
        filled
        blue
        :loading="submiting"
        @click="$emit('submit', currentSheet)"
        class="submit-btn"
      >
        Сохранить
      </app-button>
    </template>

    <h2 v-else class="empty-message">
      Таких групп не было найдено
    </h2>
  </form>
</template>

<script>
import AppDeadlinesTable from '~/components/deadlines/AppDeadlinesTable'
import AppDeadlinesTopbar from '~/components/deadlines/AppDeadlinesTopbar'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppDeadlinesForm',

  components: {
    AppDeadlinesTable,
    AppDeadlinesTopbar,
    AppButton,
  },

  data:() => ({
    allGroupsDeadline: '',

    searchText: '',

    page: 0,
    groupsPerPage: 0,

    currentSheet: undefined,
  }),

  props: {
    submiting: {
      type: Boolean,
      default: false,
    },

    sheets: {
      type: Array,
      default:() => [],
    },
  },

  computed: {
    sheetsTitle() {
      return this.sheets
        .map(sheet => sheet.title)
    },

    currentSheetGroups() {
      if (!this.currentSheet) return []

      return this.currentSheet.deadlines
        .map(group => group)
    },

    searchingGroups() {
      return this.currentSheetGroups
        .filter(group =>
          group.groupName.includes(this.searchText)
        )
    },

    groupsInPage() {
      return this.searchingGroups
        .slice(
          this.page * this.groupsPerPage,
          (this.page + 1) * this.groupsPerPage
        )
    },

    currentSheetTitle() {
      if (!this.currentSheet) return ''

      return this.currentSheet.title
    },
  },

  watch: {
    sheets() {
      this.currentSheet = this.sheets[0]
    },

    searchText() {
      this.page = 0
    },

    groupsPerPage() {
      this.page = 0
    },
  },

  methods: {
    changeSheet(title) {
      this.currentSheet = this.sheets
        .find(sheet => sheet.title === title)
    },

    inputAllGroupsDeadline(value) {
      this.allGroupsDeadline = this.formateDate(value)
    },

    // formate - dd/mm/yyyy
    formateDate(value) {
      value = value.trim()

      if (value.length === 2 || value.length === 5)
        value += '/'

      return value.substring(0, 10)
    },

    applyAllGroupsDeadline() {
      this.currentSheetGroups
        .forEach(group => {
          group.deadline = this.allGroupsDeadline
        })
    },

    submit() {
      this.$emit('submit', currentSheet)
    },
  },
}
</script>

<style scoped lang="less">
.app-deadlines-form {
  display: flex;
  flex-direction: column;
  gap: 2em;

  .empty-message {
    margin-top: 1em;
  }

  .submit-btn {
    margin-left: auto;
  }
}
</style>
