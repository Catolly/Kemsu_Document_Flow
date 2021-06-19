<template>
	<button
  	tabindex="0"
  	class="app-button"
    :class="classObj"
    :disabled="disabled"
  	@click="$emit('click')"
  	@keydown.enter="$emit('click')"
  >
    <span :class="{'hidden': loading}">
		  <slot />
    </span>
	</button>
</template>

<script>
export default {
	name: 'AppButton',

  props: {
    disabled: {
      type: Boolean,
      default: false,
    },

    round: {
      type: Boolean,
      default: false,
    },

    semiRound: {
      type: Boolean,
      default: false,
    },

    big: {
      type: Boolean,
      default: false,
    },

    red: {
      type: Boolean,
      default: false,
    },

    green: {
      type: Boolean,
      default: false,
    },

    blue: {
      type: Boolean,
      default: false,
    },

    cancel: {
      type: Boolean,
      default: false,
    },

    plain: {
      type: Boolean,
      default: false,
    },

    fluid: {
      type: Boolean,
      default: false,
    },

    underlined: {
      type: Boolean,
      default: false,
    },

    square: {
      type: Boolean,
      default: false,
    },

    filled: {
      type: Boolean,
      default: false,
    },

    icon: {
      type: Boolean,
      default: false,
    },

    loading: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    classObj() {
      return {
        'disabled': this.disabled,
        'round': this.round,
        'big': this.big,
        'red': this.red,
        'green': this.green,
        'blue': this.blue,
        'cancel': this.cancel,
        'plain': this.plain,
        'fluid': this.fluid,
        'underlined': this.underlined,
        'square': this.square,
        'filled': this.filled,
        'icon': this.icon,
        'semi-round': this.semiRound,
        'loading': this.loading,
      }
    },
  },
}
</script>

<style lang="less" scoped>

.app-button {
  position: relative;

  height: 50px;
  width: fit-content;

  padding: 12px 48px;
  border-radius: 10px;

  display: inline-flex;
  justify-content: center;
  align-items: center;

  color: @grey-darkset;
  .setInteractiveColor(color, @black, @black);

  font-size: @fz-normal;
  font-weight: @fw-medium;

	border: 1px solid @grey-darkset;
	background: none;

  cursor: pointer;
}

.square {
  padding: 0;

  height: 50px;
  width: 50px;

  &.big {
    min-height: 70px;
    min-width: 70px;
  }
}

.round {
  padding: 0;
  width: 50px;
  border-radius: 100%;
}

.semi-round {
  border-radius: 100px;
}

.big {
  min-height: 70px;
  min-width: 70px;

  .loading:after {
    width: 50px;
    height: 50px;

    top: calc(50% - 25px);
    left: calc(50% - 25px);
  }
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

.cancel {
  .setColor(@grey-darkset, @red-hover, @red-active);
}

.plain {
  height: fit-content;
  width: fit-content;
  padding: 0;

  font-weight: @fw-normal;
  background: none;
  border: none;
}

.disabled {
  cursor: auto;

  .setColor(@grey-darkset, @grey-darkset, @grey-darkset);
}

.filled {
  color: #fff;
}

.hidden {
  visibility: hidden;
}

// @keyframes spinner {
//   0% {
//     transform: rotate(0deg);
//   }
//   100% {
//     transform: rotate(360deg);
//   }
// }

.loading:after {
  .spinner();
  // content: " ";
  // display: block;
  // position: absolute;

  // top: calc(50% - 17.5px);
  // left: calc(50% - 17.5px);

  // width: 35px;
  // height: 35px;

  // border-radius: 50%;
  // border: 4px solid @black;
  // border-color: @black transparent @black transparent;

  // animation: spinner 1.2s linear infinite;
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
  .setInteractiveColor(border-color, @color-hover, @color-active);
  .setInteractiveColor(color, @white, @white);

  &.filled {
    background: @color;
    &.icon{
      fill: @white;
      .setInteractiveColor(fill, @white, @white);
    }
    &.loading:after {
      border-color: @white transparent @white transparent;
    }

    .setInteractiveColor(background, @color-hover, @color-active);
    .setInteractiveColor(border-color, @color-hover, @color-active);
  }

  &.plain {
    .setInteractiveColor(background, none, none);
    .setInteractiveColor(color, @color-hover, @color-active);
  }

  &.icon {
    border-color: transparent;
    fill: @black;

    .setInteractiveColor(background, none, none);
    .setInteractiveColor(color, @color-hover, @color-active);
    .setInteractiveColor(border-color, transparent, transparent);
    .setInteractiveColor(fill, @color-hover, @color-active);
  }

  &.loading {
    &:after {
      border-color: @color transparent @color transparent;
    }
    &:hover,
    &:active {
      &:after {
        border-color: @white transparent @white transparent;
      }
    }
  }
}

</style>
