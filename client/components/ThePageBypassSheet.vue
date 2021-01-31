<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>
		<v-button 
		class="btn-add-statement blue filled">
			Добавить заявление
		</v-button>
		<div class="bypass-sheets">
			<bypass-sheet 
			v-for="bypassSheet in bypassSheets"
			:key="bypassSheet.title"
			:data="bypassSheet"
			/>
		</div>

	</div>
</template>

<script>
import VButton from '~/components/VButton'

export default {
	name: 'ThePageBypassSheet',
	components: {
		VButton,
	},
	data() {
		return {
			bypassSheets: [
				{
					title: 'Обходной лист',
					points: [
					{
						title: 'Пункт 1',
					},
					{
						title: 'Пункт 2',
					},
					],
				},
				{

				},
			]
		}
	}
}
</script>

<style lang="less" scoped>

</style>