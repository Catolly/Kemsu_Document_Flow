<template>
  <app-list class="app-student-list">
    <app-list-item
      v-for="(student, index) in studentList"
      :key="index"
      class="student simple"
    >
      <app-checkbox
        :value="student.checked"
        @input="student.checked ? $emit('uncheck', student) : $emit('check', student)"
      />
      <div class="student-info">
        <span class="student-fullname">
          {{student.fullname}}
        </span>
        <span class="student-status">
          {{student.institute ? `${student.institute}, ` : ''}}
          {{student.group ? `${student.group}, ` : ''}}
          {{student.courseNumber ? `${student.courseNumber} курс` : ''}}
        </span>
      </div>
    </app-list-item>
  </app-list>
</template>

<script>
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppCheckbox from '~/components/common/AppCheckbox'
import AppButton from '~/components/common/AppButton'
import AppDownloadList from '~/components/common/AppDownloadList'

export default {
  name: 'AppPointList',

  components: {
    AppList,
    AppListItem,
    AppCheckbox,
    AppButton,
    AppDownloadList,
  },

  props: {
    studentList: {
      type: Array,
      default: () => [],
    },
  },
}
</script>

<style lang="less" scoped>
.student {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 24px;
}

.student-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.student-status {
  color: @text-grey;
}
</style>
