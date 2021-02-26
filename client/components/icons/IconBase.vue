<template>
	<svg 
	:width="width" 
	:height="height" 
	viewBox="0 0 24 16"
	class="icon-base" 
	xmlns="http://www.w3.org/2000/svg">
		<slot />
	</svg>
</template>

<script>

export default {
	name: 'IconBase',
	props: {
		width: {
			type: [Number, String],
			default: 16
		},
		height: {
			type: [Number, String],
			default: 16
		},
	}
}
</script>