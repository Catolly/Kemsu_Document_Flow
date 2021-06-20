<template>
  <div class="app-deadlines-topbar">
    <div class="row">
      <app-select
        small
        :placeholder="'Обходной лист'"
        :options="sheetsTitle"
        :value="currentSheetTitle"
        @input="$emit('changeSheet', $event)"
        class="sheet-select"
      />

      <div class="row apply-all-inner">
        <app-input
          small
          :placeholder="'число/месяц/год'"
          :value="allGroupsDeadline"
          @input="$emit('update:allGroupsDeadline', $event)"
          class="date-input"
        />

        <app-button
          blue
          @click="$emit('applyAllGroupsDeadline')"
          class="apply-all-btn"
        >
          Применить ко всем
        </app-button>
      </div>
    </div>

    <div class="row">
      <app-search
        round
        small
        :placeholder="'Поиск группы'"
        :value="searchText"
        @input="$emit('update:searchText', $event)"
        class="search"
      />

      <app-pagination
        :itemsAmount="groupsAmount"
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
import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppDeadlinesTopbar',

  components: {
    AppSelect,
    AppPagination,
    AppSearch,
    AppButton,
    AppInput,
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

    allGroupsDeadline: {
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

    groupsAmount: {
      type: Number,
      default: 0,
    },
  },
}
</script>

<style scoped lang="less">
.app-deadlines-topbar {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.row {
  display: flex;
  justify-content: space-between;
}

.apply-all-inner {
  gap: 1em;
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
