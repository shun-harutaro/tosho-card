<template>
  <div id="app">
    <div ref="canvas-container">
      <canvas ref="canvas" style="width:100%;margin:0 auto;"></canvas>
    </div>
    <div class="text-center pt-3">
      <div v-if="status=='play'">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded" @click="takeSnapshot">
          スナップショットを取る
        </button>
      </div>
      <!-- pause： スナップショットを撮ったので一次停止 -->
      <div v-if="status=='pause'">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 mr-1 rounded" @click="runOcr">
          ID番号を読み取る
        </button>
        <button class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 ml-1 border border-blue-500 hover:border-transparent rounded" @click="playVideo">
         戻る
        </button>
      </div>
      <!-- pause： スナップショットをOCRにかけてテキストを取得 -->
      <div v-if="status=='reading'">
        読み取り中です...
      </div>
    </div>
    <form class="form" v-on:submit.prevent="onSubmit">
      <ul>
        <li>
          <span>ID : </span>
          <input type="text" name="id" id="" v-model="card_id">
        </li>
        <li>
          <span>PIN : </span>
          <input type="text" name="pin" id="" maxlength="4" v-model="pin">
        </li>
        <li>
          {{ Validation.loginReult }}
        </li>
        <li>
          <button>
            Login
          </button>
        </li>
      </ul>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      video: null,
      canvas: null,
      context: null,
      dataUrl: '',
      status: 'none',
      loginForm: {
        card_id: "",
        pin: ""
      },
      Validation: {
        loginResult: ""
      }
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
        //this.context.fillStyle = "rgb(0, 0, 255)";
        //this.context.fillRect(20,20,50,50);
        //this.context.globalCompositeOperation = "destination-in";

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
        //this.context.fillStyle = "black";
        //this.context.fillRect(0,0,this.canvas.width, this.canvas.height);
        //this.context.globalAlpha = 0.5
        //this.context.fillStyle = "white"
        //this.context.fillRect(0,0,50, 50);
        //this.context.globalAlpha = 0;
      }
      requestAnimationFrame(this.render);
    },
    guide() {
      this.context.fillStyle = "black";
      this.context.fillRect(0,0,this.canvas.width/4, this.canvas.height);
      this.context.globalAlpha = 0.5
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4*3,0,this.canvas.width, this.canvas.height);
      this.context.globalAlpha = 0.5
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4,0,this.canvas.width/4*2, this.canvas.height/11*5);
      this.context.globalAlpha = 0.5
      this.context.fillStyle = "black";
      this.context.fillRect(this.canvas.width/4,this.canvas.height/11*6,this.canvas.width/4*2, this.canvas.height);
      this.context.globalAlpha = 0.5
    },
    runOcr() { //スナップショットからテキストを抽出
      const Tesseract = require('tesseract.js')
      this.status = 'reading';
      Tesseract.recognize(this.dataUrl, 'eng', {
        logger: log => {
          console.log(log);
        }
      }).then(result => {
        document.getElementById("id").value = result.data.text;
        this.Validation.loginResult = "success";
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
      this.status = 'pause';
    },
    takeSnapshot() {
      this.pauseVideo();
      this.dataUrl = this.canvas.toDataURL();
    }
  },

  mounted() {
    this.initialize();
  }
}
</script>
