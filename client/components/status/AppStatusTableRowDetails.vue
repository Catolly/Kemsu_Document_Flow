<template>
  <div class="app-status-table-row-details">
    <template v-if="sheet">
      <div v-if="signedPointsTitles.length" class="item green">
        <div class="header">
          <b>Подписано</b>
        </div>
        <div
          v-for="title in signedPointsTitles"
          :key="title"
        >
          {{title}}
        </div>
      </div>

      <div v-if="rejectedPointsTitles.length" class="item red">
        <div class="header">
          <b>Отказано</b>
        </div>
        <div
          v-for="title in rejectedPointsTitles"
          :key="title"
        >
          {{title}}
        </div>
      </div>

      <div v-if="reviewingPointsTitles.length" class="item grey">
        <div class="header">
          <b>На рассмотрении</b>
        </div>
        <div
          v-for="title in reviewingPointsTitles"
          :key="title"
        >
          {{title}}
        </div>
      </div>

      <div v-if="notSentPointsTitles.length" class="item grey">
        <div class="header">
          <b>Не отправлено</b>
        </div>
        <div
          v-for="title in notSentPointsTitles"
          :key="title"
        >
          {{title}}
        </div>
      </div>
    </template>

    <b v-else>Нет такого обходного листа у студента</b>
  </div>
</template>

<script>
export default {
  name: 'AppStatusTableRowDetails',

  props: {
    sheet: {
      type: Object,
      default: null,
    },

    signedPointsTitles: {
      type: Array,
      default:() => [],
    },

    rejectedPointsTitles: {
      type: Array,
      default:() => [],
    },

    reviewingPointsTitles: {
      type: Array,
      default:() => [],
    },

    notSentPointsTitles: {
      type: Array,
      default:() => [],
    },
  },
}
</script>

<style lang="less" scoped>
.app-status-table-row-details {
  padding-left: 1em;
  border-left: 1px solid @grey-darkset;

  display: flex;
  flex-direction: column;
  gap: 1em;

  .green {
    color: @green;
  }

  .red {
    color: @red;
  }

  .grey {
    color: @grey-darkset;
  }

  .header {
    margin-bottom: .5em;
  }

  .item {
    font-size: @fz-small;
    font-weight: @fw-normal;
  }
}
</style>
