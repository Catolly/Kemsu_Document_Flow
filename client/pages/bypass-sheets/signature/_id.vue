<template>
  <div class="container">
    <h1 class="header">{{title}}</h1>
    <app-group-nav class="app-group-nav mt-4" />
    <div class="topbar">
      <app-button class="btn green filled">Подписать (3)</app-button>
      <app-button class="btn">Выбрать всех</app-button>
      <app-button class="btn">Снять выбор</app-button>
      <app-input id="input" class="input round search" />
    </div>
    <app-list	class="student-list">
      <app-list-item>
      </app-list-item>
    </app-list>
  </div>
</template>

<script>
import AppGroupNav from '~/components/common/AppGroupNav'
import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'

export default {
  components: {
    AppGroupNav,
    AppButton,
    AppInput,
    AppList,
    AppListItem,
  },
  data() {
    return {
      title: 'Скидка на столовую',
    }
  },
}
</script>

<style lang="less" scoped>

.header {
  margin-top: 48px;
}

// .app-group-nav {
//   margin-top: 16px;
// }

.topbar {
  margin-top: 48px;

  display: flex;

  .btn {
    margin-right: 18px;

    &:first-child {
      margin-right: 24px;

    }
  }

  .input {
    width: 340px;
    height: 50px;

    padding: 0;
    margin: 0;
    margin-left: auto;
  }
}

.student-list {
  margin-top: 32px;
}

</style>
