<template>
  <div id="app" class="px-5">
    <h1 class="text-3xl font-bold p-2">tosho-card</h1>
    <div ref="canvas-container">
      <canvas ref="canvas" style="width:100%;margin:0 auto;"></canvas>
    </div>
    <div class="text-center pt-3">
      <div v-if="status=='play'">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded" @click="runOcr">
          ID番号を読み取る
        </button>
      </div>
      <!-- pause： スナップショットを撮ったので一次停止 -->
      <div v-if="status=='reading'">
        <p>読み取り中...</p>
        <button class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 ml-1 border border-blue-500 hover:border-transparent rounded" @click="playVideo">
         戻る
        </button>
      </div>
    </div>
    
    <modal>
      
    </modal>

    <form class="form" v-on:submit.prevent="checkForm">
      <ul>
        <li>
          <span>ID : </span>
          <input type="text" v-model="loginForm.card_id" style="width:80%">
        </li>
        <li>
          <span>PIN : </span>
          <input type="text" maxlength="4" v-model="loginForm.pin">
        </li>
        <li>
          <button>
            調べる！
          </button>
        </li>
      </ul>
    </form>
    <div>
      <p>{{ Validation.loginResult }}</p>
      <p>残額 : {{ cardData.balance }}</p>
      <p>有効期限 : {{ cardData.date }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
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
      video: null,
      canvas: null,
      context: null,
      dataUrl: '',
      status: 'none',
    }
  },
  
  methods: {
    initialize() {
      this.status = 'initialize';
      navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: {
            ideal: 'environment'
          }
        }
      }).then(stream => {
        this.canvas = this.$refs.canvas;
        this.context = this.canvas.getContext('2d');

        this.video = document.createElement('video');
        this.video.addEventListener('loadedmetadata', () => { // メタデータが取得できるようになったら実行
          const canvasContainer = this.$refs['canvas-container'];
          this.canvas.width = canvasContainer.offsetWidth;
          this.canvas.height = parseInt(this.canvas.width * this.video.videoHeight / this.video.videoWidth);
          this.render();

        });
        // for iOS
        this.video.setAttribute('autoplay','');
        this.video.setAttribute('muted', '');
        this.video.setAttribute('playsinline','');
        this.video.srcObject = stream;
        this.playVideo();

      }).catch(error => console.log(error));
    },
    render() {
      if(this.video.readyState === this.video.HAVE_ENOUGH_DATA){
        this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height,);
        this.guide();
      }
      requestAnimationFrame(this.render);
    },
    guide() {
      this.context.fillStyle = "black";
      this.context.fillRect(0,0,this.canvas.width/4, this.canvas.height);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4*3,0,this.canvas.width, this.canvas.height);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4,0,this.canvas.width/4*2, this.canvas.height/11*5);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4,this.canvas.height/11*6,this.canvas.width/4*2, this.canvas.height);
      this.context.globalAlpha = 0.8
    },
    runOcr() { //スナップショットからテキストを抽出
      const Tesseract = require('tesseract.js')
      this.status = 'reading';
      this.pauseVideo();
      this.dataUrl = this.canvas.toDataURL();
      Tesseract.recognize(this.dataUrl, 'eng', {
        logger: log => {
          console.log(log);
        }
      }).then(result => {
        const scan_data = result.data.text
        const num_data = scan_data.replace(/[^0-9]/g, ''); //正規表現によって数字のみ取り出す
        console.log(num_data)
        this.loginForm.card_id = num_data
      })
      .catch(error => console.log(error))
      .finally(() => {
        this.playVideo();
      });
    },
    playVideo() {
      this.video.play();
      this.status = 'play';
    },
    pauseVideo() {
      this.video.pause();
      //this.status = 'pause';
    },
    /*takeSnapshot() {
      this.pauseVideo();
      this.dataUrl = this.canvas.toDataURL();
    },*/
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

  mounted() {
    this.initialize();
  }
})
</script>
