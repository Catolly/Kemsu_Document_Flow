<template>
	<app-list-item
  	:class="classObj"
  	class="point"
  >
		<div
  		class="point-header"
      @click="isOpen = !isOpen"
    >
			<h3 class="point-title">{{point.title}}</h3>
			<div class="arrow" />
		</div>

		<div v-show="isOpen" class="point-body">
			<div class="about">
        <span
          v-show="isOpen"
          v-if="[
            bypassSheetStatus.Rejected,
            bypassSheetStatus.Reviewing
          ].includes(point.status)"
          :class="classObj"
        >
          {{point.rejectReason}}
        </span>

        <div class="required-documents">
          <template v-if="point.requiredDocuments.length">
    				<span class="header">Необходимые документы:</span>
    				<div class="download-list">
              <app-download-file
                v-for="(file, index) in point.requiredDocuments"
                :key="index"
                normal
                :file="file"
                class="download"
              />
    				</div>
          </template>
        </div>

        <div
          v-if="[
            bypassSheetStatus.Signed,
            bypassSheetStatus.Rejected
          ].includes(point.status)"
          class="staff-about"
        >
  				<span class="name">
  					Поставил {{
              point.status === bypassSheetStatus.Signed
              ? 'подпись'
              : 'отказ'
            }}:
            <b>{{ staffShortname }}</b>
  				</span>
        </div>
			</div>

      <h2
        class="not-required"
        v-if="point.status === bypassSheetStatus.Signed"
      >
        Заявление подписано
      </h2>

      <app-bypass-sheet-point-form
        v-else-if="[
          bypassSheetStatus.Rejected,
          bypassSheetStatus.NotSent
        ].includes(point.status)"
        :point="point"
        @success="point.status = bypassSheetStatus.Reviewing"
        class="send-form"
      />

			<div v-else class="sent">
				<p>
					Ваши документы на проверке,
          <br>
          вы можете
					<a
            @click="point.status = bypassSheetStatus.NotSent"
            class="cancel-link"
          >
            переотправить их
          </a>
				</p>
			</div>
		</div>
	</app-list-item>
</template>

<script>
import bypassSheetStatus from '~/services/bypassSheetStatus'

import AppListItem from '~/components/common/AppListItem'
import AppDownloadFile from '~/components/common/AppDownloadFile'
import AppBypassSheetPointForm from '~/components/bypass-sheets/AppBypassSheetPointForm'

export default {
	name: 'AppBypassSheetPoint',

	components: {
		AppListItem,
		AppDownloadFile,
    AppBypassSheetPointForm,
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
      requiredDocuments: {
        type: Array,
        required: true,
      },
      uploadedDocuments: {
        type: Array,
      },
      uploadDocumentsFormat: {
        type: Array,
      },
      rejectReason: {
        type: String,
        default: '',
      },
      staff: {
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
    staffShortname() {
      const [firstname, lastname, middlename] = this.point.staff.split(' ')
      return firstname + ' ' + lastname[0] + '.' + (middlename ? middlename[0] + '.' : '')
    },

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
	border-color: @grey-light;
}

.point,
.point-header,
.about,
.required-documents,
.staff-about {
  display: flex;
  flex-direction: column;
}

.point {
  padding: 0;
  justify-content: space-between;
	position: relative;

	&.is-open {
    .arrow {
  		transform: rotate(180deg);
  	}
    .point-header {
      padding-bottom: 8px;
    }

    &:hover {
      background: @grey-bright;
    }
    &:before {
      .absolute();
      top: 0;
      right: 0;

      height: 100%;
      width: 50%;

      background-color: @grey-light;
      border-radius: 0 12px 12px 0;
    }
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

  gap: 8px;
}

.point-title {
  width: 50%;
  padding-right: 48px;
}

.arrow {
	.arrow();
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
}

.about {
  gap: 24px;
}

.required-documents {
  gap: 16px;
}

.download-list {
	display: flex;
  flex-flow: wrap;
  gap: 16px;
}

.staff-about {
  gap: 8px;
}

.not-required {
  margin-left: auto;
  margin-right: auto;
}

.send-form {
	z-index: 0;
	padding-left: 64px;
}

.not-required,
.sent {
  position: absolute;
  top: calc(50% - 24px);
  right: 0;
  width: 50%;

	display: flex;
  justify-content: center;
  align-items: center;

  p {
    max-width: 380px;
  }
}

.cancel-link {
	color: @black;

	&:after {
		border-color: @black;
	}
}

b {
	font-weight: @fw-medium;
}
</style>
