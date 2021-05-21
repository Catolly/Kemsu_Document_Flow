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
            ... $v.fullname.$dirty
                && $v.fullname.required
                && !$v.fullname.twoOrThreeWords
                ? ['Поле должно содержать хотя бы имя и фамилию']
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
                ? ['Введите email']
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
        <a @click="dialog = true">администрации</a>
      </p>
    </div>

    <app-dialog :isOpen="dialog" @close="dialog = false">
      <p>
        При возникновении проблем, свяжитесь с администрацией:
        <b>{{adminEmail}}</b>
      </p>
    </app-dialog>
  </form>
</template>

<script>
import { adminEmail } from "~/services/config"
import { errorCode } from "~/services/ApiService"

import { mapGetters } from "vuex"
import { SIGNUP_STAFF, FETCH_ALL_DEPARTMENTS } from "~/store/actions.type"

import { required, minLength, email, helpers } from "vuelidate/lib/validators"
import { twoOrThreeWordsReg } from '~/vuelidate/validators'
import { minPasswordLength } from "~/vuelidate/constants"

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppSelect from '~/components/common/AppSelect'
import AppDialog from '~/components/common/AppDialog'

const isTwoOrThreeWords = helpers.regex('isTwoOrThreeWords',
  twoOrThreeWordsReg) // От 2 до 3 слов

const twoOrThreeWords = (value) => isTwoOrThreeWords(value)

export default {
  name: 'FormSingupStaff',

  components: {
    AppButton,
    AppInput,
    AppSelect,
    AppDialog,
  },

  validations:() => ({
    fullname: {
      required,
      twoOrThreeWords,
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

    dialog: false,
    adminEmail: adminEmail,
  }),

  computed: {
    ...mapGetters(['allDepartments']),
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

    signup() {
      this.error = ''
      this.conflictError = ''
      this.signupSuccess = false
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
