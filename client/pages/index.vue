<template>
	<div class="container">
    <!-- Вместо вставки компонент здесь будет редирект на компоненты как на страницы -->

		<!-- student -->
		<bypass-sheets />
    <!-- staff -->

    <!-- admin -->

  </div>
</template>

<script>
import BypassSheets from '~/pages/bypass-sheets/index'

export default {
  name: 'index',
  components: {
    BypassSheets,
  },
}
</script>

<style>

</style>