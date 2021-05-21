<template>
  <div
    class="app-schema-body"
  >
    <div class="point-list-wrapper">
      <app-list
        :gap="8"
        class="point-list"
      >
        <app-list-item
          v-for="point in points"
          :key="point.title"
          :class="{'selected': point === selected}"
          class="point"
          @click="selected = point"
        >
          {{ point.title }}
        </app-list-item>
      </app-list>
    </div>

    <div class="selected-info">
      <span v-if="selected.description" class="description">
        {{ selected.description }}
      </span>

      <div class="required-documents-wrapper">
        <div class="required-documents">
          <img
            v-for="doc in selected.requiredDocuments"
            :key="doc.img"
            :src="doc.img"
            :title="doc.title"
            class="document-img"
          >
        </div>
      </div>

      <NuxtLink
        :to="URL + id + '?step=2'"
        class="edit-link"
      >
        Список студентов
      </NuxtLink>
    </div>
  </div>
</template>

<script>
import { copy } from '~/store/methods'

import AppList from '~/components/common/AppList'
import AppListItem from '~/components/common/AppListItem'

export default {
  name: 'AppSchemaBody',

  components: {
    AppList,
    AppListItem,
  },

  data:() => ({
    selected: null,
  }),

  props: {
    URL: {
      type: String,
      required: true,
    },

    id: {
      type: String | Number,
      required: true,
    },

    points: {
      type: Array,
      required: true,
    },
  },

  methods: {
    copy(state) {
      return copy(state)
    },
  },

  beforeMount() {
    if (this.points.length)
      this.selected = this.points[0]
  },
}
</script>

<style lang="less" scoped>
.app-schema-body {
  width: 100%;

  padding: 48px;
  padding-top: 24px;

  cursor: auto;
  background: @white;

  display: grid;
  grid-template-columns: 4fr 1fr 9fr;
  grid-template-areas: "point-list . selected-info";
}

.point-list-wrapper {
  height: auto;
  min-height: 16em;

  position: relative;
}

.point-list {
  height: inherit;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;

  grid-area: point-list;

  grid-template-rows: auto 1fr;
  overflow-y: auto;
}

.point {
  height: fit-content;
  padding: 20px 28px;

  border-radius: 5px;
}

.selected {
  &,
  &:hover {
    color: @green;
    border-color: @green;
  }
}

.selected-info {
  height: fit-content;

  grid-area: selected-info;

  display: grid;
  grid-template-columns: 1fr max-content;
  grid-row-gap: .5em;
  grid-column-gap: 1em;
  grid-template-areas:
    "description edit-link"
    "required-documents .";
}

.description {
  grid-area: description;

  font-size: @fz-large;
  line-height: 160%;
}

.required-documents {
  grid-area: required-documents;

  align-self: flex-end;
  display: flex;
  flex-flow: wrap;
  gap: 8px;
}

.document-img {
  height: 45px;
  width: 45px;

  background-color: @grey-darkset;
}

.edit-link {
  grid-area: edit-link;

  align-self: flex-start;

  font-size: @fz-large;
  font-weight: @fw-medium;

  color: @black;
  &:after {
    border-color: @black;
  }
}
</style>
