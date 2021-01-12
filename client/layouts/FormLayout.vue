<template>
  <div id="container">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'FormLayout.vue',
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

#container {
  position: relative;
}

form {
  width: 516px;
}

h1 {
  text-align: center;
}

#form-inner {
  margin-top: 48px;

  & p {
    margin-top: 8px;
  }
}

input {
  font-size: @fz-large;
  line-height: 160%;
}

button {
  height: 70px;
  width: 100%;
  margin-top: 10px;

  color: @blue;
  border: 1px solid @blue;

  &:first-child {
    margin-top: 32px;
  }
  &.filled {
    background-color: @blue;
    border: none;
    color: @theme-color;
  }
}

p {
  margin-top: 18px;
}

// input {
//   height: 70px;
// }

</style>

