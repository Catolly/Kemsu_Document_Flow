<template>
	<roleStudent class="container">
		<h1 class="header">
			Обходной лист - {{title}}
		</h1>

		<app-list	class="point-list">
			<app-bypass-sheet-point
				v-for="(point, index) in points"
				:key="index"
        :point="point"
				class="point"
      />
		</app-list>
	</roleStudent>
</template>

<script>
import { WAIT_FOR } from "~/store/actions.type"
import { copy } from "~/store/methods"

import roleStudent from '~/components/roles/roleStudent'

import AppList from '~/components/common/AppList'
import AppBypassSheetPoint from '~/components/bypass-sheets/AppBypassSheetPoint'

export default {
	components: {
    roleStudent,
		AppList,
    AppBypassSheetPoint,
	},

	data:() => ({
    sheet: null,
    fetchSheetError: '',
	}),

  async beforeMount() {
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
    }
    catch (error) {
      console.error(error)
      this.fetchSheetError = error
    }
  },
}
</script>

<style lang="less" scoped>
.container,
.point-list {
	margin-top: 48px;
}
</style>
