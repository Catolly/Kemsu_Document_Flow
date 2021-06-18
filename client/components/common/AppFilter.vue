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
      <app-autocomplete
        v-for="(filter, index) in localFilterList"
        :key="index"
        v-model="filter.selected"
        :placeholder="filter.placeholder"
        :options="filterOptions(filter)"
        class="select"
        @change="select($event, filter)"
      />
    </app-list>

  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppSelect from '~/components/common/AppSelect'
import AppAutocomplete from '~/components/common/AppAutocomplete'
import AppList from '~/components/common/AppList'

export default {
  name: 'AppFilter',

  components: {
    AppButton,
    AppSelect,
    AppAutocomplete,
    AppList,
  },

  data:() => ({
    localFilterList: [],
  }),

  props: {
    filterList: {
      type: Array,
      required: true,
    },
  },

  watch: {
    filterList() {
      this.localFilterList = this.filterList
    },

    localFilterList() {
      this.localFilterList.forEach(filter => {
        filter.options = filter.options.sort()
        filter.selected += (filter.selected && filter.postfix || '')
      })
    },
  },

  methods: {
    filterOptions(filter) {
      return filter.options
        .map(option => ({
          value: option + (filter.postfix || '')
        }))
    },

    select(selected, filter) {
      if (filter.postfix && filter.selected.split(' ').length > 1) {
        selected = selected.substring(0, selected.indexOf(filter.postfix))

        // Перевод строки в число, если возможно
        if (!!+selected)
          selected = +selected
      }

      if (filter.options.some(option =>
        String(option).toLowerCase() === String(selected).toLowerCase())
      )
        this.$emit('select', [selected, filter])
    },
  },
}
</script>

<style lang="less" scoped>

.app-filter {
  height: 100vh;
  padding-top: 56px;
  padding-left: 48px;
  border-left: 1px solid @grey-medium;
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
