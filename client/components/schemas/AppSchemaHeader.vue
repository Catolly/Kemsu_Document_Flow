<template>
  <div
    class="app-schema-header"
    @click="$emit('open')"
  >
    <div class="title">
      {{ title }}
    </div>
    <div class="icons">
      <div
        class="edit-btn"
        @click="$emit('edit', id)"
      >
        <icon-edit class="edit"/>
      </div>
      <div
        class="arrow"
        :class="{'rotate': isOpen}"
      />
    </div>
  </div>
</template>

<script>
import iconEdit from '~/components/icons/iconEdit'

export default {
  name: 'AppSchemaHeader',

  components: {
    iconEdit,
  },

  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },

    id: {
      type: String | Number,
      required: true,
    },

    title: {
      type: String,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
.app-schema-header {
  width: 100%;

  padding: 48px 40px;

  position: relative;

  display: flex;
  justify-content: space-between;
  align-items: center;

  background: @grey-bright;
}

.title {
  font-size: @fz-large;
  font-weight: @fw-normal;
}

.icons {
  display: flex;
  align-items: center;
  gap: 48px;
}

.edit {
  height: 20px;
  width: 20px;

  fill: @black;

  &:hover,
  &:active, {
    fill: @blue-hover;
  }
}

.arrow {
  .arrow();
  position: relative;
  right: 0;

  &.rotate {
    transform: rotate(180deg);
  }
}
</style>
