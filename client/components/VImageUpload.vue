<template>
	<div class="v-image-upload">
		<div class="v-image-upload-inner">
			<img 
			v-if="previewImageURL"
			:src="previewImageURL"
			class="preview-img">
			<img 
			v-if="previewIconURL"
			:src="previewIconURL"
			class="preview-icon">
			<div class="plus"></div>
			<input
			@change="previewFile"
			@click.stop=""
			type="file"
			accept="image/*,image/jpeg,application/pdf,application/pdf,application/msworld, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
			class="input">
		</div>
		<div 
		:title="previewName"
		class="preview-name">
			{{previewName}}
		</div>
	</div>
</template>

<script>
export default {
	name: 'VImageUpload',
	data() {
		return {
			previewName: null,
			previewImageURL: null,
			previewIconURL: null,
		}
	},
	methods: {
		previewFile(event) {
			let file = event.target.files[0]
			let reader = new FileReader()

			reader.onloadend = () => {
				this.setPreviewImage(reader.result)
			}
			if(file) {
				this.previewName = file.name
				
				if(file.type.includes('image')) {
					reader.readAsDataURL(file)
				}
				else if(file.name.toLowerCase().includes('doc', 'docx')) {
					this.setPreviewIcon(require('~/assets/icons/VImageUpload/doc.svg'))
				}
				else if(file.name.toLowerCase().includes('pdf')) {
					this.setPreviewIcon(require('~/assets/icons/VImageUpload/pdf.svg'))
				}
			}
		},
		setPreviewImage(URL) {
			this.previewImageURL = URL
			this.previewIconURL = null
		},
		setPreviewIcon(URL) {
			this.previewImageURL = null
			this.previewIconURL = URL
		}
	},
}
</script>

<style lang="less" scoped>

.v-image-upload {
	position: relative;

}

.v-image-upload-inner {
	position: relative;

	height: 100%;
	width: 100%;

	background: #FDFDFD;
	box-shadow: 0 0 0 1px #D2D2D2;
	box-sizing: border-box;
	border-radius: 5px;
	overflow: hidden;

	&:hover {
		background: #F2F2F2;
			box-shadow: 0 0 0 1px @blue;
	}
}

.input,
.input::-webkit-file-upload-button {
	z-index: 2;

	height: 100%;
	width: 100%;

	outline: 0;
	opacity: 0;
	cursor: pointer;
	user-select: none;
}

.preview-img {
	position: absolute;
	top: 0;
	left: 0;
	
	height: 100%;
	width: 100%;

	opacity: .5;
}

.preview-icon {
	position: absolute;
	top: 10%;
	bottom: 10%;
	left: 10%;
	right: 10%;
	
	height: 80%;
	width: 80%;

	opacity: .5;
}

.preview-name {
	margin-top: 8px;

	font-size: @fz-small;
	text-overflow: ellipsis;
	overflow: hidden;
	white-space: nowrap;
}

.plus {
	position: absolute;

	@size: 20px;
	width: @size;
	height: @size;

	top: calc(50% - .5*@size);
	bottom: 50%;
	left: 50%;
	right: 50%;

	&::before,
	&::after {
		.absolute();
		background: #000;

		width: 10%;
		height: 100%;
	}

	&::before {
		transform: rotate(90deg);
	}
}

</style>