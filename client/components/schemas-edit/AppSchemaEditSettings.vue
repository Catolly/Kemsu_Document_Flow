<template>
  <div class="app-schema-edit-settings-wrapper">
    <div class="app-schema-edit-settings">
      <app-schema-edit-main-settings
        v-if="schema"
        :schema="schema"
        class="edit-main-settings"

        @touch="isInvalidMainSettings = $event"
      />

      <div class="divider" />

      <app-schema-edit-point-list
        v-if="points"
        class="edit-point-list"

        :points="points"
        :selected="selectedPoint"
        @select="selectedPoint = $event"

        @touch="isInvalidPointList = $event"
      />

      <app-schema-edit-point-settings
        v-if="selectedPoint"
        class="edit-point-settings"

        :point="selectedPoint"
        :genderList="genderList"
      />
    </div>

    <div class="nav-btns">
      <NuxtLink
        class="clear"
        tabindex="-1"
        :to="{ path: '..' }"
        append
      >
        <app-button
          cancel
          class="back"
        >
          Отмена
        </app-button>
      </NuxtLink>

      <NuxtLink
        class="clear"
        tabindex="-1"
        :to="{
          path: this.$route.path,
          query: { step: '2' }
        }"
      >
        <app-button
          filled
          blue
          class="next-step"
        >
          Далее
        </app-button>
      </NuxtLink>
    </div>
  </div>
</template>

<script>
import AppSchemaEditMainSettings from '~/components/schemas-edit/AppSchemaEditMainSettings'
import AppSchemaEditPointList from '~/components/schemas-edit/AppSchemaEditPointList'
import AppSchemaEditPointSettings from '~/components/schemas-edit/AppSchemaEditPointSettings'
import AppButton from '~/components/common/AppButton'

export default {
  name: 'AppSchemaEditSettings',

  components: {
    AppSchemaEditMainSettings,
    AppSchemaEditPointList,
    AppSchemaEditPointSettings,
    AppButton,
  },

  props: {
    genderList: {
      type: Array,
      required: true,
    },

    points: {
      type: Array,
      required: true,
    },

    schema: {
      type: Object,
      required: true,
    }
  },

  data:() => ({
    selectedPoint: null,

    isInvalidMainSettings: true,
    isInvalidPointList: true,
  }),

  computed: {
    isInvalidForm() {
      return [
        this.isInvalidMainSettings,
        this.isInvalidPointList
      ]
      .some(isInvalid => isInvalid)
    },
  },

  watch: {
    isInvalidForm() {
      this.$emit('touch', this.isInvalidForm)
    },

    points: {
      handler() {
        if (!this.points.find(point => point === this.selectedPoint)) {
          this.selectedPoint = this.points[0]
        }
      },
      immediate: true,
    },
  },
}
</script>

<style lang="less" scoped>
.app-schema-edit-settings {
  display: grid;
  grid-template-columns: 8fr 18fr;
  grid-gap: 48px;
  grid-template-areas:
    ". main-settings"
    "divider divider"
    "point-list point-settings";

  padding-bottom: 24px;
}

.edit-main-settings {
  grid-area: main-settings;
}

.divider {
  grid-area: divider;
  height: 0;
  padding: 0;
  border-top: 1px solid @grey-light;
}

.edit-point-list {
  grid-area: point-list;
}

.non-selected-message,
.edit-point-settings {
  grid-area: point-settings;
}

.nav-btns {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}
</style>
