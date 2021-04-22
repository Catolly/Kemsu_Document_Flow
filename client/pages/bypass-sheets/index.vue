<template>
	<div class="container">
		<!-- student -->
		<!-- <bypass-sheet-list-student /> -->

		<!-- staff -->
		<bypass-sheet-list-staff />
	</div>
</template>

<script>
import bypassSheetListStudent from '~/pages/bypass-sheets/bypassSheetListStudent'
import bypassSheetListStaff from '~/pages/bypass-sheets/bypassSheetListStaff'

export default {
	components: {
		bypassSheetListStudent,
    bypassSheetListStaff,
	},
}
</script>

<style lang="less" scoped>

</style>
