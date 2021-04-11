<template>
	<div class="container">
		<h2 class="header">
			{{title}}
		</h2>
		<div class="app-document-upload-container">
			<div class="document-example">
				<span class="subheader">Образец</span>
				<img
				:src="documentExampleSrc"
				class="document-example-img">
			</div>
			<div class="app-document-upload">
				<span class="subheader">Заявление</span>
				<app-image-upload class="app-image-upload" />
			</div>
		</div>
	</div>
</template>

<script>
import AppImageUpload from '~/components/bypass-sheets/AppImageUpload'

export default {
	name: 'AppDocumentUpload',
	components: {
		AppImageUpload,
	},
	props: {
		title: {
			type: String,
			required: true
		},
		documentExampleSrc: {
			type: String,
			required: true
		}
	}
}
</script>

<style lang="less" scoped>

.app-document-upload-container{
	.flex(flex-start);
}

.document-example,
.app-document-upload {
	.flex(flex-start, normal, column);
	margin-top: 24px;
}

.document-example {
	margin-right: 24px;
}

.subheader {
	display: inline-block;
	width: fit-content;

	font-size: @fz-normal;
	font-weight: @fw-light;
}

.document-example-img,
.app-image-upload {
	height: 200px;
	width: 200px;

	margin-top: 16px;
}

.document-example-img {
	background: #F1F1F1;
	border-radius: 5px;
}

</style>
