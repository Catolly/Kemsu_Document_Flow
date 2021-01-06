<template>
  <div id="container">
    <div id="login-wrapper">
      <form-layout>
        <form @submit="checkForm()" id="login-form"> 
          <h1>Вход</h1>
          <div id="form-inner">
            <v-input
            v-model.trim="form.username"
            :class="$v.form.username.$error ? 'is-invalid' : ''"
            id="username"
            type="text"
            placeholder="Ф.И.О."
            required></v-input>
            <v-input
            v-model.trim="form.password"
            :class="$v.form.password.$error ? 'is-invalid' : ''"
            id="password"
            type="password"
            placeholder="Пароль"
            required></v-input>
            <p>
              <NuxtLink to="#">Не помню пароль</NuxtLink>
            </p>
            <div class="buttons-wrapper">
              <button
              id="login"
              class="filled">
                Войти
              </button>
              <button
              id="signup">
                Зарегистрироваться
              </button>
            </div>
          </div>
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
  name: 'LoginLayout.vue',
  components: {
    VInput,
    FormLayout
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      }
    }
  },
  validations: {
    form: {
      username: { required },
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

#login-wrapper {
  height: 100vh;
  .flex(center, center);
}

input {
  height: 70px;
}

</style>

