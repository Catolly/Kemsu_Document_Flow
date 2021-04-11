<template>
  <div class="app-search-wrapper">
    <app-input
      :value="value"
      @input="updateValue"
      :type="type"
      :required="required"
      :disabled="disabled"
      :placeholder="placeholder"
      :class="{'round': round}"
      class="app-search"
    />
    <icon-search
      v-show="!value"
      class="icon-search"
    />
  </div>
</template>

<script>
import IconSearch from '~/components/icons/IconSearch'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppSearch',

  components: {
    IconSearch,
    AppInput,
  },

  props: {
    value: String,
    placeholder: String,
    type: {
      type: String,
      default: 'text',
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    round: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    updateValue(value) {
      this.$emit('input', value)
    }
  },
}
</script>

<style lang="less" scoped>
@input-background: #FDFDFD;

.app-search-wrapper {
  transition: .2s ease all;

  margin-top: 18px;
  position: relative;

  height: 70px;
  width: 100%;

  &.round .app-search {
    border-radius: 100px;
  }

  .icon-search {
    display: none;
  }

  &.search {
    .icon-search {
      .absolute();
      top: calc(50% - 12px);
      right: 18px;

      height: 24px;
      width: 24px;
    }
  }
}

.app-search {
  position: relative;

  height: inherit;
  width: inherit;

  background: @input-background;
  border: 1px solid #F3F3F3;
  border-radius: 10px;

  &:focus {
    & ~ .icon-search {
      display: none;
    }
  }
}

</style>
