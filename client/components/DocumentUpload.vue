<template>
	<div class="container">
		<h2 class="header">
			{{title}}
		</h2>
		<div class="document-upload-container">
			<div class="document-example">
				<span class="subheader">Образец</span>
				<img
				:src="documentExampleSrc" 
				class="document-example-img">
			</div>			
			<div class="document-upload">
				<span class="subheader">Заявление</span>
				<v-image-upload class="v-image-upload" />
			</div>
		</div>
	</div>
</template>

<script>
import VImageUpload from '~/components/VImageUpload'

export default {
	name: 'FormImageUpload.vue',
	components: {
		VImageUpload,
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

.document-upload-container{
	.flex(flex-start);
}

.document-example,
.document-upload {
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
.v-image-upload {
	height: 200px;
	width: 200px;
	
	margin-top: 16px;
}

.document-example-img {
	background: #F1F1F1;
	border-radius: 5px;
}

</style>