<template>
  <div
    :class="classObj"
    class="app-upload-wrapper"
  >
    <div class="app-upload">
      <div
        :class="{'small': small}"
        class="plus"
      />

      <input
        type="file"
        multiple
        accept="image/png,image/jpg,image/jpeg,application/pdf,application/pdf,application/msworld,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        class="input"
        @change="upload($event.target)"
        @click.stop=""
      >
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppUpload',

  props: {
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
  },

  methods: {
    upload(input) {
      this.$emit('upload', input.files)
      input.value = ''
    },
  },
}
</script>

<style lang="less" scoped>

.app-upload-wrapper {
  position: relative;

  height: 100px;
  width: 100px;

  &.big {
    height: 200px;
    width: 200px;
  }

  &.small {
    height: 70px;
    width: 70px;
  }
}

.app-upload {
  position: relative;

  overflow: hidden;

  height: 100%;
  width: 100%;

  background: @grey-bright;
  border: 1px solid @grey-light;
  border-radius: 5px;

  &:hover {
    background: @grey-light;
    border-color: @blue;
  }
}

.input,
.input::-webkit-file-upload-button {
  z-index: 2;

  height: 100%;
  width: 100%;

  outline: 0;
  opacity: 0;
  cursor: pointer;
  user-select: none;
}

.plus {
  .plus();

  &.small {
    .plus(16px);
  }
}

</style>
