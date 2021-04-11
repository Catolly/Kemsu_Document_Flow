<template>
	<form @submit.prevent="checkForm" id="form">
    <h1 id="form-header">Регистрация</h1>
    <div id="form-inner">
      <app-autocomplete
      v-model.trim="form.username"
      :options="relevantUsersOptions"
      autocomplete="off"
      id="username"
      class="username"
      type="text"
      placeholder="Ф.И.О."
      required />
      <app-input
      v-model.trim="form.email"
      id="email"
      class="email"
      type="email"
      placeholder="Email"
      required />
      <app-autocomplete
      v-model.trim="form.department"
      :options="departmentsOptions"
      autocomplete="off"
      id="department"
      class="department"
      type="text"
      placeholder="Отдел, в котором работаете"
      required />
      <app-input
      v-model.trim="form.password"
      id="password"
      type="password"
      placeholder="Пароль"
      required />
      <app-button
      id="signup"
      class="signup-btn blue big filled fluid">
        Зарегистрироваться
      </app-button>
      <NuxtLink
      to="/login"
      class="login-link">
        <app-button
        class="login-btn blue big fluid">
          Войти
        </app-button>
      </NuxtLink>
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
  data() {
    return {
      form: {
        username: '',
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
    }
  },
  computed: {
    relevantUsersOptions() {
      return this.relevantUsers.map(user => {
        return {
          id: user.id,
          value: user.fullName + ' - ' + user.group
        }
      })
    },
    departmentsOptions() {
      return this.departments.map(department => {
        return {
          id: department.id,
          value: department.fullName + ' - ' + department.group
        }
      })
    }
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
  }
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

#form {
  width: 516px;
}

#form-header {
  text-align: center;
}

#form-inner {
  margin-top: 48px;

  .username {
    width: 100%;
  }

  .forgot-password {
    margin-top: 8px;
  }

  .signup-btn {
    margin-top: 32px;
  }

  .login-btn {
    margin-top: 10px;
  }

  .login-link:after {
    display: none;
  }

  .signup-problem {
    margin-top: 16px;
  }
}

</style>
