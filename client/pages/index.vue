<template>
	<div></div>
</template>

<script>
import { mapGetters } from 'vuex'
import { ROLE_IS } from '~/store/actions.type'

export default {
  name: 'index',

  async beforeMount() {
    try {
      await Promise.all([
        this.$store.dispatch(ROLE_IS, this.Role.Student),
        this.$store.dispatch(ROLE_IS, this.Role.Staff),
        this.$store.dispatch(ROLE_IS, this.Role.Admin),
      ])

      if (this.Role.isStudent) this.$router.push('bypass-sheets/')
      if (this.Role.isStaff) this.$router.push('bypass-sheets/')
      if (this.Role.isAdmin) this.$router.push('schemas/')
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters(['Role'])
  },
}
</script>
