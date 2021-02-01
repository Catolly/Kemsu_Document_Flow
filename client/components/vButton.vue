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
	&.filled {
		border: none;
		color: #fff;
	}
}

.red {
	color: @red;
	border: 1px solid @red;
	&.filled {
		background-color: @red;
	}
}
.green {
	color: @green;
	border: 1px solid @green;
	&.filled {
		background-color: @green;
	}
}
.blue {
	color: @blue;
	border: 1px solid @blue;
	&.filled {
		background-color: @blue;
	}
}

</style>