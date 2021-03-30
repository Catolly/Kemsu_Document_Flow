<template>
	<div class="container">
		<!-- student -->
		<the-page-bypass-sheets-student />
    
    <!-- staff -->
    <!-- <the-page-staff-bypass-sheets /> -->
    
    <!-- admin -->

  </div>
</template>

<script>
import ThePageBypassSheetsStudent from '~/components/bypass-sheets/ThePageBypassSheetsStudent'

export default {
  name: 'index',
  components: {
    ThePageBypassSheetsStudent,
  },
}
</script>

<style>

</style>