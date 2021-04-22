<template>
	<button
  	tabindex="0"
  	class="app-button"
  	@click="$emit('click')"
  	@keydown.enter="$emit('enter')"
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
  color: @text-grey;
  font-size: @fz-normal;
  font-weight: @fw-normal;

  height: 50px;
  width: fit-content;
  padding: 0;
	border: none;
	background: transparent;

  &:focus-visible,
	&:hover {
		color: #000;
    cursor: pointer;
	}

  &.big {
    height: 70px;
  }

  &.fluid {
    width: 100%;
  }

  &.icon {
    height: fit-content;
    width: fit-content;
  }
}

.plain,
.icon {
  &.red,
  &.green,
  &.blue,
  &.cancel {
    padding: 0;
    background: none;
    border: none;

    font-size: @fz-normal;
    font-weight: @fw-normal;

    &:hover,
    &:focus-visible,
    &:active, {
      background: none;
      border: none;
    }
  }
}

.underlined {
  text-decoration: underline;
}

.red,
.green,
.blue,
.cancel {
  padding: 12px 48px;
  border-radius: 10px;
  font-weight: @fw-medium;
}

.red,
.green,
.blue {
  &:focus-visible,
  &:hover,
  &:active:not(:focus-visible),
  &:active:not(:hover) {
    color: #fff;
  }

	&.filled {
		border: 1px solid transparent;
		color: #fff;
	}
	&.filled:hover {
		color: #fff;
	}
}

.red {
	color: @red;
	border: 1px solid @red;

	&:focus-visible,
	&:hover {
		background: @red;
	}
  &:active {
    background: @red-active;
  }

	&.filled {
		background: @red;

  	&:focus-visible,
  	&:hover {
  		background: @red-hover;
  	}
    &:active {
      background: @red-active;
    }
  }

  &.plain {
    color: @red;

    &:focus-visible,
    &:hover {
      color: @red-hover;
    }
    &:active {
      color: @red-active;
    }
  }
}

.green {
	color: @green;
	border: 1px solid @green;

	&:focus-visible,
	&:hover {
		background: @green;
	}
  &:active {
    background: @green-active;
  }

  &.filled {
		background: @green;

    &:focus-visible,
    &:hover {
      background: @green-hover;
    }
    &:active {
      background: @green-active;
    }
  }

  &.plain {
    color: @green;

    &:focus-visible,
    &:hover {
      color: @green-hover;
    }
    &:active {
      color: @green-active;
    }
  }
}

.blue {
  color: @blue;
  border: 1px solid @blue;

  &:focus-visible,
  &:hover {
    background: @blue;
  }
  &:active {
    background: @blue-active;
  }

  &.filled {
    background: @blue;

    &:focus-visible,
    &:hover {
      background: @blue-hover;
    }
    &:active {
      background: @blue-active;
    }
  }

  &.plain {
    color: @blue;

    &:focus-visible,
    &:hover {
      color: @blue-hover;
    }
    &:active {
      color: @blue-active;
    }
  }
}

.cancel {
  color: @text-grey;
  border: 1px solid #E0E0E0;

  &:focus-visible,
  &:hover {
    color: @red;
    border-color: @red;
  }
  &:active {
    color: @red-active;
    border-color: @red-active;
  }
}

</style>
