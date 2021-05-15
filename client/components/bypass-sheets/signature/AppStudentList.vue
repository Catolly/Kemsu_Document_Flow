<template>
  <app-list class="app-student-list">

    <app-list-item
      v-for="(student, index) in studentList"
      :key="index"
      class="student simple"
    >
      <!-- emit check -->
      <app-checkbox
        v-model="student.checked"
      />
      <div class="student-info">
        <span class="student-fullname">
          {{student.fullName}}
        </span>
        <span class="student-status">
          {{student.groupName}},
          {{student.courseNumber}}.
          {{student.educationForm}}.
          {{student.status}}
        </span>
      </div>

      <div class="sign-btns">
        <div
          v-if="student.point.status != 'reviewing'"
          class="staff"
        >
          <span>
            {{student.point.status === 'signed' ? 'Подписал' : 'Отказал'}}
            <br>
            {{student.point.staffName}}
          </span>
        </div>

        <app-button
          v-if="student.point.status != 'signed'"
          class="btn sign green"
          @click="$emit('sign', student)"
        >
          Подписать
        </app-button>


        <app-button
          v-if="student.point.status != 'rejected'"
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
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'
import AppCheckbox from '~/components/common/AppCheckbox'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppSignPointList',

  components: {
    AppList,
    AppListItem,
    AppCheckbox,
    AppButton,
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
.app-student-list {
  margin-top: 32px;

  .student {
    display: flex;
    justify-content: flex-end;
    align-items: center;

    .student-info {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: flex-start;

      margin-left: 24px;
    }

    .sign-btns {
      display: flex;
      justify-content: flex-end;
      margin-left: auto;

      & .btn:last-child {
        margin-left: 10px;
      }
    }

    .student-status,
    .staff {
      color: @text-grey;
    }

    .signed-staff,
    .rejected-staff {
      margin-right: 10px;
    }
  }
}

</style>
