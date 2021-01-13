<template>
	<button class="btn">
		<slot></slot>
	</button>
</template>

<script>
export default {
	name: 'VButton',
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

.btn {
  height: 50px;
  width: 100%;
}

.big {
	height: 70px;
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