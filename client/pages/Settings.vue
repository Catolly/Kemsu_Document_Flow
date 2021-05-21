<template>
	<form
    @submit.prevent="submit"
    class="settings"
  >
		<h1 class="header">Личные данные</h1>
    <span
      v-if="updated && !updateError"
      class="success-message"
    >
      Данные успешно обновлены!
    </span>
    <span
      v-if="updateError"
      class="error-message"
    >
      Не удалось обновить данные
    </span>


    <div class="settings-body">
  		<div class="personal-data">

  			<app-input
    			v-model="lastname"
    			placeholder="Фамилия"
    			class="input"
          :errorMessages="[
          ... $v.lastname.$dirty
              && !$v.lastname.required
              ? ['Поле должно быть заполнено']
              : [],
          ... $v.lastname.required
              && !lastname.match(/^[а-яА-ЯЁё]+$/)
              ? ['Поле должно содержать только символы кириллицы']
              : [],
          ]"
          @input="reset($v.lastname)"
          @change="checkField($v.lastname)"
        />

  			<app-input
    			v-model="firstname"
    			placeholder="Имя"
    			class="input"
          :errorMessages="[
          ... $v.firstname.$dirty
              && !$v.firstname.required
              ? ['Поле должно быть заполнено']
              : [],
          ... $v.firstname.required
              && !firstname.match(/^[а-яА-ЯЁё]+$/)
              ? ['Поле должно содержать только символы кириллицы']
              : [],
          ]"
          @input="reset($v.firstname)"
          @change="checkField($v.firstname)"
        />

  			<app-input
    			v-model="middlename"
    			placeholder="Отчество"
    			class="input"
          :errorMessages="[
          ... $v.middlename.$dirty
              && !$v.middlename.required
              ? ['Поле должно быть заполнено']
              : [],
          ... $v.middlename.required
              && !middlename.match(/^[а-яА-ЯЁё]+$/)
              ? ['Поле должно содержать только символы кириллицы']
              : [],
          ]"
          @input="reset($v.middlename)"
          @change="checkField($v.middlename)"
        />

        <span
          v-if="loadError"
          class="error-message"
        >
          Не удалось загрузить список отделов
        </span>

  			<div
    			v-for="department in departments"
    			:key="department.title"
    			class="department"
        >
  				<span class="title">{{department.title}}</span>
  				<span class="address">{{department.address}}</span>
  			</div>
  		</div>

  		<div class="footer">
  			<span @click="logout">
  				<a
            class="logout"
            @click="logout"
          >
  					Выйти из аккаунта
  				</a>

  			</span>
  			<div class="btns-wrapper">
          <NuxtLink
            class="clear"
            to="/"
          >
    				<app-button class="btn btn-cancel red">
    					Отмена
    				</app-button>
          </NuxtLink>

  				<app-button
            :disabled="
              $v.$invalid ||
              fullname(
                lastname,
                firstname,
                middlename
              ) === currentUser.fullname"
            class="btn btn-submit blue filled"
          >
  					Сохранить
  				</app-button>
  			</div>
  		</div>
    </div>
  </form>
</template>

<script>
import { mapGetters } from "vuex"
import { UPDATE_USER, LOGOUT, FETCH_DEPARTMENTS } from "~/store/actions.type"

import { required } from "vuelidate/lib/validators"

import AppInput from '~/components/common/AppInput'
import AppButton from '~/components/common/AppButton'

export default {
	name: 'settings',

  middleware: 'authenticated',

	components: {
		AppInput,
		AppButton
	},

	data:() => ({
    updated: false,
    updateError: false,
    loadError: false,

    lastname: '',
    firstname: '',
    middlename: '',
	}),

  validations:() => ({
    lastname: {
      required,
    },
    firstname: {
      required,
    },
    middlename: {
      required,
    },
  }),

  computed: {
    ...mapGetters(['departments']),
    // ...mapGetters(['departments', 'currentUser']),

    // удалить позже
    currentUser() {
      return {
        fullname: 'Козырева Татьяна Андреевна',
      }
    },
    //
  },

	methods: {
    fullname(lastname, firstname, middlename) {
      return lastname + ' ' + firstname + (middlename ? ' ' + middlename : '')
    },

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

      this.updateUser()
    },

    updateUser() {
      this.$store
        .dispatch(UPDATE_USER, {
          fullname: [
            this.lastname,
            this.firstname,
            this.middlename
          ].join(' ')
        })
        .then(() => this.updated = true)
        .catch(error => this.updateError = error)
    },

		logout() {
      this.$store
        .dispatch(LOGOUT)
        .then(() => this.$router.push('/login'))
		},
	},

  created() {
    this.lastname = 'Козырева' // удалить позже
    this.firstname = 'Татьяна' // удалить позже
    this.middlename = 'Андреевна' // удалить позже

    // this.lastname = return this.currentUser.fullname.split(' ')[0]
    // this.firstname = return this.currentUser.fullname.split(' ')[1]
    // this.middlename = return this.currentUser.fullname.split(' ')[2] || ''

    this.$store
      .dispatch(FETCH_DEPARTMENTS, {
        departments: this.departments,
        institute: 'ИФН' //currentUser.institute
      })
      .catch(error => this.loadError = error)
  },
}
</script>

<style scoped lang="less">
.settings {
  padding-top: 48px;
  height: 100vh;
}

.settings-body {
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.personal-data {
	display: grid;
	grid-template-columns: repeat(2, minmax(200px, 360px)) minmax(360px, 1fr);
	grid-template-rows: auto 1fr;
	grid-column-gap: 24px;
	grid-row-gap: 48px;
  grid-auto-flow: dense;

	margin-top: 48px;

	.input {
		max-width: 360px;
	}

	.department {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;

    .title {
      font-weight: @fw-normal;
      font-size: @fz-large;
    }

    .address {
      margin-top: 12px;
      font-weight: @fw-light;
      font-size: @fz-normal;
    }
	}
}

.footer {
	margin-top: 60px;
  padding-bottom: 60px;

  display: flex;
  justify-content: space-between;
  align-items: center;

	width: 100%;

	.logout {
		color: @red;
		&:after {
			border-color: @red;
		}

		&:hover {
			color: @red-hover;
			&:after {
				border-color: @red-hover;
			}
		}
	}

	.btns-wrapper {
    display: flex;
    gap: 16px;
  }
}
</style>
