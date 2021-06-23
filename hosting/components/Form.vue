<template>
  <div class="w-full h-full fixed inset-0">
    <div class="w-full h-full bg-black bg-opacity-50 modal-wrap relative">
      <div class="bg-white w-2/5 h-40 absolute m-auto inset-0 text-center">
        <form class="form_cotent" v-on:submit.prevent="checkForm">
          <ul>
            <li>
              <span>ID : </span>
              {{ card_id }}
            </li>
            <li>
              <span>PIN : </span>
              <input type="text" maxlength="4" v-model="loginForm.pin" />
            </li>
            <li>
              <p>{{ Validation.loginResult }}</p>
              <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded"
              >
                調べる！
              </button>
            </li>
          </ul>
        </form>
        <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded"
            @click="$emit('closeModal')"
        >
          閉じる
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        pin: "",
      },
      Validation: {
        loginResult: "",
      },
      cardData: {},
    };
  },

  props: {
    card_id: String,
  },

  methods: {
    checkForm() {
      if (this.card_id.length != 16) {
        this.Validation.loginResult = "IDは16桁です";
      } else {
        this.getCardData();
      }
    },
    async getCardData() {
      this.Validation.loginResult = "データ取得中...";
      const carddata = await this.$axios
        .$post(this.$config.baseURL, {
          id: this.card_id,
          pin: this.loginForm.pin,
        })
        .then((res) => {
          this.cardData = res;
          this.Validation.loginResult = "";
          console.log(res);
          this.send(this.cardData);
          this.$emit('closeModal')
        })
        .catch((err) => {
          console.log(err);
          this.Validation.loginResult = "データ取得失敗";
          this.error = true;
        });
    },
    send(data) {
      this.$emit("get-card_data", data);
    },
  },
};
</script>