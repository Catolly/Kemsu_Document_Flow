<template>
  <roleAdminStaff class="status">
    <div class="header">
      <h1>Статус обходного листа</h1>
      <span v-if="fetchUsersError" class="error-message">
        Не удалось загрузить данные обходного листа
      </span>
    </div>

    <app-status-topbar
      :searchText.sync="searchText"

      :page.sync="page"
      :itemsPerPage.sync="usersPerPage"

      :sheetsTitle="sheetsTitle"
      :currentSheetTitle="currentSheetTitle"
      @changeSheetTitle="changeSheetTitle"

      :usersAmount="usersAmount"

      class="status-topbar"
    />

    <app-status-table
      v-show="!fetchingUsers"
      :users="users"
      :usersAmount="usersAmount"
      :schemaTitle="currentSheetTitle"
      class="status-table"
    />

    <div
      v-show="fetchingUsers"
      class="loading-spinner"
    />
  </roleAdminStaff>
</template>

<script>
import _ from 'lodash'

import { UsersService } from '~/services/ApiService'
import { BypassSheetsSchemasService } from '~/services/ApiService'

import { mapGetters } from 'vuex'

import roleAdminStaff from '~/components/roles/roleAdminStaff'

import AppStatusTable from '~/components/status/AppStatusTable'
import AppStatusTopbar from '~/components/status/AppStatusTopbar'

export default {
  name: 'status',

  middleware: 'authenticated',

  components: {
    roleAdminStaff,
    AppStatusTable,
    AppStatusTopbar,
  },

  data:() => ({
    fetchSheetsTitlesError: '',
    fetchingSheetsTitles: false,
    sheetsTitle: [],

    fetchUsersError: '',
    fetchingUsers: false,
    users: [],
    usersAmount: 0,

    currentSheetTitle: '',

    searchText: '',

    page: 0,
    usersPerPage: 0,
  }),

  fetch() {
    try {
      this.fetchSchemasTitles()
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters(['currentUser']),

    BypassSheetsSchemasService() {
      return BypassSheetsSchemasService
    },

    UsersService() {
      return UsersService
    },
  },

  watch: {
    sheetsTitle() {
      this.currentSheetTitle = this.sheetsTitle[0]
      this.fetchUsers()
    },

    searchText() {
      this.page = 0
      this.fetchUsersDebounced()
    },

    usersPerPage() {
      this.page = 0
      this.fetchUsers()
    },

    page() {
      this.fetchUsers()
    },
  },

  methods: {
    changeSheetTitle(title) {
      this.currentSheetTitle = title
    },

    async fetchSchemasTitles() {
      try {
        this.fetchingSheetsTitles = true
        const { data } = await this.BypassSheetsSchemasService.getTitles()
        this.sheetsTitle = data.map(schema => schema.title)
      } catch (error) {
        this.fetchSheetsTitlesError = error
        console.error(error)
      } finally {
        this.fetchingSheetsTitles = false
      }
    },

    async fetchUsers() {
      try {
        if (this.fetchingUsers) return
        if (!this.sheetsTitle.length) return
        this.fetchingUsers = true
        const { data } = await this.UsersService.get({
          title: this.currentSheetTitle,
          institute: this.currentUser.institute,
          limit: this.usersPerPage,
          offset: this.page * this.usersPerPage,
          search: this.searchText,
        })
        this.users = data.students
        this.usersAmount = data.studentsAmount
      } catch (error) {
        this.fetchUsersError = error
        console.error(error)
      } finally {
        this.fetchingUsers = false
      }
    },

    fetchUsersDebounced: _.debounce(async function() {
      this.fetchUsers()
    }, 500)
  }
}
</script>

<style scoped lang="less">
.status,
.header {
  display: flex;
  flex-direction: column;
}

.status {
  padding-top: 3em;

  display: flex;
  flex-direction: column;
  gap: 2em;

  &-topbar,
  &-table {
    width: 1300px;
  }
}

.header {
  gap: .5em;
}

.loading-spinner {
  .spinner();
}
</style>
