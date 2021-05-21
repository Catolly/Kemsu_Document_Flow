<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>

    <p
      v-if="loadError"
      class="error-message"
    >
      Не удалось загрузить обходные листы
    </p>

    <div class="topbar">
  		<app-button
    		@click="$router.push('/bypass-sheets/create')"
    		class="btn-open-add-statement-form blue filled"
      >
  			Добавить заявление
  		</app-button>

      <app-pagination
        v-if="bypassSheets.length > 0"
        :itemsAmount="bypassSheets.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"
      />
    </div>

		<app-list	class="bypass-sheet-list">
			<app-list-item
  			v-for="(bypassSheet, index) in bypassSheetsInPage"
  			:key="index"
  			@click="$router.push('/bypass-sheets/' + bypassSheet.id)"
  			class="bypass-sheet"
      >
				<div class="bypass-sheet-title">
					{{ bypassSheet.title }}
				</div>
			</app-list-item>
		</app-list>
	</div>
</template>

<script>
import { mapGetters } from "vuex"
import { FETCH_BYPASS_SHEETS } from "~/store/actions.type"

import AppButton from '~/components/common/AppButton'
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppPagination from '~/components/common/AppPagination'

export default {
  name: 'AppBypassSheetListStudent',

	components: {
		AppButton,
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
    ...mapGetters(['bypassSheets']),

    bypassSheetsInPage() {
      return this.bypassSheets
      .slice(
        this.page * this.itemsPerPage,
        (this.page + 1) * this.itemsPerPage
      )
    },
  },

  beforeMount() {
    this.$store
      .dispatch(FETCH_BYPASS_SHEETS, {
        bypassSheets: this.bypassSheets,
        // department: 'ИФН' //currentUser.department
      })
      .catch(error => {
        console.error(error)
        this.loadError = error
      })
  },
}
</script>

<style lang="less" scoped>
.container {
  padding-top: 48px;
}

.topbar {
  margin-top: 48px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-message {
  margin-top: 48px;
}

.bypass-sheet-list {
	margin-top: 32px;
}

.bypass-sheet {
  &.signed {
    border-color: @green;
    color: @green;
  }
}

.bypass-sheet-title {
	font-size: @fz-normal;
}
</style>
