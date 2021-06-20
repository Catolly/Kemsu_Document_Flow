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
        class="checkbox"
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
          v-if="student.point"
          :files="student.point.uploadedDocuments"
          class="student-documents"
        />
      </div>

      <div v-if="student.point.deadline" class="deadline">
        Срок заполнения:
        <br>
        до {{student.point.deadline}}
      </div>

      <div v-if="student.point" class="sign-btns">
        <div
          v-if="[
            bypassSheetStatus.Signed,
            bypassSheetStatus.Rejected
          ].includes(student.point.status)"
          class="staff"
        >
          <span>
            {{student.point.status === bypassSheetStatus.Signed ? 'Подписал' : 'Отказал'}}
            <br>
            {{staffShortname(student.point.staff)}}
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
  name: 'AppStudentList',

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
      required: true,
    },
  },

  computed: {
    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },

  methods: {
    staffShortname(staff) {
      const [firstname, lastname, middlename] = staff.split(' ')
      return firstname + ' ' + lastname[0] + '.' + (middlename ? middlename[0] + '.' : '')
    },
  }
}
</script>

<style lang="less" scoped>
.student {
  display: flex;
  justify-content: flex-start;
  align-items: center;

  position: relative;

  padding-top: 24px;
  padding-bottom: 24px;
}

.checkbox {
  flex-shrink: 0;
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

.deadline {
  flex-shrink: 0;
  margin: 0 .5em;
  max-width: 120px;
  line-height: 135%;

  font-size: @fz-small;
  color: @grey-darkset;
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
