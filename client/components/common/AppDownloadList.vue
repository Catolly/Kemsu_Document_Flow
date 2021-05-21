<template>
  <div class="app-download-list">
    <div class="short-file-list">
      <div class="file-list">
        <app-download-file
          v-for="(file, index) in files.slice(0, 3)"
          :key="index"
          :file="file"
          class="file"
        />
      </div>

      <div v-if="files.length > 3" class="btns">
        <app-button
          square
          class="toggle btn"
          title="Открыть"
          @click="isOpen = true"
        >
          <icon-arrow class="icon icon-arrow"/>
        </app-button>

        <app-button
          square
          class="btn"
        >
          {{files.length}}
        </app-button>
      </div>
    </div>

    <div
      v-show="isOpen"
      class="full-file-list-wrapper"
    >
      <div class="full-file-list">
        <div class="file-list">
          <app-download-file
            v-for="(file, index) in files"
            :key="index"
            :file="file"
            class="file"
          />
        </div>

        <div class="btns">
          <app-button
            square
            class="toggle btn"
            title="Закрыть"
            @click="isOpen = false"
          >
            <icon-arrow class="icon icon-arrow is-open"/>
          </app-button>
          <app-button
            square
            class="btn"
          >
            {{files.length}}
          </app-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import IconArrow from '~/components/icons/IconArrow'
import IconDownload from '~/components/icons/IconDownload'
import AppDownloadFile from '~/components/common/AppDownloadFile'

export default {
  name: 'AppDownloadList',

  components: {
    AppButton,
    IconArrow,
    IconDownload,
    AppDownloadFile,
  },

  data:() => ({
    isOpen: false,
  }),

  props: {
    files: {
      type: Array,
      default:() => [],
    },
  },
}
</script>

<style lang="less" scoped>
.app-download-list {
  display: flex;
  gap: 8px;
}

.full-file-list-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;

  padding: 48px 24px;

  background: @grey-bright;
  border: 1px solid @grey-light;
  border-radius: 10px;

  box-shadow: 10px 10px 50px fade(@black, 3%);
}

.short-file-list {
  display: flex;
  gap: 8px;

  .file-list {
    display: flex;
    gap: 4px;
  }
}

.full-file-list {
  display: flex;
  gap: 24px;

  .file-list {
    display: grid;
    grid-template-columns: repeat(5, auto);
    grid-gap: 8px 4px;
  }
}

.btns {
  display: flex;
  gap: 4px;
}

.btn {
  height: 36px;
  width: fit-content;
  padding: 0 18px;

  border-radius: 3px;
  border-color: @grey-medium;

  color: @black;

  &:focus-visible,
  &:hover {
    background: @grey-light;
    color: @blue;
    .icon {
      fill: @blue;
    }
  }
}

.icon-arrow {
  width: 16px;
  transform: rotate(-90deg);

  &.is-open {
    transform: rotate(90deg);
  }
}
</style>
