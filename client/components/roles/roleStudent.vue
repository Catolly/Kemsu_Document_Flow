<template>
  <div>
    <slot />
  </div>
</template>

<script>
import Role from '~/services/role'
import { CHECK_ROLE, WAIT_FOR } from '~/store/actions.type'
import { SET_ERROR } from '~/store/mutations.type'

export default {
  name: 'roleStudent',

  async beforeMount() {
    try {
      await this.$store.dispatch(WAIT_FOR, 'checkingAuth')
      const hasAccess = await this.$store.dispatch(CHECK_ROLE, Role.Student)
      if (!hasAccess) this.$router.push('/')
    } catch (error) {
      console.error(error)
      this.$store.commit(SET_ERROR, error)
      this.$router.push('/')
    }
  },
}
</script>
