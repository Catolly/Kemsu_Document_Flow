<template>
	<div class="container">
		<form id="form">
			<h1 class="header">Обходной лист</h1>
			<v-select 
			class="reason"
			id="reason"
			:title="'Причина'"
			:options="reasonOptions"
			required />
			<document-upload class="document-upload">
				Необходимые документы
			</document-upload>
		</form>
	</div>
</template>

<script>
import VButton from '~/components/VButton'
import VSelect from '~/components/VSelect'
import DocumentUpload from '~/components/DocumentUpload'

export default {
	name: 'ThePageCreateBypassSheet',
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
			]
		}
	}
}
</script>

<style lang="less" scoped>

.header {
	padding-top: 48px;
}

.reason {
	padding-top: 40px;
}

.document-upload {
	padding-top: 48px;
}

</style>