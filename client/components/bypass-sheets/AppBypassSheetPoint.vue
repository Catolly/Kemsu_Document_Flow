<template>
	<app-list-item
  	:class="classObj"
  	class="point"
  >
		<div
  		class="point-header"
      @click="isOpen = !isOpen"
    >
			<h3 class="point-title">
				{{point.title}}
			</h3>
			<span
  			v-show="isOpen"
  			v-if="point.status === bypassSheetStatus.Rejected"
  			class="reason"
      >
				{{point.reason}}
			</span>
			<div class="arrow" />
		</div>

<!-- 		@click.stop="" -->
		<div
  		v-show="isOpen"
  		class="point-body"
    >
			<div class="required-documents-wrapper">
				<span class="required-document-header">
					Необходимые документы
				</span>

				<div class="required-documents">
					<img
  					v-for="(doc, index) in point.requiredDocuments"
  					:key="index"
  					:src="doc.src"
  					class="required-document-img"
          >
				</div>

				<span class="worker">
					Поставил отказ <b>{{point.worker}}</b>
				</span>
				<span class="contacts">
					Телефон библиотеки <b>{{point.phone}}</b>
				</span>
			</div>

			<form
  			v-if="[bypassSheetStatus.Rejected, bypassSheetStatus.NotSent].includes(point.status)"
  			class="send-document-form"
      >
				<h2>Отправить документы</h2>

				<div class="app-document-upload-section">
					<div
  					v-for="(doc, index) in point.requiredDocuments"
  					:key="index"
  					class="app-document-upload-wrapper"
          >
						<span class="document-title">
							{{doc.title}}
						</span>

						<div class="app-document-upload">
							<app-image-upload class="document-image-upload" />
							<img class="document-image-uploaded">
						</div>
					</div>
				</div>

				<app-button class="blue filled submit">
					Отправить
				</app-button>
			</form>

			<div
  			v-else
  			class="document-sent"
      >
				<p>
					Ваши документы на проверке, вы можете
					<NuxtLink class="document-cancel-link" to="#">отменить отправку</NuxtLink>
				</p>
			</div>
		</div>
	</app-list-item>
</template>

<script>
import bypassSheetStatus from '~/services/bypassSheetStatus'

import AppListItem from '~/components/common/AppListItem'
import AppImageUpload from '~/components/bypass-sheets/AppImageUpload'
import AppButton from '~/components/common/AppButton'

export default {
	name: 'AppBypassSheetPoint',

	components: {
		AppListItem,
		AppImageUpload,
		AppButton,
	},

	data:() => ({
    isOpen: false,
  }),

	props: {
    point: {
      type: Object,
      required: true,

      status: {
        type: String,
        required: true,
      },

      title: {
        type: String,
        required: true,
      },

      reason: {
        type: String,
        default: '',
      },
      requiredDocuments: {
        type: Array,
        default: [],
      },
      worker: {
        type: String,
        default: '',
      },
      phone: {
        type: String,
        default: '',
      },
    },
	},

  computed: {
    classObj() {
      return {
        'green': this.point.status === bypassSheetStatus.Signed,
        'red': this.point.status === bypassSheetStatus.Rejected,
        'disabled': this.point.status === bypassSheetStatus.Reviewing,
        'is-open' : this.isOpen,
      }
    },

    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },

	methods: {

	},
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
  padding: 0;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

	position: relative;

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
.point-body {
	z-index: 1;
}

.point-header {
  padding: 40px 48px;
	min-width: 100%;

	position: relative;

  display: flex;
  flex-direction: column;
}

.arrow {
	.arrow();
}

.reason {
	margin-top: 8px;
}

.point-body {
  padding: 0 48px 40px;

  width: 100%;

  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-column-gap: 96px;

	color: @black;
	font-weight: @fw-light;
	cursor: default;

	.required-documents-wrapper {
    display: flex;
    flex-direction: column;

		.required-documents {
			margin-top: 24px;

      display: flex;
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
		padding-left: 64px;

		.app-document-upload-section {
			margin-top: 24px;

      display: flex;

			.app-document-upload-wrapper {
				margin-right: 32px;
			}

			.app-document-upload {
				margin-top: 12px;

        display: flex;
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

		.submit {
			margin-top: 24px;
		}
	}

	.document-sent {
		display: flex;
    justify-content: center;
    align-items: center;

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
