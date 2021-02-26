<template>
	<div class="container">
		<h1 class="header">Личные данные</h1>
		<div class="personal-data">
			<v-input
			:value="lastName"
			placeholder="Фамилия"
			id="last-name" 
			class="v-input" />
			<v-input
			:value="firstName"
			placeholder="Имя"
			id="first-name" 
			class="v-input" />
			<v-input
			:value="patronymic"
			placeholder="Отчество"
			id="patronymic" 
			class="v-input" />
			<div 
			v-for="item in about"
			:key="item.title"
			class="about-field">
			<span class="field-title">{{item.title}}</span>
			<span class="field-body">{{item.body}}</span>
		</div>
	</div>
	<div class="footer">
		<NuxtLink to="/login" class="logout">
			Выйти из аккаунта
		</NuxtLink>
		<div class="btns-wrapper">
			<v-button class="btn btn-cancel red">
				Отмена
			</v-button>
			<v-button class="btn btn-submit blue filled">
				Отправить
			</v-button>
		</div>
	</div>
</div>
</template>

<script>
import VInput from '~/components/VInput'
import VButton from '~/components/VButton'

export default {
	name: 'ThePageSettings',
	components: {
		VInput,
		VButton
	},
	data() {
		return {
			lastName: 'Козырева',
			firstName: 'Татьяна',
			patronymic: 'Андреевна',
			about: [
				{
					title: 'Интитут, группа',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Дирекция института',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Отдел платных образовательных услуг',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Библиотека',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'ОКБ Бюро пропусков',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'ОКБ Бюро пропусков',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Военно-учетный стол',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Студенческий городок',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Центр мониторинга трудоустройства выпускников',
					body: 'Факультет 1, КГУ, группа 45'
				},
				{
					title: 'Студенческая бухгалтерия',
					body: 'Факультет 1, КГУ, группа 45'
				},
			]
		}
	}
}
</script>

<style scoped lang="less">

.container {
	padding-top: 48px;
	height: 100vh;
}

.personal-data {
	display: grid;
	grid-template-columns: repeat(2, 360px) 1fr;
	grid-template-rows: auto 1fr;
	grid-column-gap: 24px;
	grid-row-gap: 48px;

	.v-input {
		width: 360px;
	}

	.about-field {
		.flex(flex-start, normal, column);
	}

	.field-title {
		font-weight: @fw-normal;
		font-size: @fz-large;
	}

	.field-body {
		margin-top: 12px;
		font-weight: @fw-light;
		font-size: @fz-normal;
	}
}

.footer {
	position: absolute;
	bottom: 96px;
	right: 0;

	.flex(space-between, center);
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

	.btn:not(:last-child) {
		margin-right: 16px;
	}
}

</style>