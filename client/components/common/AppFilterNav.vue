<template>
	<nav class="app-filter-nav">
  	<app-button
      icon
      blue
      square
		  class="back-button"
      @click="$emit('setFilterDepth', filterPathClear.length - 2)"
    >
			<icon-arrow/>
		</app-button>

  	<span class="filter-body">
			{{filterNamesBody}}
      <span class="filter-head">{{filterNamesHead}}</span>
		</span>

  </nav>

</template>

<script>
import IconArrow from '~/components/icons/IconArrow'
import AppButton from '~/components/common/AppButton'

export default {
	name: "AppFilterNav",

	components: {
		IconArrow,
    AppButton,
	},

  props: {
    filterNames: {
      type: Array,
      default:() => ([])
    },
  },

  computed: {
    // Переименовать filterPathHead
    filterNamesHead() {
      return this.filterNamesClearedEmpty.slice(-1).join()
    },

    // Переименовать filterPathBody
    filterNamesBody() {
      if (this.filterNamesClearedEmpty.length <= 1) return ''

      return this.filterNamesClearedEmpty.slice(0, -1)
                                         .join(' / ') +
                                         ' / ' // Разделитель последнего элемента
    },

    // Заменить на filterNamesHead
    filterNamesClearedEmpty() {
      return this.filterNames.filter(filterName => filterName)
    },

    // filterPath() {
    //   return
    // },
  },
}
</script>

<style lang="less" scoped>
.app-filter-nav {
  margin-top: 16px;

  display: flex;
  align-items: center;
  gap: 24px;
}

  .filter-body {
  	color: @text-grey;
  	font-size: @fz-small;
    font-weight: @fw-normal;
  }
.back-button {
  height: fit-content;
  width: fit-content;
}

  .filter-head {
  	color: #000;
  }
}

</style>
