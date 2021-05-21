<template>
	<div class="container">
		<h1 class="header">Обходные листы</h1>

    <h2
      v-if="bypassSheetsSchemas.length === 0 && !loadError"
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
        v-if="bypassSheetsSchemas.length > 0"
        :itemsAmount="bypassSheetsSchemas.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"
      />
    </div>

		<app-list	class="bypass-sheet-list">
			<app-list-item
  			v-for="(bypassSheetsSchemas, index) in bypassSheetSchemasInPage"
  			:key="index"
  			@click="$router.push('/bypass-sheets/signature/' + bypassSheetsSchemas.id)"
  			class="bypass-sheet"
      >
				<div class="bypass-sheet-title">
					{{ bypassSheetsSchemas.title }}
				</div>

				<div class="bypass-sheet-count">
					{{ bypassSheetsSchemas.count }}
				</div>
			</app-list-item>
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

    bypassSheetSchemasInPage() {
      return this.bypassSheetsSchemas
      .slice(
        this.page * this.itemsPerPage,
        (this.page + 1) * this.itemsPerPage
      )
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
	font-size: @fz-normal;
}
</style>
