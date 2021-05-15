<template>
  <div class="contacts">
    <div class="contacts-head">
      <h1 class="header">Личные данные</h1>
      <span
        v-if="loadError"
        class="error-message"
      >
        Не удалось загрузить контакты
      </span>
    </div>

    <div class="contacts-body">
      <div
        v-for="(contact, index) in currentDepartment.contacts"
        :key="index"
        class="contact"
      >
        <span class="contact-name">{{contact.fullname}}</span>
        <span class="contact-email">{{contact.email}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { FETCH_DEPARTMENT } from "~/store/actions.type"

export default {
  name: 'settings',

  data:() => ({
    loadError: false,

    // Удалить позже
    currentDepartment: {
      contacts: [
        {
          fullname: 'Иванов Иван Иванович',
          email: 'example@example.com',
        },
        {
          fullname: 'Иванов Иван Иванович',
          email: 'example@example.com',
        },
        {
          fullname: 'Иванов Иван Иванович',
          email: 'example@example.com',
        },
      ],
    },
    //
  }),

  computed: {
    // ...mapGetters(['currentDepartment, currentUser']),

    // удалить позже
    currentUser() {
      return {
        department: 'Библиотека',
      }
    },
    //
  },

  created() {
    this.$store
      .dispatch(FETCH_DEPARTMENT, {
        department: this.currentDepartment,
        institute: this.currentUser.institute,
      })
      .catch(error => this.loadError = error)
  },
}
</script>

<style scoped lang="less">
.contacts,
.contacts-head,
.contact {
  display: flex;
  flex-direction: column;
}

.contacts {
  padding-top: 48px;
  gap: 48px;
}

.contacts-head {
  gap: 8px;
}

.contacts-body {
  display: grid;
  grid-template-rows: repeat(auto, 1fr);
  grid-template-columns: repeat(3, minmax(min-content, 360px));
  grid-auto-flow: row dense;
  grid-gap: 24px;
}

.contact {
  gap: 8px;

  &-name {
    font-weight: @fw-normal;
    font-size: @fz-large;
  }
}

.error-message {
  color: @red;
}

@media all and (max-width: 1250px) {
  .contacts-body {
    grid-template-columns: repeat(2, minmax(min-content, 360px));
  }
}

@media all and (max-width: 1000px) {
  .contacts-body {
    grid-template-columns: repeat(1, minmax(min-content, 360px));
  }
}
</style>
