<template>
  <div class="app-reject-form">

    <app-button
      class="close-btn icon"
      @click="$emit('close')"
    >
      <icon-close />
    </app-button>

    <div class="header">
      <h1>Отказать</h1>

      <span>
        <span>
          Козырева Татьяна Андреевна
        </span>
        <br>
        <span class="student-status">
          Курс, факультет и тд.
        </span>
      </span>
    </div>

    <div class="reason">
      <app-text-field
        class="reason-text-field"
      />

      <!-- @click="addChipsToTextField" -->
      <div class="likely-reason-crisps">
        <app-chips class="chips">
          Необходимо сдать ключ от комнаты
        </app-chips>
        <app-chips class="chips">
          Необходимо сдать ключ от комнаты
        </app-chips>
        <app-chips class="chips">
          Необходимо сдать ключ от комнаты
        </app-chips>
      </div>
    </div>

    <app-button
      class="reject-btn red filled"
      @click="$emit('reject')"
    >
      Отказать
    </app-button>

  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import IconClose from '~/components/icons/IconClose'
import AppTextField from '~/components/common/AppTextField'
import AppChips from '~/components/common/AppChips'

export default {
  name: 'AppRejectForm',

  components: {
    AppButton,
    IconClose,
    AppTextField,
    AppChips,
  },


}
</script>

<style lang="less" scoped>
.app-reject-form {
  position: relative;

  display: grid;
  grid-row-gap: 48px;

  width: 900px;

  .close-btn {
    position: absolute;
    top: 0;
    right: 0;
  }

  .header,
  .reason {
    display: grid;
    grid-row-gap: 32px;
  }

  .student-status {
    color: @text-grey;
  }

  .reason-text-field {

  }

  .likely-reason-crisps {
    display: flex;
    flex-flow: row wrap;

    .chips {
      margin: 4px 8px 4px 0;
    }
  }
}

</style>
