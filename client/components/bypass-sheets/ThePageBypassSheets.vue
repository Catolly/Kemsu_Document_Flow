<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>
		<v-button 
		@click.native="openAddStatementForm"
		class="btn-open-add-statement-form blue filled">
			Добавить заявление
		</v-button>
		<div class="bypass-sheet-list-wrapper">
			<v-list class="bypass-sheet-list">
					<v-list-item
					v-for="bypassSheet in bypassSheets"
					:key="bypassSheet.id"
					@click="openBypassSheet(bypassSheet)"
					class="bypass-sheet">
						<div class="bypass-sheet-title">
							{{ bypassSheet.title }}
						</div>
					</v-list-item>
			</v-list>
		</div>
	</div>
</template>

<script>
import VButton from '~/components/VButton'
import VList from '~/components/VList'
import VListItem from '~/components/VListItem'

export default {
	name: 'ThePageBypassSheet',
	components: {
		VButton,
		VList,
		VListItem,
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

.header {
	padding-top: 48px;
}

.btn-open-add-statement-form {
	margin-top: 48px;
}

.bypass-sheet-list-wrapper {
	margin-top: 32px;
}

.bypass-sheet-title {
	font-size: @fz-normal;
}
</style>