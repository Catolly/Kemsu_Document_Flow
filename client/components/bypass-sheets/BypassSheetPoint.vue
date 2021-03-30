<template>
	<v-list-item-base
	@click="toggle"
	:class="{ 
		'green': status === 'signed',
		'red': status === 'rejected',
		'disabled': status === 'submitted',
		'is-open' : isOpen
	}"
	class="v-list-item-point">
		<div
		class="point-header">
			<h3 class="point-title">
				{{title}}
			</h3>
			<span
			v-show="isOpen"
			v-if="status === 'rejected'"
			class="reason">
				{{reason}}
			</span>
			<div class="arrow" />
		</div>
		<div 
		@click.stop=""
		v-show="isOpen"
		class="point-inner">
			<div class="required-documents-wrapper">	
				<span class="required-document-header">
					Необходимые документы
				</span>
				<div class="required-documents">
					<img 
					v-for="doc in requiredDocuments"
					:key="doc.id"
					:src="doc.src"
					class="required-document-img">
				</div>
				<span class="worker">
					Поставил отказ <b>{{worker}}</b>
				</span>
				<span class="contacts">
					Телефон библиотеки <b>{{phone}}</b>
				</span>
			</div>
			<form
			v-if="['rejected', 'not sent'].includes(status)" 
			class="send-document-form">
				<h2>Отправить документы</h2>
				<div class="document-upload-section">
					<div 
					v-for="doc in requiredDocuments"
					:key="doc.id"
					class="document-upload-wrapper">
						<span class="document-title">
							{{doc.title}}
						</span>
						<div class="document-upload">
							<v-image-upload 
							class="document-image-upload" />
							<img class="document-image-uploaded">
						</div>
					</div>
				</div>
				<v-button id="submit" class="blue filled">
					Отправить
				</v-button>
			</form>
			<div 
			v-else
			class="document-sent">
				<p>
					Ваши документы на проверке, вы можете 
					<NuxtLink class="document-cancel-link" to="#">отменить отправку</NuxtLink>
				</p>
			</div>
		</div>
	</v-list-item-base>
</template>

<script>
import VListItemBase from '~/components/common/VListItemBase'
import VImageUpload from '~/components/bypass-sheets/VImageUpload'
import VButton from '~/components/common/VButton'

export default {
	name: 'BypassSheetPoint',
	components: {
		VListItemBase,
		VImageUpload,
		VButton,
	},
	data() {
		return {
			isOpen: false,
		}
	},
	props: {
		id: {
			type: Number,
			required: true
		},
		status: {
			type: String,
			required: true
		},
		title: {
			type: String,
			required: true
		},
		reason: String,
		requiredDocuments: Array,
		worker: String,
		phone: String,
	},
	methods: {
		toggle: function() {
			this.isOpen = !this.isOpen
		}
	}
}
</script>

<style lang="less" scoped>

.green {
	color: @green;
	border-color: @green;
}

.red {
	color: @red;
	border-color: @red;
}

.disabled {
	color: @text-grey;
	border-color: #F3F3F3;
}

.point {
	position: relative;
	.flex(space-between, normal, column);

	&.is-open .arrow {
		transform: rotate(180deg);
	}

	&.is-open:hover {
		background: #FDFDFD;
	}

	&.is-open:before {
		.absolute();
		top: 0;
		right: 0;

		height: 100%;
		width: 50%;

		background-color: #F5F5F5;
		border-radius: 0 12px 12px 0;
	}
}

.point-header,
.point-inner {
	z-index: 1;	
}

.point-header {
	position: relative;
	min-width: 100%;
	.flex(flex-start, normal, column);
}

.arrow {
	.absolute();
	@size: 8px;
	top: .5*(@fz-h2 - @size);
	right: 4px;

	width: 0;
	height: 0;
 
	border-top: @size solid #262626;
	border-left: .5*@size solid transparent;
	border-right: .5*@size solid transparent;
}

.reason {
	margin-top: 8px;
}

.point-inner {
	.flex(space-between, normal, row);
	color: #000;
	font-weight: @fw-light;
	cursor: default;

	.required-documents-wrapper {
		margin-top: 40px;
		.flex(flex-start, normal, column);

		.required-documents {
			margin-top: 24px;
			.flex(flex-start);
		}

		.required-document-img {
			width: 116px;
			height: 116px;
			margin-right: 16px;
		}

		.worker {
			margin-top: 24px;
		}

		.contacts {
			margin-top: 16px;
		}
	}

	.send-document-form {
		z-index: 0;
		width: 50%;
		padding-top: 8px;
		padding-left: 64px;

		.document-upload-section {
			margin-top: 24px;
			.flex(flex-start);

			.document-upload-wrapper {
				margin-right: 32px;
			}

			.document-upload {
				margin-top: 12px;
				.flex(flex-start, normal);
			}

			.document-image-upload,
			.document-image-uploaded {
				width: 100px;
				height: 100px;
			}

			.document-image-upload {
				margin-right: 16px;
			}

			.document-image-uploaded {
				background: #C4C4C4;

				&:not(:last-child) {
					margin-right: 16px;
				}
			}
		}

		#submit {
			margin-top: 24px;
		}
	}

	.document-sent {
		.flex(center, center);
		width: 50%;

		p {
			display: inline-block;
			width: 300px;
		}

		.document-cancel-link {
			color: #000;

			&:after {
				border-color: #000;
			}
		}
	}

	b {
		font-weight: @fw-medium;
	}
}

</style>