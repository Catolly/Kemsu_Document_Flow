<template>
	<button
  	tabindex="0"
  	class="app-button"
  	@click="$emit('click')"
  	@keydown.enter="$emit('click')"
  >
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
  height: 50px;
  width: fit-content;

  padding: 12px 48px;
  border-radius: 10px;

  color: @grey-darkset;
  .setInteractiveColor(color, @black, @black);

  font-size: @fz-normal;
  font-weight: @fw-medium;

	border: 1px solid @grey-darkset;
	background: none;

  cursor: pointer;
}

.big {
  height: 70px;
}

.fluid {
  width: 100%;
}

.underlined {
  text-decoration: underline;
}

.red {
	.setColor(@red, @red-hover, @red-active);
}

.green {
  .setColor(@green, @green-hover, @green-active);
}

.blue {
  .setColor(@blue, @blue-hover, @blue-active);
}

.plain {
  height: fit-content;
  width: fit-content;
  padding: 0;

  font-weight: @fw-normal;
  background: none;
  border: none;
}




.filled {
  color: #fff;
}

.setInteractiveColor(@prop, @color-hover, @color-active) {
  &:focus-visible,
  &:hover {
    @{prop}: @color-hover;
  }
  &:active {
    @{prop}: @color-active;
  }
}

.setColor(@color, @color-hover, @color-active) {
  color: @color;
  border-color: @color;

  .setInteractiveColor(background, @color-hover, @color-active);
  .setInteractiveColor(color, @white, @white);

  &.filled {
    background: @color;

    .setInteractiveColor(background, @color-hover, @color-active);
  }

  &.plain {
    .setInteractiveColor(background, none, none);
    .setInteractiveColor(color, @color-hover, @color-active);
  }
}

</style>
