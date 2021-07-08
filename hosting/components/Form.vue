<template>
  <div class="w-full h-full fixed inset-0">
    <div class="w-full h-full bg-black bg-opacity-50 modal-wrap relative">
      <div class="bg-white w-4/5 h-1/4 absolute m-auto inset-0 text-center flex items-center justify-center">
        <div class="modal-content" v-if="showForm">
          <form class="form_cotent" v-on:submit.prevent="checkForm">
            <ul>
              <li>
                <span>ID : </span>
                {{ card_id }}
              </li>
              <li>
                <span>PIN : </span>
                <input type="text" maxlength="4" v-model="loginForm.pin" class="w-20 border rounded"/>
              </li>
              <li>
                <p>{{ Validation.loginResult }}</p>
                <button
                  class="
                    bg-blue-500
                    hover:bg-blue-700
                    text-white
                    font-bold
                    px-8
                    py-2
                    rounded
                    my-1
                  "
                >
                  調べる
                </button>
              </li>
            </ul>
          </form>
          <button
            class="
              bg-transparent
              hover:bg-blue-500
              text-blue-700
              font-semibold
              hover:text-white
              px-8
              py-2
              rounded
              ml-1
              border border-blue-500
            "
            @click="$emit('closeModal')"
          >
            閉じる
          </button>
        </div>
        <div class="loading" v-else>
          <!-- TODO:loading animation -->
          <p class="text-5xl">データ取得中</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showForm: true,
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
      //this.Validation.loginResult = "データ取得中...";
      this.showForm = false;
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
          this.$emit("closeModal");
        })
        .catch((err) => {
          console.log(err);
          this.Validation.loginResult = "データ取得失敗";
          this.showForm = true;
          this.error = true;
        });
    },
    send(data) {
      this.$emit("get-card_data", data);
    },
  },
};
</script>