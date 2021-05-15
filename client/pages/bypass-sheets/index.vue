<template>
	<div class="container">
		<!-- student -->
		<!-- <app-bypass-sheet-list-student /> -->

		<!-- staff -->
		<app-bypass-sheet-list-staff />
	</div>
</template>

<script>
import AppBypassSheetListStudent from '~/components/bypass-sheets/AppBypassSheetListStudent'
import AppBypassSheetListStaff from '~/components/bypass-sheets/AppBypassSheetListStaff'

export default {
	components: {
		AppBypassSheetListStudent,
    AppBypassSheetListStaff,
	},
}
</script>

<style lang="less" scoped>

</style>
