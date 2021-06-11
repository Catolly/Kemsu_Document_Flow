<template>
  <div class="app-pagination">
    <span>Показывать по:</span>
    <app-select
      v-model="selectedItemsPerPage"
      :options="itemsPerPage"
      small
      class="items-per-page"
    />

    <div class="nav-btns">
      <app-button
        small
        square
        filled
        blue
        :disabled="page <= 0"
        class="prev"
        @click="$emit('updatePage', page - 1)"
      >
        <div class="arrow" />
      </app-button>

      <span class="currentPage">{{page + 1}} из {{maxPage}}</span>

      <app-button
        small
        square
        filled
        blue
        :disabled="page >= maxPage - 1"
        class="next"
        @click="$emit('updatePage', page + 1)"
      >
        <div class="arrow" />
      </app-button>
    </div>
  </div>
</template>

<script>
import AppSelect from '~/components/common/AppSelect'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppPagination',

  components: {
    AppSelect,
    AppButton,
  },

  data:() => ({
    selectedItemsPerPage: 0,
  }),

  props: {
    page: 0,

    itemsPerPage: {
      type: Array,
      default:() => [
        5,
        10,
        20,
        50,
        100,
        1000
      ],
    },

    itemsAmount: {
      type: Number,
      required: true,
    },
  },

  watch: {
    selectedItemsPerPage() {
      this.$emit('updateItemsPerPage', this.selectedItemsPerPage)
      this.$emit('updatePage', 0)
    },
  },

  computed: {
    maxPage() {
      return Math.ceil(this.itemsAmount / this.selectedItemsPerPage)
    },
  },

  created() {
    this.selectedItemsPerPage = this.itemsPerPage[0]
  },
}
</script>

<style lang="less" scoped>
.app-pagination,
.nav-btns {
  display: flex;
  align-items: center;
  gap: 16px;
}

.arrow {
  @size: 8px;
  .arrow(@size);

  top: 50% - @size;
  right: 50% - @size;

  border-top-color: @white;
}

.currentPage {
  min-width: 60px;
  max-width: 100px;

  display: flex;
  justify-content: center;
}

.prev {
  transform: rotate(90deg);
}

.next {
  transform: rotate(270deg);
}

.items-per-page {
  width: 120px;
}
</style>
