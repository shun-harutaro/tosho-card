<template>
  <div class="form">
    <form class="form_cotent" v-on:submit.prevent="checkForm">
      <ul>
        <li>
          <span>ID : </span>
          {{ card_id }}
        </li>
        <li>
          <span>PIN : </span>
          <input type="text" maxlength="4" v-model="loginForm.pin">
        </li>
        <li>
          <button>
            調べる！
          </button>
          <p>{{ Validation.loginResult }}</p>
        </li>
      </ul>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        pin: '',
      },
      Validation: {
        loginResult: '',
      },
      cardData: {},
    }
  },

  props: {
    card_id: String,
  },

  methods: {
    checkForm(){
      if (this.loginForm.card_id.length != 16){
        this.Validation.loginResult = "IDは16桁です"
      } else {
        this.getCardData()
      }
    },
    async getCardData() {
      this.Validation.loginResult = "データ取得中...";
      const carddata = await this.$axios.$post(
        this.$config.baseURL,{
        "id": this.card_id,
        "pin": this.loginForm.pin
      }).then((res) => {
        this.cardData = res
        this.Validation.loginResult = ""
        console.log(res)
      }).catch((err) => {
        console.log(err)
        this.Validation.loginResult = "データ取得失敗";
      });
    },
  },
}
</script>