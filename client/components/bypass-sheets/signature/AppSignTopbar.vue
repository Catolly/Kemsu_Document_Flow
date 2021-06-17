<template>
  <div class="app-sign-topbar">
    <app-button
      class="btn green filled"
      @click="$emit('signChecked')"
    >
      Подписать ({{checkedPointsCount}})
    </app-button>

    <app-button
      class="btn plain"
      @click="$emit('checkAll')"
    >
      Выбрать всех
    </app-button>

    <app-button
      class="btn plain"
      @click="$emit('uncheckAll')"
    >
      Снять выбор
    </app-button>

    <app-search
      :value="searchText"
      @change="$emit('search', $event)"
      round
      small
      class="search"
    />
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppSearch from '~/components/common/AppSearch'

export default {
  name: 'AppSignTopbar',

  components: {
    AppButton,
    AppSearch,
  },

  props: {
    checkedPointsCount: {
      type: Number,
      default: 0,
    },
    searchText: {
      type: String,
    }
  },
}
</script>

<style lang="less" scoped>
.app-sign-topbar {
  display: flex;
  align-items: center;
  gap: 18px;

  .btn:first-child {
    margin-right: 6px;
  }

  .search {
    width: 340px;
    margin-left: auto;
  }
}
</style>
