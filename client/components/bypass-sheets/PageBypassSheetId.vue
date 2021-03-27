<template>
	<div class="container">
		<h1 class="header">
			Обходной лист - {{title}}
		</h1>
	</div>
</template>

<script>

export default {
	name: 'PageBypassSheet',
	data() {
		return {
			id: 0,
			title: 'Скидка на столовую',
			points: [
				{
					id: 0,
					title: 'Библиотека',
					status: 'signed',
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
					status: 'submitted',
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
		}
	},
}
</script>

<style lang="less" scoped>

.header {
	margin-top: 48px;
}


</style>