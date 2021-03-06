<template>
  <div class="app-upload-list">
    <div
      v-for="(file, index) in documentList"
      :key="index"
      :title="'Удалить ' + filename(file)"
      :class="classObj"
      class="file"
    >
      <div
        :class="classObj"
        class="body"
        @click="$emit('delete', file)"
      >
        <img
          v-if="previewIcon(file)"
          :src="previewIcon(file)"
          class="preview-icon"
        >

        <div
          :class="{'small': small}"
          class="cross"
        />
      </div>

      <a
        class="header"
        :title="'Открыть ' + filename(file)"
        :download="filename(file)"
        :href="createURL(file)"
        target="_blank"
      >
        {{filename(file)}}
      </a>
    </div>
  </div>
</template>

<script>
import { BASE_URL } from '~/services/config'

export default {
  name: 'AppUploadList',

  props: {
    documentList: {
      type: Array,
      default:() => [],
    },

    big: {
      type: Boolean,
      default: false,
    },

    small: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    classObj() {
      return {
        'big': this.big,
        'small': this.small,
      }
    },

    BASE_URL() {
      return BASE_URL
    },
  },

  methods: {
    filename(file) {
      if (this.isLink(file)) return this.shortname(file)
      return file.name
    },

    shortname(file) {
      return file
        .split('/')
        .slice(-1)
        .join()
    },

    isLink(file) {
      return typeof file === 'string'
    },

    createURL(file) {
      if (this.isLink(file)) return this.BASE_URL + file
      return URL.createObjectURL(file)
    },

    previewIcon(file) {
      let fileType
      if (this.isLink(file))
        fileType = file.split('.').reverse()[0].toLowerCase()
      else
        fileType = file.name.split('.').reverse()[0].toLowerCase()

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
.app-upload-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.file {
  display: flex;
  flex-direction: column;
  gap: 8px;

  width: 100px;

  &.big {
    width: 200px;
  }

  &.small {
    width: 70px;
  }
}

.body {
  position: relative;

  cursor: pointer;

  width: 100%;
  height: 100px;

  &.big {
    height: 200px;
  }

  &.small {
    height: 70px;
  }

  background: @white;
  border: 1px solid @grey-light;
  border-radius: 5px;

  &:hover {
    border-color: @red;

    .cross:before,
    .cross:after {
      background: @red;
    }
  }
}

.cross {
  .cross();

  &.small {
    .cross(16px);
  }

  &::before {
    transform: rotate(45deg);
  }
  &::after {
    transform: rotate(135deg);
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

.header {
  width: 100%;

  font-size: @fz-small;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
