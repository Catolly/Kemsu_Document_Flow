<template>
  <div class="contacts">
    <div class="contacts-head">
      <h1 class="header">Контакты</h1>
      <span
        v-if="loadError"
        class="error-message"
      >
        Не удалось загрузить контакты
      </span>
    </div>

    <div
      v-for="(department, index) in allDepartments"
      :key="index"
      class="department"
    >
      <div class="department-head">
        <span v-if="department.staff.length" class="department-title">
          {{
            (department.title
            + (department.institute ? (' ' + department.institute) : ''))
              .toUpperCase()
          }}
        </span>
        <span v-if="department.staff.length" class="department-address">
          Адрес: {{department.address}}
        </span>
      </div>
      <div class="contacts-body">
        <div
          v-for="(staff, index) in department.staff"
          :key="index"
          class="contact"
        >
          <span class="contact-name">{{staff.fullname}}</span>
          <span class="contact-email">{{staff.email}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { FETCH_ALL_DEPARTMENTS } from "~/store/actions.type"

export default {
  name: 'settings',

  middleware: 'authenticated',

  data:() => ({
    loadError: false,

    contacts: [],
  }),

  async beforeMount() {
    const currentUser = this.$store.getters.currentUser
    try {
      await this.$store
        .dispatch(FETCH_ALL_DEPARTMENTS)
    } catch (error) {
      console.error(error)
      this.loadError = error
    }
  },

  computed: {
    ...mapGetters(['allDepartments', 'currentUser']),
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
  padding-top: 3em;
  gap: 3em;
}

.contacts-head {
  gap: .5em;
}

.department {
  display: grid;
  grid-template-rows: repeat(auto, 1fr);
  grid-template-columns: minmax(200px, 270px) 1fr;
  grid-gap: 1em;
}

.department-head {
  display: flex;
  flex-direction: column;
  gap: .5em;

  font-size: @fz-large;
  font-weight: @fw-light;
  color: @grey-darkset;
}

.department-address {
  font-size: @fz-small;
}

.contacts-body {
  display: grid;
  grid-template-rows: repeat(auto, 1fr);
  grid-template-columns: repeat(2, minmax(min-content, 400px));
  grid-auto-flow: row dense;
  grid-gap: 1.5em;
}

.contact {
  gap: .5em;

  &-name {
    font-weight: @fw-normal;
    font-size: @fz-large;
  }
}

@media all and (max-width: 1300px) {
  .department {
    display: grid;
    grid-template-rows: repeat(auto, 1fr);
    grid-template-columns: 1fr;
    grid-gap: 1.5em;
  }

  .department-head {
    max-width: 350px;
  }
}

@media all and (max-width: 1000px) {
  .contacts-body {
    grid-template-columns: 1fr;
  }
}
</style>
