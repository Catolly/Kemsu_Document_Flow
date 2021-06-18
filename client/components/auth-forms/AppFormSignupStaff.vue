<template>
	<form @submit.prevent="submit" class="form">

    <h1 class="header">Регистрация</h1>

    <div class="body">
      <div class="inputs">
        <app-input
          v-model="$v.fullname.$model"
          placeholder="Ф.И.О."
          :errorMessages="[
            ... $v.fullname.$dirty
                && !$v.fullname.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.fullname.required
                && !$v.fullname.cyrillic
                ? ['Поле должно содержать только символы кириллицы']
                : [],
            ... $v.fullname.$dirty
                && $v.fullname.required
                && !$v.fullname.twoOrThreeWords
                ? ['Поле должно содержать фамилию, имя и (необязательно) отчество']
                : [],
          ]"
          @input="reset($v.fullname)"
          @change="checkField($v.fullname)"
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
                ? ['Поле должно быть заполнено по email-маске']
                : [],
          ]"
          @input="reset($v.email)"
          @change="checkField($v.email)"
        />

        <app-select
          v-model="$v.department.$model"
          :options="allDepartments.map(department => department.title)"
          placeholder="Отдел, в котором работаете"
          :errorMessages="[
            ... $v.department.$dirty
                && !$v.department.required
                ? ['Поле должно быть заполнено']
                : [],
          ]"
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

      <p v-if="error" class="signup-error">
        Не удалось зарегистрироваться
        <br>
        Повторите попытку позже
      </p>

      <p v-if="conflictError" class="signup-error">
        Пользователь с таким Email уже зарегистрирован
      </p>

      <p v-if="signupSuccess" class="signup-success">
        Заявка на регистрацию успешно отправлена!
        <br>
        Аккаунт станет доступен после рассмотрения заявки
      </p>

      <div class="btns">
        <app-button
          class="signup-btn blue big filled fluid"
          :disabled="$v.$invalid || signupSuccess"
          :loading="submitLoading"
        >
          Зарегистрироваться
        </app-button>

        <nuxt-link to="/login" tabindex="-1" class="clear">
          <app-button class="to-login-btn blue big fluid">
            Войти
          </app-button>
        </nuxt-link>
      </div>

      <p class="signup-problem">
        Возникли проблемы?
        <a class="clear" target="_blank" :href="telegramHelpUrl">
          Напишите нам
        </a>
      </p>
    </div>
  </form>
</template>

<script>
import { telegramHelpUrl } from '~/services/config'
import { errorCode } from "~/services/ApiService"

import { mapGetters } from "vuex"
import { SIGNUP_STAFF, FETCH_ALL_DEPARTMENTS } from "~/store/actions.type"

import { required, minLength, email, helpers } from "vuelidate/lib/validators"
import { minPasswordLength } from "~/vuelidate/constants"

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppSelect from '~/components/common/AppSelect'

export default {
  name: 'FormSingupStaff',

  components: {
    AppButton,
    AppInput,
    AppSelect,
  },

  validations:() => ({
    fullname: {
      required,
      twoOrThreeWords: (value, vm) => !!value.match(
        /^[а-яА-ЯЁёa-zA-Z]+\s[а-яА-ЯЁёa-zA-Z]+\s?[а-яА-ЯЁёa-zA-Z]*$/
      ),
      cyrillic: (value, vm) => !!value.match(/^[а-яА-ЯЁё]+/),
    },
    email: {
      required,
      email,
    },
    department: {
      required,
    },
    password: {
      required,
      minLength: minLength(minPasswordLength),
    },
  }),

  data:() => ({
    fullname: '',
    email: '',
    department: '',
    password: '',

    minPasswordLength: minPasswordLength,

    error: '',
    conflictError: '',
    signupSuccess: false,
    submitLoading: false,
  }),

  computed: {
    ...mapGetters(['allDepartments']),

    telegramHelpUrl() {
      return telegramHelpUrl
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

      if (this.$v.$invalid || this.signupSuccess || this.submitLoading) return

      this.signup()
    },

    signup() {
      this.error = ''
      this.conflictError = ''
      this.signupSuccess = false
      this.submitLoading = true
      this.$store
        .dispatch(SIGNUP_STAFF, {
          'fullname': this.fullname,
          'email': this.email,
          'department': this.department,
          'password': this.password,
        })
        .then(() => this.signupSuccess = true)
        .catch(error => {
          console.error(error)
          if (errorCode(error === '409'))
            this.conflictError = error
          else this.error = error
        })
        .finally(() => this.submitLoading = false)
    },

    fetchAllDepartments() {
      this.$store.dispatch(FETCH_ALL_DEPARTMENTS, this.allDepartments)
    },
  },

  mounted() {
    this.fetchAllDepartments()
  },
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

.signup-success,
.signup-error {
  margin-top: 16px;
  margin-bottom: -16px;
}

.signup-error {
  color: @red;
}

.signup-success {
  color: @green;
}
</style>
