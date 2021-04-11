<template>
  <icon-base
  width="24"
  height="24"
  class="icon-search">
    <rect x="0.5" y="0.101074" width="24" height="24" fill="url(#pattern0)"/>
    <defs>
      <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
        <use xlink:href="#image0" transform="scale(0.01)"/>
      </pattern>
      <image id="image0" width="100" height="100" xlink:href="data:image/png;base64,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"/>
    </defs>
  </icon-base>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
  name: 'IconSearch',
  components: {
    IconBase
  }
}
</script>

<style></style>
