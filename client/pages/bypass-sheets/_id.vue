<template>
	<div class="container">
		<h1 class="header">
			Обходной лист - {{title}}
		</h1>
		<nav class="group-nav">
			<NuxtLink 
			to="#"
			class="back-link">
				<icon-arrow-back class="active"/>
			</NuxtLink>
			<NuxtLink 
			to="#"
			class="next-link">
				<icon-arrow-next/>
			</NuxtLink>
			<span class="group-path">
				Университет 8 / ... / Факультет 6 / <span class="group">Группа 5</span>
			</span>
		</nav>
		<v-list class="point-list">
			<v-list-item
				v-for="point in points"
				:key="point.id"
				@click="toggle(point)"
				:class="{ 
					'green' : point.status === 'signed',
					'red': point.status === 'rejected',
					'disabled': point.status === 'submitted',
					'open' : point.open
			  }"
				class="point">
				<div
				class="point-header">
					<h3 class="point-title">
						{{point.title}}
					</h3>
					<span
					v-show="point.open"
					v-if="point.status === 'rejected'"
					class="reason">
						{{point.reason}}
					</span>
					<div class="arrow" />
				</div>
				<div 
				@click.stop=""
				v-show="point.open"
				class="point-inner">
				<div class="required-documents-wrapper">	
					<span class="required-document-header">
						Необходимые документы
					</span>
					<div class="required-documents">
						<img 
						v-for="doc in point.requiredDocuments"
						:key="doc.id"
						:src="doc.src"
						class="required-document-img">
					</div>
					<span class="worker">
						Поставил отказ <b>{{point.worker}}</b>
					</span>
					<span class="contacts">
						Телефон библиотеки <b>{{point.phone}}</b>
					</span>
				</div>
				<form
				v-if="['rejected', 'not sent'].includes(point.status)" 
				class="send-document-form">
					<h2>Отправить документы</h2>
					<div class="document-upload-section">
						<div 
						v-for="doc in point.requiredDocuments"
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
		</v-list-item>
		</v-list>	
	</div>
</template>

<script>
import IconArrowBack from '~/components/icons/IconArrowBack'
import IconArrowNext from '~/components/icons/IconArrowNext'
import VList from '~/components/VList'
import VListItem from '~/components/VListItem'
import VImageUpload from '~/components/VImageUpload'
import VButton from '~/components/VButton'

export default {
	components: {
		IconArrowBack,
		IconArrowNext,
		VList,
		VListItem,
		VImageUpload,
		VButton
	},
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
					open: false,
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
					open: true,
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
					open: false,
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
					open: false,
				},
			]
		}
	},
	methods: {
		toggle: function(point) {
			point.open = !point.open
		}
	}
}
</script>

<style lang="less" scoped>

.header {
	margin-top: 48px;
}

.group-nav {
	margin-top: 16px;
}

.back-link:after,
.next-link:after {
	display: none;
}

.back-link {
	margin-right: 14px;
}

.next-link {
	margin-right: 28px;
}

.group-path {
	color: @text-grey;
	font-size: @fz-small;
}

.group {
	color: #000;
}

.point-list {
	margin-top: 48px;
}

.point {
	position: relative;
	.flex(space-between, normal, column);

	&.open .arrow {
		transform: rotate(180deg);
	}

	&.open:before {
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