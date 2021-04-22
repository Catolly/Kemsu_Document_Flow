<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>
		<app-button
		@click="openAddStatementForm"
		class="btn-open-add-statement-form blue filled">
			Добавить заявление
		</app-button>
		<app-list	class="bypass-sheet-list">
			<app-list-item
			v-for="bypassSheet in bypassSheets"
			:key="bypassSheet.id"
			@click="openBypassSheet(bypassSheet)"
			class="bypass-sheet">
				<div class="bypass-sheet-title">
					{{ bypassSheet.title }}
				</div>
			</app-list-item>
		</app-list>
	</div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'

export default {
	components: {
		AppButton,
		AppList,
    AppListItem,
	},
	methods: {
		openBypassSheet(bypassSheet) {
			this.$router.push('/bypass-sheets/' + bypassSheet.id)
		},
		openAddStatementForm() {
			this.$router.push('/bypass-sheets/create')
		}
	},
	data() {
		return {
			bypassSheets: [
				{
					id: 0,
					title: 'Скидка на столовую',
				},
				{
					id: 1,
					title: 'Отчисление',
				},
			]
		}
	}
}
</script>

<style lang="less" scoped>

.container {
  padding-top: 48px;
}

.bypass-sheet-list {
	margin-top: 32px;
}

.bypass-sheet-title {
	font-size: @fz-normal;
}
</style>
