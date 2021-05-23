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

      <p v-if="error" class="signup-error">
        Не удалось зарегистрироваться
        <br>
        Повторите попытку позже
      </p>

      <p v-if="conflictError" class="signup-error">
        Пользователь с таким Email уже зарегистрирован
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
import { SIGNUP_STUDENT, FETCH_UNREGISTERED_STUDENTS } from "~/store/actions.type"

import { required, minLength, email } from "vuelidate/lib/validators"
import { optionExist } from "~/vuelidate/validators"
import { minPasswordLength } from "~/vuelidate/constants"

import _ from "lodash"
import { throttleDelay } from "~/services/config"

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppAutocomplete from '~/components/common/AppAutocomplete'
import AppDialog from '~/components/common/AppDialog'

export default {
  name: 'FormSingupStudent',

  components: {
    AppButton,
    AppInput,
    AppAutocomplete,
    AppDialog,
  },

  data:() => ({
    fullnameAndGroup: '',

    fullname: '',
    group: '',
    email: '',
    password: '',
    divider: ' - ', // Разделяет fullname и group

    minPasswordLength: minPasswordLength,

    error: '',
    conflictError: '',
    fetchUnregisteredStudentsError: '',

    dialog: false,
    adminEmail: adminEmail,
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
    ...mapGetters(['unregisteredStudents']),

    unregisteredStudentsOptionList() {
      console.log(this.unregisteredStudents)
      if (this.unregisteredStudents)
        return this.unregisteredStudents.map(user => ({
          id: user.id,
          value: user.fullname + this.divider + user.group,
        }))
    },
  },

  watch: {
    fullnameAndGroup() {
      this.fullname = this.fullnameAndGroup.split(this.divider)[0]
      this.group = this.fullnameAndGroup.split(this.divider)[1]

      this.fetchUnregisteredStudents()
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

    signup() {
      this.error = ''
      this.conflictError = ''
      this.$store
        .dispatch(SIGNUP_STUDENT, {
          'fullname': this.fullname,
          'group': this.group,
          'email': this.email,
          'password': this.password,
        })
        .then(() => this.$router.push('/'))
        .catch(error => {
          console.error(error)
          if (errorCode(error === '409'))
            this.conflictError = error
          else this.error = error
        })
    },

    fetchUnregisteredStudents: _.throttle(async function() {
      this.$store
        .dispatch(FETCH_UNREGISTERED_STUDENTS, {
          search: this.fullname,
          limit: 4,
        })
        .then(data => {
          console.log(data)
        })
        .catch(error => {
          console.error(error)
          this.fetchUnregisteredStudentsError = error
        })
    }, 500)
  },

  beforeMount() {
    this.fetchUnregisteredStudents()
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

.signup-error {
  margin-top: 16px;
  margin-bottom: -16px;
  color: @red;
}
</style>
