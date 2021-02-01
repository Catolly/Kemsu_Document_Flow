<template>
	<button class="v-button">
		<slot />
	</button>
</template>

<script>
export default {
	name: 'VButton',
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

.v-button {
  padding: 16px 48px;
  
  font-size: @fz-normal;
  font-weight: @fw-medium;

  background-color: transparent;
  
  border-radius: 10px;
  border: none;
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
	&:hover {
		color: @red-hover;
		border-color: @red-hover;
	}
	&.filled {
		background-color: @red;
	}
	&.filled:hover {
		background-color: @red-hover;
	}
}
.green {
	color: @green;
	border: 1px solid @green;
	&:hover {
		color: @green-hover;
		border-color: @green-hover;
	}
	&.filled {
		background-color: @green;
	}
	&.filled:hover {
		background-color: @green-hover;
	}
}
.blue {
	color: @blue;
	border: 1px solid @blue;
	&:hover {
		color: @blue-hover;
		border-color: @blue-hover;
	}
	&.filled {
		background-color: @blue;
	}
	&.filled:hover {
		background-color: @blue-hover;
	}
}

</style>