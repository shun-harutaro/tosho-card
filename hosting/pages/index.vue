<template>
  <div>
    <Scan @my-click='card_id = $event'/>
    <Form :card_id="card_id"/>
  </div>
</template>

<script>
import Scan from '~/components/Scan.vue'
import Form from '~/components/Form.vue'
export default {
  data() {
    return {
      card_id:'1054924354380148'
    }
  },
  components: {
    Scan,
    Form
  }
}
</script>