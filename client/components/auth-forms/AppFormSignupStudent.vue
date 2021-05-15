<template>
	<form @submit.prevent="submit" class="form">

    <h1 class="header">Регистрация</h1>

    <div class="body">
      <div class="inputs">
        <app-autocomplete
          v-model="$v.fullnameAndGroup.$model"
          :options="unregisteredStudentsOptionList"
          placeholder="Ф.И.О."
          :errorMessages="[
            ... $v.fullnameAndGroup.$dirty
                && !$v.fullnameAndGroup.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.fullnameAndGroup.$dirty
                && $v.fullnameAndGroup.required
                && !$v.fullnameAndGroup.exist
                ? ['Такого студента или группы не существует']
                : [],
            ... fetchUnregisteredStudentsError
                ? ['Не удалось загрузить список пользователей']
                : [],
          ]"
          @input="reset($v.fullnameAndGroup)"
          @change="checkField($v.fullnameAndGroup)"
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
          :messages="[`Пароль должен содержать ${minPasswordLength} и более символов`]"
          :errorMessages="[
            ... $v.password.$dirty
                && !$v.password.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.password.$dirty
                && $v.password.required
                && !$v.password.minLength
                ? [`Пароль должен содержать ${minPasswordLength} и более символов`]
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
import { minPasswordLength } from "~/vuelidate/constants"

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
    fullnameAndGroup: '',

    fullname: '',
    group: '',
    email: '',
    password: '',
    divider: ' - ', // Разделяет fullname и group

    minPasswordLength: minPasswordLength,

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
    fullnameAndGroup: {
      required,
      exist: (value, vm) => !!vm.unregisteredStudentsOptionList.find(option => option.value === value)
    },
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(minPasswordLength),
    },
  }),

  computed: {
    relevantUsersOptionList() {
      return this.relevantUsers.map(user => ({
        id: user.id,
        value: user.fullName + ' - ' + user.group,
      }))
    }

  watch: {
    fullnameAndGroup() {
      this.fullname = this.fullnameAndGroup.split(this.divider)[0]
      this.group = this.fullnameAndGroup.split(this.divider)[1]
    },
  },

  methods: {
    reset($v) {
      if (!$v.required) return

      $v.$reset()
    },

    checkField($v) {
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

.signup-error {
  margin-top: 16px;
  margin-bottom: -16px;
  color: @red;
}
</style>
