<template>
  <app-list-item
    class="app-schema"
  >
    <!-- schema header -->
    <app-schema-header
      :isOpen="isOpen"
      :title="schema.title"
      :id="schema.id"
      class="header"
      @open="toggle"
      @edit="$emit('edit', $event)"
    />

    <!-- schema body -->
    <app-schema-body
      v-if="isOpen"
      :points="schema.points"
      :URL="URL"
      :id="schema.id"
      class="body"
    />
  </app-list-item>
</template>

<script>
import AppListItem from '~/components/common/AppListItem'
import AppSchemaHeader from '~/components/schemas/AppSchemaHeader'
import AppSchemaBody from '~/components/schemas/AppSchemaBody'

export default {
  name: 'AppSchema',

  components: {
    AppListItem,
    AppSchemaHeader,
    AppSchemaBody,
  },

  data:() => ({
    isOpen: false,
  }),

  props: {
    URL: {
      type: String,
      required: true,
    },

    schema: {
      type: Object,
      required: true,

      id: {
        type: String | Number,
        required: true,
      },

      title: {
        type: String,
        required: true,
      },

      points: {
        type: Array,
        required: true,
      }
    },
  },

  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
  },
}
</script>

<style lang="less" scoped>
.app-schema {
  padding: 0;

  display: flex;
  flex-direction: column;

  overflow: auto;
}

.body {
  width: 100%;

  padding: 48px;
  padding-bottom: 24px;

  border: none;

  cursor: auto;
  background: @white;
}

</style>
