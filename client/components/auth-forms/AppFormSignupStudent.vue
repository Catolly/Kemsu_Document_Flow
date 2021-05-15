<template>
	<form @submit.prevent="submit" class="form">

    <h1 class="header">Регистрация</h1>

    <div class="body">
      <div class="inputs">
        <app-autocomplete
          v-model="$v.fullNameAndGroup.$model"
          :options="relevantUsersOptionList"
          placeholder="Ф.И.О."
          :errorMessages="[
            ... $v.fullNameAndGroup.$dirty
                && !$v.fullNameAndGroup.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.fullNameAndGroup.$dirty
                && $v.fullNameAndGroup.required
                && !$v.fullNameAndGroup.exist
                ? ['Такого студента или группы не существует']
                : [],
          ]"
          @input="reset($v.fullNameAndGroup)"
          @change="checkField($v.fullNameAndGroup)"
        />

        <app-input
          v-model.trim="$v.email.$model"
          placeholder="Email"
          :errorMessages="[
            ... $v.email.$dirty
                && !$v.email.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.email.$dirty
                && $v.email.required
                && !$v.email.email
                ? ['Введите email']
                : [],
          ]"
          @input="reset($v.email)"
          @change="checkField($v.email)"
        />

        <app-input
          v-model="$v.password.$model"
          type="password"
          placeholder="Пароль"
          :messages="['Пароль должен содержать 7 и более символов']"
          :errorMessages="[
            ... $v.password.$dirty
                && !$v.password.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.password.$dirty
                && $v.password.required
                && !$v.password.minLength
                ? ['Пароль должен содержать 7 и более символов']
                : [],
          ]"
          @input="reset($v.password)"
          @change="checkField($v.password)"
        />
      </div>

      <div class="btns">
        <app-button
          class="signup-btn blue big filled fluid"
          :disabled="$v.$invalid"
        >
          Зарегистрироваться
        </app-button>

        <NuxtLink to="/login" tabindex="-1" class="clear">
          <app-button class="to-login-btn blue big fluid">
            Войти
          </app-button>
        </NuxtLink>
      </div>

      <p class="signup-problem">
        Кто-то зарегистрировался под вашим именем? Обратитесь к
        <NuxtLink to="#">администрации</NuxtLink>
      </p>
    </div>

  </form>
</template>

<script>
import { required, minLength, email } from "vuelidate/lib/validators"
import { optionExist } from "~/vuelidate/validators"

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppAutocomplete from '~/components/common/AppAutocomplete'

export default {
  name: 'FormSingupStudent',

  components: {
    AppButton,
    AppInput,
    AppAutocomplete,
  },

  data:() => ({
    fullNameAndGroup: '',
    email: '',
    password: '',

    relevantUsers: [
      {
        id: 34,
        fullName: 'Козырева Татьяна Андреевна',
        group: "M-174",
      },
      {
        id: 64,
        fullName: 'Козырева Татьяна Андреевна',
        group: "M-185",
      },
      {
        id: 18,
        fullName: 'Сергиенко Анатолий Николаевич',
        group: "M-174",
      },
      {
        id: 93,
        fullName: 'Оооооооооооооооооооочень длинное имя',
        group: "M-174",
      },
    ],
  }),

  validations:() => ({
    fullNameAndGroup: {
      required,
      exist: optionExist,
    },
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(7),
    },
  }),

  computed: {
    relevantUsersOptionList() {
      return this.relevantUsers.map(user => ({
        id: user.id,
        value: user.fullName + ' - ' + user.group,
      }))
    }
  },

  methods: {
    reset($v) {
      if (!$v.required) return

      $v.$reset()
    },

    checkField($v) {
      if (!$v.required) return

      $v.$model = $v.$model.trim()

      $v.$touch()
    },

    submit() {
      this.$v.$touch()

      if (this.$v.$invalid) return

      this.signup()
    },

    async signup() {
      // Отправка данных на сервер
      // ...

      this.$router.push('/')
    },
  }
}
</script>

<style lang="less" scoped>

.inputs,
.btns {
  display: grid;
}

.form {
  .header {
    text-align: center;
  }

  .body {
    margin-top: 48px;

    .inputs {
      grid-row-gap: 16px;
    }

    .btns {
      margin-top: 32px;

      grid-row-gap: 8px;
    }

    .signup-problem {
      margin-top: 16px;
    }
  }
}
</style>
