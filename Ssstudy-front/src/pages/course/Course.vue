<template>
    <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
      <h1>课程</h1>
    </div>
  </template>
  <script>
    import {mapState} from 'vuex'
    export default {
      name: 'Course',
      data() {
        return {
          desc: '课程清单'
        }
      },
      computed: {
        ...mapState('setting', ['pageMinHeight']),
      }
    }
  </script>
  <style scoped lang="less">
  @import "index.less";
  </style>