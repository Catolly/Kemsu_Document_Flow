<template>
  <div id="container">
    <div id="signup-wrapper">
      <form-layout>
        <form @submit="checkForm()" id="signup-form"> 
          <h1>Регистрация</h1>
          <div id="form-inner">
            <v-input
            v-model.trim="form.username"
            :class="$v.form.username.$error ? 'is-invalid' : ''"
            id="username"
            type="text"
            placeholder="Ф.И.О."
            required></v-input>
            <v-input
            v-model.trim="form.email"
            :class="$v.form.email.$error ? 'is-invalid' : ''"
            id="email"
            type="email"
            placeholder="Email"
            required></v-input>
            <v-input
            v-model.trim="form.password"
            :class="$v.form.password.$error ? 'is-invalid' : ''"
            id="password"
            type="password"
            placeholder="Пароль"
            required></v-input>
            <div class="buttons-wrapper">
              <button
              class="filled"
              id="signup">
                Зарегистрироваться
              </button>
              <button
              id="login">
                Войти
              </button>
            </div>
          </div>
          <p>Кто-то зарегистрировался под вашим именем? Обратитесь к <NuxtLink to="#">администрации</NuxtLink></p>
        </form>
      </form-layout>
    </div>
  </div>
</template>

<script>
import VInput from '~/components/VInput'
import FormLayout from '~/layouts/FormLayout'
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
  name: 'SignupLayout.vue',
  components: {
    VInput,
    FormLayout
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
      }
    }
  },
  validations: {
    form: {
      username: { required, minLength: minLength(5) },
      email: { required, email },
      password: { required },
    },
  },
  methods: {
    checkForm() {
      this.$v.form.$touch()
      if (!this.$v.form.$error) {
        this.send()
      }
    },
    send() {
      /*Sending form data to server*/
    }
  }
}
</script>

<style lang="less">
@import '~/styles/index.less';

#container {
  position: relative;
}

#signup-wrapper {
  height: 100vh;
  .flex(center, center);
}

input {
  height: 70px;
}

</style>

