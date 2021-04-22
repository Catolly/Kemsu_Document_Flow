<template>
	<div class="icon-logo">
    <icon-base
    :height="height"
    :width="width"
    class="icon-logo-img">
      <g :transform="`translate(0.000000,${height}) scale(${0.1 * width/202},-${0.1 * height/202})`"
      fill="#000000" stroke="none">
        <path d="M400 1980 c0 -22 -9 -69 -21 -103 -51 -154 -168 -252 -329 -273 l-50
        -7 0 -143 0 -144 43 0 c56 0 158 25 209 51 23 12 65 44 95 72 l53 50 0 -592 0
        -591 -200 0 -200 0 0 -150 0 -150 550 0 550 0 0 150 0 150 -200 0 -200 0 0
        860 0 860 -150 0 -150 0 0 -40z"/>
        <path d="M1673 1999 c-133 -42 -250 -170 -282 -309 -6 -25 -11 -103 -11 -175
        0 -118 -3 -135 -26 -185 -14 -30 -37 -68 -52 -83 -34 -37 -105 -73 -159 -82
        l-43 -7 0 -138 0 -138 43 -7 c54 -9 125 -45 159 -82 15 -15 38 -53 52 -83 24
        -50 26 -66 26 -192 0 -75 5 -161 11 -190 26 -122 119 -238 237 -294 43 -21 77
        -29 140 -32 l82 -5 0 142 0 141 -49 0 c-52 0 -98 27 -123 74 -7 12 -15 94 -19
        191 -4 114 -12 187 -23 222 -22 70 -92 170 -147 212 -24 18 -44 37 -44 41 0 4
        20 23 44 41 56 42 125 143 147 212 10 33 19 109 23 207 4 85 13 165 19 176 25
        47 71 74 123 74 l49 0 0 145 0 145 -57 -1 c-32 0 -86 -9 -120 -20z"/>
      </g>
    </icon-base>
	</div>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
  name: 'IconLogo',
  components: {
    IconBase
  },
  data() {
    return {
      height: 58,
      width: 52,
    }
  }
}
</script>

<style lang="less" scoped>

.icon-logo {
	height: 66px;
  width: 42px;

  &.big {
  	height: 86px;
  	width: 54px;
  }
}

.icon-logo-img {
  height: 100%;
  width: 100%;
}

</style>
