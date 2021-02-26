<template> 
	<div class="logo">
		<img class="logo-img" :src="require('~/assets/logo.svg')" alt="КемГУ">
	</div>
</template>

<script>
export default {
  name: 'Logo'
}
</script>

<style lang="less" scoped>

.logo {
	height: 66px;
  width: 42px;

  position: fixed;
  top: 25px;
  left: 60px;

  &.big {
  	height: 86px;
  	width: 54px;
  }
}

.logo-img {
  height: 100%;
  width: 100%;
}

</style>
