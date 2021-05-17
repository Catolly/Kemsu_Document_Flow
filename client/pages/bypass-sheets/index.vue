<template>
	<roleStudentStaff class="container">
		<app-bypass-sheet-list-student v-if="Role.isStudent"/>
		<app-bypass-sheet-list-staff v-if="Role.isStaff"/>
	</roleStudentStaff>
</template>

<script>
import { mapGetters } from 'vuex'
import { ROLE_IS } from '~/store/actions.type'

import roleStudentStaff from '~/components/roles/roleStudentStaff'

import AppBypassSheetListStudent from '~/components/bypass-sheets/AppBypassSheetListStudent'
import AppBypassSheetListStaff from '~/components/bypass-sheets/AppBypassSheetListStaff'

export default {
  middleware: 'authenticated',

	components: {
    roleStudentStaff,
    AppBypassSheetListStudent,
    AppBypassSheetListStaff,
	},

  async beforeMount() {
    try {
      await Promise.all([
        this.$store.dispatch(ROLE_IS, this.Role.Student),
        this.$store.dispatch(ROLE_IS, this.Role.Staff)
      ])
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters(['Role'])
  },
}
</script>
