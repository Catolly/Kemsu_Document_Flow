<template>
	<div class="container">
		<form id="form">
			<h1 class="header">Обходной лист</h1>
			<v-select 
			placeholder="Причина"
			:options="reasonOptions"
			id="reason"
			class="reason"
			required />
			<document-upload 
			:documentExampleSrc="documentExampleSrc"
			:title="'Необходимые документы'	"
			class="document-upload" />
			<div class="btns-wrapper">
				<v-button class="btn btn-cancel red">
					Отмена
				</v-button>
				<v-button class="btn btn-submit blue filled">
					Отправить
				</v-button>
			</div>
		</form>
	</div>
</template>

<script>
import VButton from '~/components/common/VButton'
import VSelect from '~/components/common/VSelect'
import DocumentUpload from '~/components/bypass-sheets/DocumentUpload'

export default {
	name: 'Create',
	components: {
		VButton,
		VSelect,
		DocumentUpload,
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

.document-upload {
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