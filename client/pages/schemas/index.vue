<template>
  <roleAdmin class="container">
    <h1 class="header">Обходные листы</h1>

    <p
      v-if="loadError"
      class="error-message"
    >
      Не удалось загрузить обходные листы
    </p>

    <div class="topbar">
      <NuxtLink
        to="new"
        append
        class="clear"
      >
          <app-button blue filled class="create-btn">Добавить</app-button>
      </NuxtLink>
      <app-search
        round
        small
        class="search"
        v-model="searchText"
      />
    </div>

    <app-pagination
      v-show="schemas.length > 0"
      :itemsAmount="schemas.length"
      :page="page"
      @updateItemsPerPage="itemsPerPage = $event"
      @updatePage="page = $event"
      class="pagination"
    />

    <h2
      v-if="!loadError && !schemas.length"
      class="empty-schema-list-message"
    >
      Список обходных листов пуст. Создайте первый
    </h2>

    <app-list class="schema-list">
      <app-schema
        v-for="(schema, index) in schemasInPage"
        :key="index"
        :schema="schema"
        :URL="$nuxt.$route.path + '/'"
        class="schema"
        @edit="edit"
      />
    </app-list>

    <h2
      v-if="!loadError && schemas.length && !schemasInPage.length"
      class="empty-search-message"
    >
      Нет результатов
    </h2>
  </roleAdmin>
</template>

<script>
import { mapGetters } from "vuex"
import { FETCH_BYPASS_SHEETS_SCHEMAS } from "~/store/actions.type"

import roleAdmin from '~/components/roles/roleAdmin'

import AppButton from '~/components/common/AppButton'
import AppSearch from '~/components/common/AppSearch'
import AppList from '~/components/common/AppList'
import AppSchema from '~/components/schemas/AppSchema'
import AppPagination from '~/components/common/AppPagination'

export default {
  name: 'index',

  middleware: 'authenticated',

  components: {
    roleAdmin,
    AppButton,
    AppSearch,
    AppList,
    AppSchema,
    AppPagination,
  },

  data:() => ({
    searchText: '',

    loadError: '',
    itemsPerPage: 0,
    page: 0,

    // bypassSheetsSchemas: [
    //   {
    //     id: 0,
    //     title: 'Скидка на столовую',
    //     educationForm: 'Очная',
    //     points: [
    //       {
    //         title: 'Пункт 1',
    //         description: "Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта.",
    //         requiredDocuments: [],
    //         gender: 'Мужской',
    //         studentUploadDocuments: [
    //           { title: 'Фото/скан паспорта', },
    //           { title: 'Заполненный документ', },
    //         ],
    //       },
    //       {
    //         title: 'Пункт 2',
    //         description: "Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта. Сообщение, содержащее указания для определённого пункта.",
    //         requiredDocuments: [],
    //         gender: 'Не указывать',
    //         studentUploadDocuments: [],
    //       },
    //       {
    //         title: 'Пункт 3',
    //         description: '',
    //         requiredDocuments: [],
    //         gender: '',
    //         studentUploadDocuments: [],
    //       },
    //       {
    //         title: 'Пункт 4',
    //         description: '',
    //         requiredDocuments: [],
    //         gender: '',
    //         studentUploadDocuments: [],
    //       },
    //       {
    //         title: 'Пункт 5',
    //         description: '',
    //         requiredDocuments: [],
    //         gender: '',
    //         studentUploadDocuments: [],
    //       },
    //     ],
    //   },
    //   {
    //     id: 1,
    //     title: 'Отчисление',
    //     educationForm: 'Очная',
    //     points: [
    //       {
    //         title: 'Пункт 1',
    //         description: '',
    //         requiredDocuments: [],
    //       },
    //     ],
    //   },
    // ],
  }),

  computed: {
    ...mapGetters(['bypassSheetsSchemas']),

    schemasInPage() {
      return this.searchingSchemas
      .slice(
        this.page * this.itemsPerPage,
        (this.page + 1) * this.itemsPerPage
      )
    },

    searchingSchemas() {
      if (!this.searchText) return this.schemas

      return this.schemas.filter(schema =>
        schema.title.includes(this.searchText))
    },

  methods: {
    edit(id) {
      this.$router.push($nuxt.$route.path + '/' + id)
    },
  },

  beforeMount() {
    this.$store
      .dispatch(FETCH_BYPASS_SHEETS_SCHEMAS, {
        bypassSheetsSchemas: this.bypassSheetsSchemas
      })
      .catch(error => this.loadError = error)
  },
}
</script>

<style lang="less" scoped>

.container {
  margin-top: 48px;

  display: flex;
  flex-direction: column;
  gap: 32px;
}

.topbar {
  display: flex;
  justify-content: space-between;
}

.search {
  max-width: 340px;
}

.pagination {
  margin-left: auto;
}

.error-message {
  color: @red;
}
</style>
