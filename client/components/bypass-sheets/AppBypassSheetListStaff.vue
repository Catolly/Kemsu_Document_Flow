<template>
	<div class="container">
		<h1 class="header">Обходные листы</h1>

    <h2
      v-if="!loadError && (schemas.length === 0)"
      class="empty-message"
    >
      Нет обходных листов
    </h2>

    <p
      v-if="loadError"
      class="error-message"
    >
      Не удалось загрузить обходные листы
    </p>

    <div class="topbar">
      <app-pagination
        v-show="schemas.length > 0"
        :itemsAmount="schemas.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"
      />
    </div>

		<app-list	class="bypass-sheet-list">
      <template
        v-for="(schema, index) in schemasInPage"
      >
  			<app-list-item
          :key="index"
    			@click="$router.push('/bypass-sheets/signature/' + schema.id)"
    			class="bypass-sheet"
        >
  				<div class="bypass-sheet-title">
  					{{ schema.title }}
  				</div>
  			</app-list-item>
      </template>
		</app-list>
	</div>
</template>

<script>
import { mapGetters } from "vuex"
import { FETCH_BYPASS_SHEETS_SCHEMAS } from "~/store/actions.type"

import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppPagination from '~/components/common/AppPagination'

export default {
	name: 'AppBypassSheetListStaff',

	components: {
		AppList,
    AppListItem,
    AppPagination,
	},

	data:() => ({
    itemsPerPage: 0,
    page: 0,

    loadError: '',
	}),

  computed: {
    ...mapGetters(['bypassSheetsSchemas']),

    schemasInPage() {
      return this.schemas
      .slice(
        this.page * this.itemsPerPage,
        (this.page + 1) * this.itemsPerPage
      )
    },

    schemas() {
      return this.bypassSheetsSchemas
      .slice()
      .filter(schema => schema.points.length)
      .reverse()
    },
  },

  beforeMount() {
    try {
      this.$store
        .dispatch(
          FETCH_BYPASS_SHEETS_SCHEMAS,
          this.$store.getters.currentUser.department
        )
    } catch (error) {
      console.error(error)
      this.loadError = error
    }
  },
}
</script>

<style lang="less" scoped>
.container {
  padding-top: 48px;
}

.empty-message {
  margin-top: 48px;
}

.topbar {
  display: flex;
  justify-content: flex-end;
}

.bypass-sheet-list {
	margin-top: 32px;
}

.bypass-sheet-title {
  font-size: @fz-large;
  font-weight: @fw-normal;
}
</style>
