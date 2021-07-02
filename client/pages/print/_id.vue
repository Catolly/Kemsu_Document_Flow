<template>
  <roleAdminStaff class="container">
    <div class="university-title">
      <b>ФБГОУ ВО «Кемеровский Государственный Университет» КемГУ</b>
    </div>

    <div class="label">Обходной лист</div>

    <template v-if="sheet">
      <div class="points">
        <div
          v-for="(point, index) in points"
          :key="index"
          class="point"
        >
          <div class="point-index-title">
            <div class="point-index">{{index + 1}}.</div>
            <div class="point-title">{{point.title}}</div>
          </div>
          <div class="point-value">{{point.value}}</div>
        </div>
      </div>

      <div class="staff-initials">
        {{currentUser.department}} ______________ / ______________
      </div>
    </template>

    <div class="date">{{currentDate}}</div>
  </roleAdminStaff>
</template>

<script>
import { UsersService } from '~/services/ApiService'
import bypassSheetStatus from '~/services/bypassSheetStatus'

import { mapGetters } from 'vuex'

import roleAdminStaff from '~/components/roles/roleAdminStaff'

export default {
  name: 'print',

  // layout: 'printLayout',

  components: {
    roleAdminStaff,
  },

  data:() => ({
    user: null,
    sheet: null,
  }),

  computed: {
    ...mapGetters(['currentUser']),

    currentDate() {
      return new Date(Date.now()).toLocaleString().split(',')[0]
    },

    userId() {
      return this.$route.params.id
    },

    sheetName() {
      return this.$route.query.name
    },

    points() {
      const points = this.sheet.points
        .map(point => ({
          title: point.title,
          value: point.status === bypassSheetStatus.Signed
            ? 'Одобрено'
            : 'Не одобрено',
        }))

      points.unshift(...[
        {
          title: 'ФИО',
          value: this.user.fullname
        },
        {
          title: this.user.institute,
          value: `Группа ${this.user.group}`
        }
      ])

      return points
    },
  },

  methods: {
    print() {
      setTimeout(window.print, 600)
    },

    getUser() {
      return UsersService.getById(this.userId)
    },
  },

  async beforeMount() {
    const { data } = await this.getUser()
    this.user = data
    this.sheet = this.user.bypassSheets
      .find(sheet => sheet.title === this.sheetName)
    this.print()
  },
}
</script>

<style scoped lang="less">
.container {
  * {
    font-family: Roboto;
    text-align: center;
  }

  display: flex;
  flex-direction: column;
  margin: auto;

  height: 210mm;
  width: 297mm;
  padding: 10mm 15mm;

  .university-title {
    margin-top: 5mm;
    font-size: 32px;
  }

  .label,
  .point,
  .staff-initials,
  .date {
    font-weight: 400;
  }

  .label {
    margin-top: 10mm;
    font-size: 28px;
  }

  .points {
    margin-top: 20mm;

    display: flex;
    flex-direction: column;
    line-height: 2em;
  }

  .point {
    display: flex;
    gap: 10px;

    &:not(:first-child) {
      justify-content: space-between;
    }

    font-size: 20px;
    * {
      text-align: left;
      word-break: break-word;
    }

    &-index-title {
      display: flex;
    }

    &-index {
      min-width: 10mm;
    }

    &-value {
      min-width: 85mm;
    }
  }

  .staff-initials {
    margin-top: 30mm;
    margin-right: 25mm;
    font-size: 24px;
    text-align: right;
  }

  .date {
    margin-top: 10mm;
    font-size: 24px;
    text-align: right;
  }
}
</style>
