<template>
	<roleStudent class="container">
    <template v-if="sheet">
  		<div class="head">
        <h1 class="header">Обходной лист - {{sheet.title}}</h1>
        <span v-if="fetchSheetError" class="error-message">
          Не удалось загрузить обходной лист
        </span>
      </div>

  		<app-list	class="point-list">
  			<app-bypass-sheet-point
  				v-for="(point, index) in sheet.points"
  				:key="index"
          :point="point"
  				class="point"
        />
  		</app-list>
    </template>
	</roleStudent>
</template>

<script>
import { WAIT_FOR } from "~/store/actions.type"
import { copy } from "~/store/methods"

import bypassSheetStatus from '~/services/bypassSheetStatus'

import roleStudent from '~/components/roles/roleStudent'

import AppList from '~/components/common/AppList'
import AppBypassSheetPoint from '~/components/bypass-sheets/AppBypassSheetPoint'

export default {
  middleware: 'authenticated',

	components: {
    roleStudent,
		AppList,
    AppBypassSheetPoint,
	},

  async fetch() {
    try {
      this.fetchSheetError = ''
      await this.$store.dispatch(WAIT_FOR, 'checkingAuth')

      const id = this.$route.params.id
      const sheet = this.$store.getters
        .currentUser
        .bypassSheets
          .find(sheet => sheet.id == id)

      if (!sheet) {
        return this.$nuxt.error({ statusCode: 404 })
      }

      this.sheet = copy(sheet)
      this.sheet.points
        .forEach(point => {
          point.uploadedDocuments = []
          if (point.uploadDocumentsFormat.length === 0
              && point.status === this.bypassSheetStatus.Rejected)
            point.uploadDocumentsFormat.push({
              title: 'Необходимые документы'
            })
        })
    }
    catch (error) {
      console.error(error)
      this.fetchSheetError = error
    }
  },

	data:() => ({
    sheet: null,
    fetchSheetError: '',
	}),

  computed: {
    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },
}
</script>

<style lang="less" scoped>
.container,
.head {
  display: flex;
  flex-direction: column;
}

.container {
	padding-top: 48px;

  gap: 48px;
}

.head {
  gap: .5em;
}
</style>

