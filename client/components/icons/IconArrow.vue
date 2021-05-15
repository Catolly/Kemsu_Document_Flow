<template>
	<icon-base
	width="24"
	height="16"
	class="icon-arrow">
		<path d="M0.292892 7.39397C-0.0976315 7.78449 -0.0976315 8.41766 0.292892 8.80818L6.65685 15.1721C7.04738 15.5627 7.68054 15.5627 8.07107 15.1721C8.46159 14.7816 8.46159 14.1485 8.07107 13.7579L2.41421 8.10107L8.07107 2.44422C8.46159 2.0537 8.46159 1.42053 8.07107 1.03001C7.68054 0.639482 7.04738 0.639482 6.65685 1.03001L0.292892 7.39397ZM23 7.10107L1 7.10107V9.10107L23 9.10107V7.10107Z"/>
	</icon-base>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
	name: 'IconArrow',
	components: {
		IconBase
	}
}
</script>

<style scoped lang="less">
.icon-arrow {
	fill: #000;

	&:hover {
		fill: @blue;
	}
}
</style>
