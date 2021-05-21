<template>
  <div class="app-schema-edit-point-list">
    <div class="point-list-wrapper">
      <span
        v-if="$v.$anyDirty && $v.$invalid"
        class="error-message"
      >
        Выберите минимум один пункт
      </span>

      <app-list
        :gap="8"
        class="point-list"
      >
        <app-list-item
          v-for="(point, index) in points"
          :key="index"
          :class="{'selected': point === selected}"
          class="point"
          @click="$emit('select', point)"
        >
          <app-checkbox
            class="checkbox"
            v-model="point.checked"
            @input="$v.points.$touch()"
          />
          {{ point.title }}
        </app-list-item>
      </app-list>
    </div>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators"

import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppCheckbox from '~/components/common/AppCheckbox'

const checkedAtListOne = (points, vm) => {
  return points.some(point => point.checked)
}

export default {
  name: 'AppSchemaEditPointList',

  components: {
    AppList,
    AppListItem,
    AppCheckbox,
  },

  validations: {
    points: { checkedAtListOne }
  },

  props: {
    points: {
      type: Array,
      required: true,
    },

    selected: {
      type: Object,
      default:() => {},
    },
  },

  created() {
    this.$watch('$v.$invalid', () => {
        this.$emit('touch', this.$v.$invalid)
    }, {
      deep: true,
      immediate: true,
    })
  },
}
</script>

<style lang="less" scoped>
.app-schema-edit-point-list {
  display: flex;
  flex-direction: column;
  gap: 16px;

  position: relative;
}

.point-list-wrapper {
  position: absolute;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  gap: 16px;
}

.point-list {
  max-height: stretch;
  height: min-content;
  overflow-y: auto;

  padding-right: 8px; // для разделения со скроллом
}

.point {
  padding: 20px 28px;
  height: fit-content;
  border-radius: 5px;

  display: flex;
  justify-content: flex-start;
  gap: 16px;
}

.checkbox {
  flex-shrink: 0;
}

.selected {
  &,
  &:hover {
    color: @green;
    border-color: @green;
  }
}
</style>
