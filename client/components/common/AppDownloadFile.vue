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
  height: 60px;
  width: 60px;

  background: @white;
  border: 1px solid @grey-light;
  border-radius: 5px;

  display: inline-block;
  position: relative;

  &:focus-visible,
  &:hover {
    border-color: @blue;

    .icon-download {
      fill: @blue;
    }
  }
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

  position: absolute;
  top: calc(50% - .5*@size);
  left: calc(50% - .5*@size);
}
</style>
