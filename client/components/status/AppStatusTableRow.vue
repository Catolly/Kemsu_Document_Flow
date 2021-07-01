<template>
  <div class="app-status-table-row">
    <div class="item">
      <b>{{user.fullname}}</b>
    </div>

    <div class="item">
      {{user.group}}
    </div>

    <div class="item green">
      {{signedPoints.length || '—'}}
    </div>

    <div class="item red">
      {{rejectedPoints.length || '—'}}
    </div>

    <div class="item grey">
      {{reviewingPoints.length || '—'}}
    </div>

    <div class="item grey">
      {{notSentPoints.length || '—'}}
    </div>

    <div class="item">
      <app-button
        blue
        plain
        class="print-btn"
      >
        Распечатать
      </app-button>
    </div>

    <div class="item">
      <app-button
        plain
        class="toggle-details-btn"
        @click="toggleDetails"
      >
        <div v-if="!isOpen" class="plus" />
        <div v-else class="minus" />
      </app-button>
    </div>

    <app-status-table-row-details
      v-show="isOpen"
      :sheet="sheet"
      :signedPointsTitles="signedPointsTitles"
      :rejectedPointsTitles="rejectedPointsTitles"
      :reviewingPointsTitles="reviewingPointsTitles"
      :notSentPointsTitles="notSentPointsTitles"
      class="details"
    />
  </div>
</template>

<script>
import bypassSheetStatus from '~/services/bypassSheetStatus'

import AppStatusTableRowDetails from '~/components/status/AppStatusTableRowDetails'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppStatusTableRow',

  components: {
    AppStatusTableRowDetails,
    AppButton,
  },

  data:() => ({
    isOpen: false,
  }),

  props: {
    user: {
      type: Object,
      required: true,
    },

    schemaTitle: {
      type: String,
      default: '',
    },
  },

  computed: {
    sheet() {
      return this.user
        .bypassSheets
        .find(sheet => sheet.title === this.schemaTitle)
    },

    points() {
      return this.sheet ? this.sheet.points : []
    },

    signedPoints() {
      return this.points
        .filter(point =>
          point.status === this.bypassSheetStatus.Signed)
    },

    rejectedPoints() {
      return this.points
        .filter(point =>
          point.status === this.bypassSheetStatus.Rejected)
    },

    reviewingPoints() {
      return this.points
        .filter(point =>
          point.status === this.bypassSheetStatus.Reviewing || (
            point.status === this.bypassSheetStatus.NotSent &&
            !point.requiredDocuments.length
          )
        )
    },

    notSentPoints() {
      return this.points
        .filter(point =>
          point.status === this.bypassSheetStatus.NotSent &&
          point.requiredDocuments.length
        )
    },

    signedPointsTitles () {
      return this.signedPoints
        .map(point => point.title)
    },

    rejectedPointsTitles () {
      return this.rejectedPoints
        .map(point => point.title)
    },

    reviewingPointsTitles () {
      return this.reviewingPoints
        .map(point => point.title)
    },

    notSentPointsTitles () {
      return this.notSentPoints
        .map(point => point.title)
    },

    bypassSheetStatus() {
      return bypassSheetStatus
    },
  },

  methods: {
    toggleDetails() {
      this.isOpen = !this.isOpen
    },
  },
}
</script>

<style scoped lang="less">
.app-status-table-row {
  .green {
    color: @green;
  }

  .red {
    color: @red;
  }

  .grey {
    color: @grey-darkset;
  }

  .item {
    padding: 0 .5em;

    &:first-child {
      padding-left: 0;
    }

    align-self: center;

    font-size: @fz-large;
    font-weight: @fw-normal;
    line-height: 135%;

    position: relative;
  }

  .toggle-details-btn {
    width: 40px;
    height: 60px;

    .plus {
      .plus();
    }

    .minus {
      .minus();
    }
  }

  .details {
    grid-column: 1/-1;
    margin: .5em 0;
  }
}

@media all and (max-width: 900px) {
  .app-status-table-row {
    .item,
    .print-btn /deep/ * {
      font-size: @fz-small;
    }
  }
}
</style>
