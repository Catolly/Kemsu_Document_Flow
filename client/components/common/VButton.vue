<template>
	<button 
	tabindex="0"
	class="v-button">
		<slot />
	</button>
</template>

<script>
export default {
	name: 'VButton',
}
</script>

<style lang="less" scoped>

.v-button {
  padding: 16px 48px;
  
  font-size: @fz-normal;
  font-weight: @fw-medium;

  border-radius: 10px;
	border: 1px solid #000;
	background: transparent;

	&:hover {
		background: rgba(0, 0, 0, .025);
	}
}

.big {
	padding-top: 19px;
	padding-bottom: 19px;

	font-size: @fz-large;
}

.fluid {
	width: 100%;
}

.red,
.green,
.blue {
	&:hover {
		cursor: pointer;
	}
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
		background: @green-hover;
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