<template>
  <div
    :class="{'vertical': vertical}"
    class="app-radio-group"
  >
    <label
    v-for="(option, index) in optionList"
    :key="index"
    class="option">
      <app-radio
        :value="option === value"
        class="radio"
        @input="select(option)"
      />
      <span>{{ option }}</span>
    </label>
  </div>
</template>

<script>
import AppRadio from '~/components/common/AppRadio'

export default {
  name: 'AppRadioGroup',

  props: {
    value: {
      type: String | Number,
      required: true,
    },

    optionList: {
      type: Array,
      required: true,
    },

    vertical: {
      type: Boolean,
      default: false,
    },
  },

  components: {
    AppRadio,
  },

  watch: {
    value() {
      this.selectFirstIfValueIsInvalid()
    },
  },

  methods: {
    select(option) {
      this.$emit('input', option)
    },

    selectFirstIfValueIsInvalid() {
      if (!this.value || !this.optionList.includes(this.value))
        this.select(this.optionList[0])
    }
  },

  created() {
    this.selectFirstIfValueIsInvalid()
  },
}
</script>

<style lang="less" scoped>
.app-radio-group {
  display: flex;
  gap: 24px;

  &.vertical {
    flex-direction: column;
    gap: 16px;
  }
}

.option {
  display: flex;
  align-items: center;
  gap: 12px;

  font-size: @fz-normal;
  font-weight: @fw-light;
}
</style>
