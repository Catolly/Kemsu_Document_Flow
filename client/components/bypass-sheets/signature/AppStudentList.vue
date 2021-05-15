<template>
  <app-list class="app-student-list">
    <app-list-item
      v-for="(student, index) in studentList"
      :key="index"
      class="student simple"
    >
      <app-checkbox
        v-model="student.checked"
      />
      <div class="student-info">
        <span class="student-fullname">
          {{student.fullname}}
        </span>
        <span class="student-status">
          {{student.group}},
          {{student.courseNumber}} курс.
          {{student.recruitmentForm}}.
          {{student.status}}
        </span>
        <app-download-list
          :files="student.point.requiredDocuments"
          class="student-documents"
        />
      </div>

      <div class="sign-btns">
        <div
          v-if="student.point.status != bypassSheetStatus.Reviewing"
          class="staff"
        >
          <span>
            {{student.point.status === bypassSheetStatus.Signed ? 'Подписал' : 'Отказал'}}
            <br>
            {{student.point.staff}}
          </span>
        </div>

        <app-button
          v-if="student.point.status != bypassSheetStatus.Signed"
          class="btn sign green"
          @click="$emit('sign', student)"
        >
          Подписать
        </app-button>


        <app-button
          v-if="student.point.status != bypassSheetStatus.Rejected"
          class="btn reject red"
          @click="$emit('reject', student)"
        >
          Отказать
        </app-button>
      </div>
    </app-list-item>
  </app-list>
</template>

<script>
import bypassSheetStatus from '~/services/bypassSheetStatus'

import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppCheckbox from '~/components/common/AppCheckbox'
import AppButton from '~/components/common/AppButton'
import AppDownloadList from '~/components/common/AppDownloadList'

export default {
  name: 'AppSignPointList',

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

  computed: {
    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },
}
</script>

<style lang="less" scoped>
.student {
  display: flex;
  justify-content: flex-end;
  align-items: center;

  position: relative;
}

.student-info {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  margin-left: 24px;
}

.student-documents {
  margin-top: 8px;
}

.sign-btns {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;

  margin-left: auto;
}

.student-status,
.staff {
  color: @text-grey;
}

.staff {
  margin-right: 10px;
}

.signed-staff,
.rejected-staff {
  margin-right: 10px;
}

</style>
