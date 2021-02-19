<template>
	<div class="v-image-upload">
		<div class="plus"></div>
	</div>
</template>

<script>
export default {
	name: 'VImageUpload'
}
</script>

<style lang="less" scoped>

.v-image-upload {
	position: relative;

	background: #FDFDFD;
	border: 1px solid #D2D2D2;
	border-radius: 5px;

	transition: .2s ease all;
	cursor: pointer;

	&:hover {
		background: #F2F2F2;
		border-color: @blue;
	}
}

.plus {
	position: absolute;

	@size: 20px;
	width: @size;
	height: @size;

	top: 50% - .25*@size;
	bottom: 50%;
	left: 50%;
	right: 50%;

	&::before,
	&::after {
		.absolute();
		background: #000;

		width: 10%;
		height: 100%;
	}

	&::before {
		transform: rotate(90deg);
	}
}

</style>