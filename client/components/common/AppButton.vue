<template>
	<button
	tabindex="0"
<<<<<<< Updated upstream:client/components/common/VButton.vue
	class="v-button">
||||||| constructed merge base:client/components/common/VButton.vue
	@click="$emit('click')"
	@keydown.enter="$emit('enter')"
	class="v-button">
=======
	@click="$emit('click')"
	@keydown.enter="$emit('enter')"
	class="app-button">
>>>>>>> Stashed changes:client/components/common/AppButton.vue
		<slot />
	</button>
</template>

<script>
export default {
	name: 'AppButton',
}
</script>

<style lang="less" scoped>

.app-button {
  color: @text-grey;
  font-size: @fz-normal;
  font-weight: @fw-normal;

  height: 50px;
  padding: 0;
	border: none;
	background: transparent;

	&:hover {
		color: #000;
    cursor: pointer;
	}
}

.big {
	height: 70px;
}

.fluid {
	width: 100%;
}

.red,
.green,
.blue {
  padding: 12px 48px;
  border-radius: 10px;
  font-weight: @fw-medium;

	&.filled {
		border: none;
		color: #fff;
	}
	&.filled:hover {
		color: #fff;
	}
}

.red {
	color: @red;
	border: 1px solid @red;
	&:focus,
	&:hover {
		color: #fff;
		background-color: @red-hover;
	}
	&.filled {
		background: @red;
	}
	&.filled:focus,
	&.filled:hover {
		background: @red-hover;
	}
}
.green {
	color: @green;
	border: 1px solid @green;
	&:focus,
	&:hover {
		color: #fff;
		background-color: @green;
	}
	&.filled {
		background: @green;
	}
	&.filled:focus,
	&.filled:hover {
		background: @green-hover;
	}
}
.blue {
	color: @blue;
	border: 1px solid @blue;
	&:focus,
	&:hover {
		color: #fff;
		background-color: @blue-hover;
	}
	&.filled {
		background: @blue;
	}
	&.filled:focus,
	&.filled:hover {
		background: @blue-hover;
	}
}

</style>
