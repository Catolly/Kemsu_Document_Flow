<template>
	<form @submit.prevent="submit" class="form">

    <h1 class="header">Регистрация</h1>

    <div class="body">
      <div class="inputs">
        <app-input
          v-model="$v.fullName.$model"
          placeholder="Ф.И.О."
          :errorMessages="[
            ... $v.fullName.$dirty
                && !$v.fullName.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.fullName.$dirty
                && $v.fullName.required
                && !$v.fullName.twoOrThreeWords
                ? ['Поле должно содержать хотя бы имя и фамилию']
                : [],
          ]"
          @input="reset($v.fullName)"
          @change="checkField($v.fullName)"
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
          :options="departmentList"
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
import { required, minLength, email, helpers } from "vuelidate/lib/validators"
import { twoOrThreeWordsReg } from '~/vuelidate/validators'

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppSelect from '~/components/common/AppSelect'

const isTwoOrThreeWords = helpers.regex('isTwoOrThreeWords',
  twoOrThreeWordsReg) // От 2 до 3 слов

const twoOrThreeWords = (value) => isTwoOrThreeWords(value)

export default {
  name: 'FormSingupStaff',

  components: {
    AppButton,
    AppInput,
    AppSelect,
  },

  validations:() => ({
    fullName: {
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
      minLength: minLength(7),
    },
  }),

  data:() => ({
    fullName: '',
    email: '',
    department: '',
    password: '',

    departmentList: [
        'Институт биологии, экологии и природных ресурсов',
        'Институт инженерных технологий',
        'Институт истории и международных отношений',
        'Институт образования',
        'Институт филологии, иностранных языков и медиакоммуникаций',
        'Технологический институт пищевой промышленности',
        'Институт цифры',
        'Институт экономики и управления',
        'Социально-психологический институт',
        'Факультет физкультуры и спорта',
        'Институт фундаментальных наук',
        'Юридический институт',
        'Среднетехнический факультет',
    ],
  }),

  methods: {
    reset($v) {
      if (!$v.required) return

      $v.$reset()
    },

    checkField($v) {
      if (!$v.required) return

      $v.$touch()
    },

    submit() {
      // Проверка данных формы
      // ...
      this.signup()
    },

    async signup() {
      // Отправка данных на сервер
      // ...

      this.$router.push('/')
    },
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

</style>
