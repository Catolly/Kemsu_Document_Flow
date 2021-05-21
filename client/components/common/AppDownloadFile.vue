<template>
  <a
    :title="'Скачать ' + file.name"
    :download="file.name"
    class="app-download-file clear"
  >
    <!-- :href="createURL(file)" -->
    <img
      v-if="previewIcon(file)"
      :src="previewIcon(file)"
      class="preview-icon"
    >

    <icon-download class="icon-download" />
  </a>
</template>

<script>
import IconArrow from '~/components/icons/IconArrow'
import IconDownload from '~/components/icons/IconDownload'

export default {
  name: 'AppDownloadFile',

  components: {
    IconArrow,
    IconDownload,
  },

  data:() => ({
    isOpen: false,
  }),

  props: {
    file: {
      type: Object,
      required: true,
    },
  },

  methods: {
    createURL(file) {
      return URL.createObjectURL(file)
    },

    previewIcon(file) {
      const fileType = file.name.split('.').reverse()[0].toLowerCase()

      switch(fileType) {
        case 'doc':
          return require('~/assets/icons/AppImageUpload/doc.svg')
        case 'docx':
          return require('~/assets/icons/AppImageUpload/doc.svg')
        case 'pdf':
          return require('~/assets/icons/AppImageUpload/pdf.svg')
        case 'png':
          return require('~/assets/icons/AppImageUpload/png.svg')
        case 'jpg':
          return require('~/assets/icons/AppImageUpload/jpg.svg')
        case 'jpeg':
          return require('~/assets/icons/AppImageUpload/jpg.svg')
        default:
          return
      }
    },
  },
}
</script>

<style lang="less" scoped>
.app-download-file {
  display: flex;
  flex-direction: column;
  gap: 8px;

  width: 60px;
  &.big {
    width: 200px;
  }
  &.normal {
    width: 100px;
  }
}

.preview {
  position: relative;

  width: 100%;
  height: 60px;
  &.big {
    height: 200px;
  }
  &.normal {
    height: 100px;
  }

  background: @white;
  border: 1px solid @grey-light;
  border-radius: 5px;

  &:focus-visible,
  &:hover {
    border-color: @blue;
  }

  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-icon {
  position: absolute;

  top: 10%;
  bottom: 10%;
  left: 10%;
  right: 10%;

  height: 80%;
  width: 80%;

  opacity: .5;
}

.icon-download {
  @size: 10%;

  min-height: 16px;
  min-width: 16px;

  height: @size;
  width: @size;
}

.header {
  width: 100%;

  font-size: @fz-small;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
