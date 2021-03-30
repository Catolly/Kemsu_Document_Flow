<template>
  <div class="container">
    <div class="content">
      <form-signup-staff v-if="$route.query.staff"/>
      <form-signup-student v-else/>
    </div>
  </div>
</template>

<script>
import VButton from '~/components/common/VButton'
import FormSignupStaff from '~/components/common/FormSignupStaff'
import FormSignupStudent from '~/components/common/FormSignupStudent'

export default {
	layout: 'empty',
	name: 'Signup',
  components: {
    VButton,
    FormSignupStaff,
    FormSignupStudent,
  }
}
</script>

<style lang="less" scoped>

.container {
  height: 100vh;
  .flex(center, center, column);
}

.content {
  width: 516px;
}

</style>

