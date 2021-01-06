<template> 
	<div id="logo">
		<img src="~/assets/logo.svg" alt="КемГУ">
	</div>
</template>

<script>
export default {
  name: 'logo'
}
</script>

<style lang="less" scoped>

#logo {
	height: 66px;
  width: 42px;

  position: absolute;
  top: 25px;
  left: 60px;

  &.big {
  	height: 86px;
  	width: 54px;
  }
}

</style>
