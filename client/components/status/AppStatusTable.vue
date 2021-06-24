<template>
  <div class="app-status-table">
    <div class="row header">
      <div class="item">
        <b>Студент</b>
      </div>
      <div class="item">
        <b>Группа</b>
      </div>
      <div class="item green">
        <b>Подписано</b>
      </div>
      <div class="item red">
        <b>Отказано</b>
      </div>
      <div class="item grey">
        <b>На рассмотрении</b>
      </div>
      <div class="item grey">
        <b>Не отправлено</b>
      </div>
    </div>

    <app-status-table-row
      v-for="(user, index) in users"
      :key="index"
      :user="user"
      :schemaTitle="schemaTitle"
      class="row"
    />
  </div>
</template>

<script>
import AppStatusTableRow from '~/components/status/AppStatusTableRow'

export default {
  name: 'AppStatusTable',

  components: {
    AppStatusTableRow,
  },

  props: {
    users: {
      type: Array,
      required: true,
    },

    usersAmount: {
      type: Number,
      default: 0,
    },

    schemaTitle: {
      type: String,
      default: '',
    },
  },
}
</script>

<style scoped lang="less">
.app-status-table {
  display: grid;
  grid-template-columns: 100%;
  grid-row-gap: .5em;

  .header {
    padding-bottom: 1em;
  }

  .row {
    display: grid;
    grid-template-columns:
      350px
      repeat(3, 150px)
      repeat(2, 210px)
      60px;
  }

  .item {
    padding: 0 .5em;

    &:first-child {
      padding-left: 0;
    }

    font-size: @fz-large;
    font-weight: @fw-normal;
    line-height: 135%;

    position: relative;

    &.green {
      color: @green;
    }

    &.red {
      color: @red;
    }

    &.grey {
      color: @grey-darkset;
    }
  }
}
</style>
