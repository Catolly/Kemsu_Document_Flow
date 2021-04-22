<template>

	<nav class="app-filter-nav">

    <!-- change NuxtLink to app-button with icon attribute -->
  	<NuxtLink
		to="#"
		class="back-link">
			<icon-arrow-back class="active"/>
		</NuxtLink>

    <!-- change NuxtLink to app-button with icon attribute -->
  	<NuxtLink
		to="#"
		class="next-link">
			<icon-arrow-next/>
		</NuxtLink>

  	<span class="filter-body">
			{{filterNamesBody}}
      <span class="filter-head">{{filterNamesHead}}</span>
		</span>

  </nav>

</template>

<script>
import IconArrowBack from '~/components/icons/IconArrowBack'
import IconArrowNext from '~/components/icons/IconArrowNext'

export default {
	name: "AppFilterNav",

	components: {
		IconArrowBack,
		IconArrowNext,
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

// change style
.app-filter-nav {
  margin-top: 16px;

  .back-link:after,
  .next-link:after {
  	display: none;
  }

  .back-link {
  	margin-right: 14px;
  }

  .next-link {
  	margin-right: 28px;
  }

  .filter-body {
  	color: @text-grey;
  	font-size: @fz-small;
    font-weight: @fw-normal;
  }

  .filter-head {
  	color: #000;
  }
}

</style>
