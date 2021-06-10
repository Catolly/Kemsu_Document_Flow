<template>
  <div class="app-delete-schema-dialog">
    <app-button
      plain
      red
      type="button"
      class="delete"
      @click="dialog = true"
    >
      Удалить шаблон
    </app-button>

    <app-dialog :isOpen="dialog" @close="dialog = false">
      <div class="dialog">
        <span>Действительно удалить шаблон обходного листа?</span>

        <div class="btns">
          <app-button type="button" cancel @click="$emit('delete')">
            Удалить
          </app-button>
          <app-button type="button" blue filled @click="dialog = false">
            Отмена
          </app-button>
        </div>
      </div>
    </app-dialog>
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppDialog from '~/components/common/AppDialog'

export default {
  name: 'AppDeleteSchemaDialog',

  components: {
    AppButton,
    AppDialog,
  },

  data:() => ({
    dialog: false,
  }),
}
</script>

<style lang="less" scoped>
.dialog {
  margin-top: .5em;
  width: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5em;
}

.btns {
  display: flex;
  justify-content: center;
  gap: 2em;
}
</style>
