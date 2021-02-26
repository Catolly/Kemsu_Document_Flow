<template>
	<icon-base
	width="24"
	height="16"
	class="icon-arrow-next">
		<path d="M23.185 8.46151C23.5755 8.07098 23.5755 7.43782 23.185 7.04729L16.8211 0.68333C16.4305 0.292805 15.7974 0.292805 15.4068 0.683329C15.0163 1.07385 15.0163 1.70702 15.4068 2.09754L21.0637 7.7544L15.4068 13.4113C15.0163 13.8018 15.0163 14.4349 15.4068 14.8255C15.7974 15.216 16.4305 15.216 16.821 14.8255L23.185 8.46151ZM0.477905 8.75439L22.4779 8.7544L22.4779 6.7544L0.477905 6.75439L0.477905 8.75439Z"/>
	</icon-base>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
	name: 'IconArrowNext',
	components: {
		IconBase
	}
}
</script>

<style scoped lang="less">

.icon-arrow-next {
	fill: #E0E0E0;

	&:hover {
		fill: #000;
	}
}

.icon-arrow-next.active {
	fill: #000;

	&:hover {
		fill: #E0E0E0;
	}
}

</style>