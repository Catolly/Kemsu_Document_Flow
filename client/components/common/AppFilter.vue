<template>
  <div class="app-filter">

    <div class="topbar">
      <h2 class="header">Фильтры</h2>

      <app-button
        class="plain underlined red"
        @click="$emit('clear')"
      >
        Сбросить
      </app-button>
    </div>

    <app-list
      class="filter-list"
      :gap="16"
    >
      <app-select
        v-for="(filter, index) in filterList"
        :key="index"
        :placeholder="filter.placeholder"
        :options="filter.options.map(option => option + (filter.postfix || ''))"
        :value="filter.selected + (filter.selected && filter.postfix || '')"
        class="select"
        @input="select($event, filter)"
      />
    </app-list>

  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppSelect from '~/components/common/AppSelect'
import AppList from '~/components/common/AppList'

export default {
  name: 'AppFilter',

  components: {
    AppButton,
    AppSelect,
    AppList,
  },

  props: {
    filterList: {
      type: Array,
      required: true,
    },
  },

  methods: {
    select(selected, filter) {
      if (filter.postfix) {
        selected = selected.substring(0, selected.indexOf(filter.postfix))
      }

      this.$emit('select', [selected, filter])
    }
  },
}
</script>

<style lang="less" scoped>

.app-filter {
  height: 100vh;
  padding-top: 56px;
  padding-left: 48px;
  border-left: 1px solid #eee;

  .topbar {
    display: flex;
    align-items: baseline;

    .header {
      margin-right: 18px;
    }
  }

  .filter-list {
    margin-top: 64px;
  }
}

@media all and (max-width: 1800px) {

  .app-filter {
    padding-left: 32px;
    padding-right: 32px;
  }

}

</style>
