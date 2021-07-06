<template>
  <div class="px-5">
    <Scan @get-scan='card_id = $event'/>
    <Form @closeModal="card_id = ''" :card_id="card_id" @get-card_data='card_data = $event' v-if="card_id" />
    <Result @closeModal="card_data = ''" v-if="card_data" :card_data="card_data" />
  </div>
</template>

<script>
import Scan from '~/components/Scan.vue'
import Form from '~/components/Form.vue'
import Result from '~/components/Result.vue'
export default {
  data() {
    return {
      card_id:'xxxxxxxxxxxxxxx',
      card_data: false,
    }
  },
  components: {
    Scan,
    Form,
    Result
  }
}
</script>