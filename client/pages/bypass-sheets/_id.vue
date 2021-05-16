<template>
	<roleStudent class="container">
		<h1 class="header">
			Обходной лист - {{title}}
		</h1>

		<app-list	class="point-list">
			<app-bypass-sheet-point
				v-for="(point, index) in points"
				:key="index"
        :point="point"
				class="point"
      />
		</app-list>
	</roleStudent>
</template>

<script>
import { mapGetters } from "vuex"
import { LOGOUT, FETCH_BYPASS_SHEETS } from "~/store/actions.type"

import roleStudent from '~/components/roles/roleStudent'

import AppList from '~/components/common/AppList'
import AppBypassSheetPoint from '~/components/bypass-sheets/AppBypassSheetPoint'

export default {
	components: {
    roleStudent,
		AppList,
    AppBypassSheetPoint,
	},

	data:() => ({
		id: 0,
		title: 'Скидка на столовую',

		points: [
			{
				id: 0,
				title: 'Библиотека',
				status: 'signed',
				requiredDocuments: [
					{
						index: 0,
						title: 'Фото/скан паспорта',
						src: require('~/assets/img/document_example.png')
					},
					{
						id: 1,
						title: 'Заполненный документ',
						src: require('~/assets/img/document_example.png')
					},
				],
				worker: 'И.В.Иванов',
				phone: '7 920 392 57 51',
			},
			{
				id: 1,
				title: 'Общежитие',
				status: 'rejected',
				reason: 'Нет книги Н.В.Гоголя и части документов',
				requiredDocuments: [
					{
						id: 0,
						title: 'Фото/скан паспорта',
						src: require('~/assets/img/document_example.png')
					},
					{
						id: 1,
						title: 'Заполненный документ',
						src: require('~/assets/img/document_example.png')
					},
				],
				worker: 'И.В.Иванов',
				phone: '7 920 392 57 51',
			},
			{
				id: 2,
				title: 'Библиотека',
				status: 'reviewing',
				requiredDocuments: [
					{
						id: 0,
						title: 'Фото/скан паспорта',
						src: require('~/assets/img/document_example.png')
					},
					{
						id: 1,
						title: 'Заполненный документ',
						src: require('~/assets/img/document_example.png')
					},
				],
				worker: 'И.В.Иванов',
				phone: '7 920 392 57 51',
			},
			{
				id: 3,
				title: 'Общежитие',
				status: 'not sent',
				requiredDocuments: [
					{
						id: 0,
						title: 'Фото/скан паспорта',
						src: require('~/assets/img/document_example.png')
					},
					{
						id: 1,
						title: 'Заполненный документ',
						src: require('~/assets/img/document_example.png')
					},
				],
				worker: 'И.В.Иванов',
				phone: '7 920 392 57 51',
			},
		]
	}),

  computed: {
    // ...mapGetters(['currentUser']),
  },

  created() { // Достаем обходные листы либо через fetch, либо через currentUser.bypassSheets
    // this.$store
    //   .dispatch(FETCH_BYPASS_SHEETS, {
    //     departments: this.departments,
    //     institute: 'ИФН' //currentUser.institute
    //   })
  },
}
</script>

<style lang="less" scoped>
.container,
.point-list {
	margin-top: 48px;
}
</style>
