<template>
	<div class="container">
		<form id="form">
			<h1 class="header">Обходной лист</h1>
			<app-select
			placeholder="Причина"
			:options="reasonOptions"
			id="reason"
			class="reason"
			required />
			<app-document-upload
			:documentExampleSrc="documentExampleSrc"
			:title="'Необходимые документы'	"
			class="app-document-upload" />
			<div class="btns-wrapper">
				<app-button class="btn btn-cancel red">
					Отмена
				</app-button>
				<app-button class="btn btn-submit blue filled">
					Отправить
				</app-button>
			</div>
		</form>
	</div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppSelect from '~/components/common/AppSelect'
import AppDocumentUpload from '~/components/bypass-sheets/AppDocumentUpload'

export default {
	name: 'Create',
	components: {
		AppButton,
		AppSelect,
		AppDocumentUpload,
	},
	methods: {
	},
	data() {
		return {
			reasonOptions: [
				{
					id: 0,
					value: 'Скидка на столовую',
				},
				{
					id: 1,
					value: 'Отчисление',
				},
			],
			documentExampleSrc: require('~/assets/img/document_example.png'),
		}
	}
}
</script>

<style lang="less" scoped>

#form {
	position: relative;
}

.header {
	padding-top: 48px;
}

.reason {
	padding-top: 40px;
}

.app-document-upload {
	padding-top: 48px;
}

.btns-wrapper {
	position: fixed;
	right: 48px;
	bottom: 96px;

	.btn:not(:last-child) {
		margin-right: 16px;
	}
}

</style>
