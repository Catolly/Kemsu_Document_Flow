<template>
	<div class="container">
		<h1 class="header">Обходные листы</h1>
		<app-list	class="bypass-sheet-list">
			<app-list-item
			v-for="bypassSheet in bypassSheets"
			:key="bypassSheet.id"
			@click="openBypassSheet(bypassSheet)"
			class="bypass-sheet">
				<div class="bypass-sheet-title">
					{{ bypassSheet.title }}
				</div>
				<div
				v-if="bypassSheet.newCount > 0"
				class="bypass-sheet-new-count">
					+{{ bypassSheet.newCount }}
				</div>
				<div
				v-else
				class="bypass-sheet-count">
					{{ bypassSheet.count }}
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
	name: 'bypassSheetListStaff',

	components: {
		AppButton,
		AppList,
    AppListItem,
	},

	data() {
		return {
			bypassSheets: [
				{
					id: 0,
					title: 'Скидка на столовую',
					count: 35,
				},
				{
					id: 1,
					title: 'Отчисление',
					count: 50,
					newCount: 40,
				},
			],
		}
	},

  methods: {
    openBypassSheet(bypassSheet) {
      this.$router.push('/bypass-sheets/signature/' + bypassSheet.id)
    },
  },
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

.bypass-sheet-new-count {
	position: relative;
	color: @red;

	&:before {
		.absolute();
		top: -100%;
		left: calc(-1.75em + 45%);

		width: 70px;
		height: 70px;

		border: 1px solid @red;
		border-radius: 50%;
	}
}

</style>
