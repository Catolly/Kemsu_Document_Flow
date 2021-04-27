<template>
  <div class="app-sign-topbar">
    <app-button
      class="btn green filled"
      @click="$emit('signChecked')"
    >
      Подписать ({{checkedPointsCount}})
    </app-button>

    <app-button
      class="btn"
      @click="$emit('checkAll')"
    >
      Выбрать всех
    </app-button>

    <app-button
      class="btn"
      @click="$emit('uncheckAll')"
    >
      Снять выбор
    </app-button>

    <app-search
      :value="searchText"
      @input="$emit('search', $event)"
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
  margin-top: 48px;

  display: flex;

  .btn {
    margin-right: 18px;

    &:first-child {
      margin-right: 24px;

    }
  }

  .search {
    width: 340px;

    padding: 0;
    margin: 0;
    margin-left: auto;
  }
}
</style>
