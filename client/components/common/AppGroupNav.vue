<template>
	<nav class="app-group-nav">
		<NuxtLink
		to="#"
		class="back-link">
			<icon-arrow-back class="active"/>
		</NuxtLink>
		<NuxtLink
		to="#"
		class="next-link">
			<icon-arrow-next/>
		</NuxtLink>
		<span class="group-path">
			Университет 8 / ... / Факультет 6 / <span class="group-name">Группа 5</span>
		</span>
	</nav>
</template>

<script>
import IconArrowBack from '~/components/icons/IconArrowBack'
import IconArrowNext from '~/components/icons/IconArrowNext'

export default {
	name: "AppGroupNav",
	components: {
		IconArrowBack,
		IconArrowNext,
	}
}
</script>

<style scoped lang="less">

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

.group-path {
	color: @text-grey;
	font-size: @fz-small;
  font-weight: @fw-normal;
}

.group-name {
	color: #000;
}

</style>
