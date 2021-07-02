<template>
  <div>
    <Nuxt />
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { CHECK_AUTH } from '~/store/actions.type'

export default {
  name: 'printLayout',

  computed: {
    ...mapGetters(['isAuthenticated']),
  },

  beforeMount() {
    this.$store.dispatch(CHECK_AUTH)
      .then(() => {
        if (!this.isAuthenticated) this.$router.push('/login')
      })
  },
}
</script>
