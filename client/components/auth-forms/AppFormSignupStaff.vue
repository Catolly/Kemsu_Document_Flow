<template>
	<form @submit.prevent="checkForm" class="form">

    <h1 class="header">Регистрация</h1>

    <div class="body">
      <div class="inputs">
        <app-autocomplete
          v-model.trim="form.fullName"
          :options="relevantUsersOptions"
          placeholder="Ф.И.О."
          required
        />

        <app-input
          v-model.trim="form.email"
          type="email"
          placeholder="Email"
          required
        />

        <app-autocomplete
          v-model.trim="form.department"
          :options="departmentsOptions"
          placeholder="Отдел, в котором работаете"
          required
        />

        <app-input
          v-model.trim="form.password"
          type="password"
          placeholder="Пароль"
          required
        />
      </div>

      <div class="btns">
        <app-button
          class="signup-btn blue big filled fluid"
        >
          Зарегистрироваться
        </app-button>

        <app-button
          class="to-login-btn blue big fluid"
          @click="toLogin"
        >
          Войти
        </app-button>
      </div>

      <p class="signup-problem">
        Кто-то зарегистрировался под вашим именем? Обратитесь к <NuxtLink to="#">администрации</NuxtLink>
      </p>
    </div>

  </form>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppAutocomplete from '~/components/common/AppAutocomplete'

export default {
  name: 'FormSingupStaff',

  components: {
    AppButton,
    AppInput,
    AppAutocomplete,
  },

  data:() => ({
      form: {
        fullName: '',
        email: '',
        department: '',
        password: '',
      },

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

      departments: [
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

  computed: {
    relevantUsersOptions() {
      return this.relevantUsers.map(user => ({
        id: user.id,
        value: user.fullName + ' - ' + user.group,
      }))
    },

    departmentsOptions() {
      return this.departments.map(department => ({
          id: department.id,
          value: department.fullName + ' - ' + department.group,
      }))
    },
  },

  methods: {
    checkForm() {
      // Проверка данных формы
      // ...
      this.signup()
    },

    async signup() {
      // Отправка данных на сервер
      // ...

      this.$router.push('/')
    },

    toLogin() {
      this.$router.push('/login')
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
