<template>
  <app-list class="app-sign-point-list">

    <app-list-item
      v-for="(point, index) in pointList"
      :key="index"
      class="point simple"
    >
      <!-- emit check -->
      <app-checkbox
        v-model="point.checked"
      />
      <div class="owner-info">
        <span class="owner-fullname">
          {{point.owner.fullName}}
        </span>
        <span class="owner-status">
          {{point.owner.status}}
        </span>
      </div>

      <div class="sign-btns">
        <div
          v-if="point.status != 'reviewing'"
          class="signer-fullname"
        >
          <span>
            {{point.status === 'signed' ? 'Подписал' : 'Отказал'}}
            <br>
            {{point.signer.fullName}}
          </span>
        </div>

        <app-button
          v-if="point.status != 'signed'"
          class="btn sign green"
          @click="$emit('sign', point)"
        >
          Подписать
        </app-button>


        <app-button
          v-if="point.status != 'rejected'"
          :class="point.status === 'reviewing' ? 'red' : 'cancel'"
          class="btn reject"
          @click="$emit('reject', point)"
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
    pointList: {
      type: Array,
      default: () => [],
    },
  },
}
</script>

<style lang="less" scoped>
.app-sign-point-list {
  margin-top: 32px;

  .point {
    display: flex;
    justify-content: flex-end;
    align-items: center;

    .owner-info {
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

    .owner-status,
    .signer-fullname {
      color: @text-grey;
    }

    .signed-staff,
    .rejected-staff {
      margin-right: 10px;
    }
  }
}

</style>
