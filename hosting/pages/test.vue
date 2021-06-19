<template>
  <div>
    <h1>Hello from App.vue</h1>
    <p>parent_num: {{ parent_num }}</p>
    <Scan @my-click='parent_num = $event'/>
  </div>
</template>

<script>
import Scan from '~/components/Scan.vue'
export default {
  data() {
    return {
      parent_num: 100
    }
  },
  components: {
    Scan
  }
}
</script>