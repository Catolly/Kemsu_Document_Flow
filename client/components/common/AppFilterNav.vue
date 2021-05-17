<template>
	<nav :class="{ 'hidden': !filterPathClear.length }" class="app-filter-nav">
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
			{{filterPathBody}}
      <span class="filter-head">{{filterPathHead}}</span>
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
    filterPath: {
      type: Array,
      default:() => ([])
    },
  },

  computed: {
    filterPathHead() {
      return this.filterPathClear
      .slice(-1)
      .join()
    },

    filterPathBody() {
      if (this.filterPathClear.length <= 1) return ''

      return this.filterPathClear
      .slice(0, -1)
      .join(' / ') + ' / ' // Разделитель последнего элемента
    },

    filterPathClear() {
      return this.filterPath.filter(filterName => filterName)
    },
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

.back-button {
  height: fit-content;
  width: fit-content;
}

.filter-body {
	color: @text-grey;
	font-size: @fz-small;
  font-weight: @fw-normal;
}

.filter-head {
	color: @black;
}

.hidden {
  visibility: hidden;
}
</style>
