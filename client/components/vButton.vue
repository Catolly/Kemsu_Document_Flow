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
  padding: 16px 48px;
  
  font-size: @fz-large;
  font-weight: @fw-medium;

  background-color: transparent;
  
  border-radius: 10px;
  border: none;
}

.big {
	padding-top: 19px;
	padding-bottom: 19px;
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