<template>
  <div class="container">

    <h1 class="header">{{title}}</h1>

    <app-group-nav class="app-group-nav" />

    <app-sign-topbar
      :checkedPointsCount="checkedPointList.length"
      @signChecked="signChecked"
      @checkAll="checkAll"
      @uncheckAll="uncheckAll"
      @search="search"
    />

  </div>
</template>

<script>
import AppGroupNav from '~/components/common/AppGroupNav'
import AppSignTopbar from '~/components/bypass-sheets/signature/AppSignTopbar'

export default {

  components: {
    AppGroupNav,
    AppSignTopbar,
  },

  data:() => ({
    title: 'Скидка на столовую',

    searchText: '',

    pointList: [
      {
        id: 1893,
        checked: false,
        status: 'reviewing',
        owner: {
          id: 10342,
          fullName: 'Люкшин Михаил Сергеевич',
          status: 'Бюджет, учится',
        },
        signer: {
          fullName: 'Иванов И.И.',
        },
      },
      {
        id: 1894,
        checked: false,
        status: 'signed',
        owner: {
          id: 10343,
          fullName: 'Сергиенко Анатолий Николаевич',
          status: 'Бюджет, учится',
        },
        signer: {
          fullName: 'Иванов И.И.',
        },
      },
      {
        id: 1894,
        checked: false,
        status: 'rejected',
        owner: {
          id: 10343,
          fullName: 'Панчук Роман Олегович',
          status: 'Бюджет, учится',
        },
        signer: {
          fullName: 'Иванов И.И.',
        },
      },
    ],
  }),

  computed: {
    checkedPointList: function() {
      return this.pointList.filter(point => point.checked)
    },
  },

  methods: {

    // Методы app-sign-topbar
    signChecked() {
      this.checkedPointList.forEach(this.sign)
    },
    checkAll() {
      this.pointList.forEach(this.check)
    },
    uncheckAll() {
      this.pointList.forEach(this.uncheck)
    },
    search(searchText) {
      this.searchText = searchText
    },
  },
}
</script>

<style lang="less" scoped>

.header {
  margin-top: 48px;
}

.app-group-nav {
  margin-top: 16px;
}

.student-list {
  margin-top: 32px;
}
</style>
