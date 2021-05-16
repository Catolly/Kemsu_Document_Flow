<template>
  <div>
    <slot />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { ROLE_IS } from '~/store/actions.type'

export default {
  name: 'roleAdmin',

  async beforeMount() {
    try {
      const hasAccess = await this.$store.dispatch(ROLE_IS, this.Role.Admin)
      if (!hasAccess) this.$router.push('/')
    } catch (error) {
      console.error(error)
      this.$router.push('/')
    }
  },

  computed: {
    ...mapGetters(['Role'])
  },
}
</script>
