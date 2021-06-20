<template>
  <table class="app-deadlines-table">
    <colgroup>
      <col class="col-first">
      <col class="col-second">
    </colgroup>

    <tr class="row header">
      <th class="item">Группа</th>
      <th class="item">Крайняя дата подписания</th>
    </tr>

    <tr
      v-for="(group, index) in groups"
      :key="index"
      class="row"
    >
      <!-- group.name -->
      <td class="item">
        <b>{{group.groupName}}</b>
      </td>
      <td class="item">
        <app-input
          :placeholder="'число/месяц/год'"
          :value="group.deadline"
          @input="inputGroupDeadline(group, $event, $el)"
          class="date-input"
        />
      </td>
    </tr>
  </table>
</template>

<script>
import AppSelect from '~/components/common/AppSelect'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppDeadlinesTable',

  components: {
    AppSelect,
    AppInput,
  },

  props: {
    groups: {
      type: Array,
      required: true,
    }
  },

  methods: {
    inputGroupDeadline(group, value, el) {
      group.deadline = this.formateDate(value)
      el.value = group.deadline
      el.dispatchEvent(new Event('input'))
    },

    // formate - dd/mm/yyyy
    formateDate(value) {
      value = value.trim()

      if (value.length === 2 || value.length === 5)
        value += '/'

      return value.substring(0, 10)
    },
  },
}
</script>

<style scoped lang="less">
.app-deadlines-table {
  border-collapse: collapse;

  .col-first {
    width: 50%;
  }

  .date-input {
    min-width: 350px;
  }

  .row {
    text-align: left;
  }

  .row.header {
    .item {
      padding-bottom: 1em;
    }
  }

  .item {
    padding: .5em;
    padding-left: 0;

    font-size: @fz-large;
  }
}
</style>
