<template>
  <app-list class="student-list">
    <app-list-item
      v-for="(student, index) in studentList"
      :key="index"
      class="student"
    >
      <div class="student-info">
        <span class="fullname">{{student.fullname}}</span>
        <span class="about">
          {{student.institute}},
          {{student.group}},
          {{student.courseNumber}} курс
        </span>
        <span
          v-for="(bypassSheet, index) in student.sheets"
          :key="index"
          :class="{'signed': bypassSheet.status === bypassSheetSchema.Signed}"
          class="bypass-sheets-status"
        >
          Обходной лист
          "{{bypassSheet.name}}"
          {{bypassSheet.status === bypassSheetSchema.Signed ? '' : ' не '}}
          подписан
        </span>
      </div>

      <app-button
        red
        @click="student.isActive ? ban(student) : unban(student)"
      >
        Заблокировать аккаунт
      </app-button>
    </app-list-item>
  </app-list>
</template>

<script>
import {
  BAN_USER,
  UNBAN_USER,
} from "~/store/actions.type"

import bypassSheetSchema from '~/services/bypassSheetSchema'

import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppCheckbox from '~/components/common/AppCheckbox'
import AppButton from '~/components/common/AppButton'
import AppDownloadList from '~/components/common/AppDownloadList'

export default {
  name: 'AppStudentList',

  components: {
    AppList,
    AppListItem,
    AppCheckbox,
    AppButton,
    AppDownloadList,
  },

  data:() => ({
    banError: '',
    unbanError: '',
  }),

  props: {
    studentList: {
      type: Array,
      default: () => [],
    },
  },

  computed: {
    bypassSheetSchema() {
      return bypassSheetSchema
    },
  },

  methods: {
    async ban(user) {
      this.banError = ''
      try {
        await this.$store.dispatch(BAN_USER, user.id)
        user.isActive = false
      } catch (error) {
        console.error(error)
        this.banError = error
      }
    },

    async unban(user) {
      this.unbanError = ''
      try {
        await this.$store.dispatch(UNBAN_USER, user.id)
        user.isActive = true
      } catch (error) {
        console.error(error)
        this.unbanError = error
      }
    },
  },
}
</script>

<style lang="less" scoped>
.student {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.student-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .about {
    color: @grey-darkset;
  }
}

.bypass-sheets-status {
  font-size: @fz-small;
  color: @grey-darkset;
  &.signed {
    color: @green;
  }
}
</style>
