<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>

    <p v-if="loadError" class="error-message">
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
        v-if="sheets.length > 0"
        :itemsAmount="sheets.length"
        :page="page"
        @updateItemsPerPage="itemsPerPage = $event"
        @updatePage="page = $event"
      />
    </div>

    <h2 v-if="!sheets.length && !loadError" class="empty-message">
      Нет обходных листов
    </h2>

		<app-list	class="bypass-sheet-list">
			<app-list-item
  			v-for="(sheet, index) in sheetsInPage"
  			:key="index"
  			@click="$router.push('/bypass-sheets/' + sheet.id)"
        :class="{'signed': sheet.status === bypassSheetSchema.Signed}"
  			class="bypass-sheet"
      >
				<div class="bypass-sheet-title">
					{{ sheet.title }}
				</div>
			</app-list-item>
		</app-list>
	</div>
</template>

<script>
import bypassSheetSchema from '~/services/bypassSheetSchema'

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

    sheetsInPage() {
      return this.sheets
      .slice(
        this.page * this.itemsPerPage,
        (this.page + 1) * this.itemsPerPage
      )
    },

    sheets() {
      return this.bypassSheets
      .slice()
      .reverse()
    },

    bypassSheetSchema() {
      return bypassSheetSchema
    },
  },

  beforeMount() {
    this.$store
      .dispatch(FETCH_BYPASS_SHEETS, {
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
