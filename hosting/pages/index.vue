<template>
  <div id="app" class="px-5">
    <h1 class="text-3xl font-bold p-2">tosho-card</h1>
    
    <div>
      
      <p>残額 : {{ cardData.balance }}</p>
      <p>有効期限 : {{ cardData.date }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        card_id: '',
        pin: ''
      },
      Validation: {
        loginResult: ''
      },
      cardData: {},

    }
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
        "id": this.loginForm.card_id,
        "pin": this.loginForm.pin
      }).then((res) => {
        this.cardData = res
        this.Validation.loginResult = ""
        console.log(res)
      }).catch((err) => {
        console.log(err)
        this.Validation.loginResult = "データ取得失敗";
      });
    }
  },
}
</script>
