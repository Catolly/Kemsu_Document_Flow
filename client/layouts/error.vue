<template>
  <div class="container">
    <h1
      v-if="error.statusCode == 404"
      class="error-message"
    >
      Страница не найдена
    </h1>
    <h1 v-else class="error-message">Произошла ошибка</h1>
  </div>
</template>

<script>
import IconLogo from '~/components/icons/IconLogo'

export default {
  layout: 'error',
  props: ['error'],

  components: {
    IconLogo,
  },
}
</script>

<style lang="less" scoped>
.container {
  padding-top: 48px;
}

.error-message {
  color: @red;
}
</style>
