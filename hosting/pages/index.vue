<template>
  <div>
    <Scan @get-scan='card_id = $event'/>
    <Form :card_id="card_id" @get-card_data='card_data = $event' />
    <!-- カスタムイベントcloseModalを受け取り、showをfalseにし非表示に。 --->
    <Modal @closeModal="card_data = ''" v-if="card_data" :card_data="card_data" />
    <button @click="show = true">
      <p>モーダル表示</p>
    </button>
  </div>
</template>

<script>
import Scan from '~/components/Scan.vue'
import Form from '~/components/Form.vue'
import Modal from '~/components/Modal.vue'
export default {
  data() {
    return {
      card_id:'',
      card_data: {
        balance: '1000',
        date: '2020'
      },
    }
  },
  components: {
    Scan,
    Form,
    Modal
  }
}
</script>