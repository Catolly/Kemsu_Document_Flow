<template>
	<icon-base
	width="12"
  height="12"
	class="icon-download">
		<path d="M5.64662 9.43412C5.84189 9.62938 6.15847 9.62938 6.35373 9.43412L9.53571 6.25214C9.73097 6.05688 9.73097 5.74029 9.53571 5.54503C9.34045 5.34977 9.02387 5.34977 8.8286 5.54503L6.00018 8.37346L3.17175 5.54503C2.97649 5.34977 2.65991 5.34977 2.46464 5.54503C2.26938 5.74029 2.26938 6.05688 2.46464 6.25214L5.64662 9.43412ZM5.50018 0.0805664L5.50018 9.08057L6.50018 9.08057L6.50018 0.0805664L5.50018 0.0805664ZM0 12.0806H12V11.0806H0V12.0806Z" />
	</icon-base>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
	name: 'IconDownload',
	components: {
		IconBase
	}
}
</script>

<style scoped lang="less">
.icon-download {
	fill: #000;
}
</style>
