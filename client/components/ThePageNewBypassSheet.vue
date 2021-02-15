<template>
	<div class="container">
		<h1 class="header">Обходной лист</h1>
		<v-select />
	</div>
</template>

<script>
import VButton from '~/components/VButton'
import VSelect from '~/components/VSelect'

export default {
	name: 'ThePageNewBypassSheet',
	components: {
		VButton,
		VSelect
	},
	methods: {
	},
	data() {
		return {

		}
	}
}
</script>

<style lang="less" scoped>

.header {
	padding-top: 48px;
}

</style>