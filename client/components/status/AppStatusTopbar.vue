<template>
  <div class="app-status-topbar">
    <div class="row">
      <app-select
        small
        :placeholder="'Обходной лист'"
        :options="sheetsTitle"
        :value="currentSheetTitle"
        @input="$emit('changeSheetTitle', $event)"
        class="sheet-select"
      />
    </div>

    <div class="row">
      <app-search
        round
        small
        :placeholder="'Ф.И.О. студента'"
        :value="searchText"
        @input="$emit('update:searchText', $event)"
        class="search"
      />

      <app-pagination
        :itemsAmount="usersAmount"
        :page="page"
        @updateItemsPerPage="$emit('update:itemsPerPage', $event)"
        @updatePage="$emit('update:page', $event)"

        class="pagination"
      />
    </div>
  </div>
</template>

<script>
import AppSelect from '~/components/common/AppSelect'
import AppPagination from '~/components/common/AppPagination'
import AppSearch from '~/components/common/AppSearch'

export default {
  name: 'AppStatusTopbar',

  components: {
    AppSelect,
    AppPagination,
    AppSearch,
  },

  props: {
    sheetsTitle: {
      type: Array,
      required: true,
    },

    currentSheetTitle: {
      type: String,
      default: '',
    },

    searchText: {
      type: String,
      default: '',
    },

    page: {
      type: Number,
      default: 0,
    },

    itemsPerPage: {
      type: Number,
      default: 0,
    },

    usersAmount: {
      type: Number,
      default: 0,
    },
  },
}
</script>

<style scoped lang="less">
.app-status-topbar {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.row {
  display: flex;
  justify-content: space-between;
}

.search,
.sheet-select {
  min-width: 350px;
  width: 500px;
}

.date-input {
  min-width: 200px;
  width: 300px;
}
</style>
