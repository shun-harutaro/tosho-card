<template>
  <div class="scan">
    <h1 class="text-3xl font-bold p-2">tosho-card</h1>
    <div ref="canvas-container">
      <canvas class="w-full max-w-3xl mx-auto" ref="canvas" ></canvas>
    </div>
    <div class="text-center pt-3">
      <div v-if="status=='play'">
        <button @click="takeSnapshot">
          snapshot
        </button>
      </div>
      <div v-if="status=='pause'">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded" @click="runOcr">
          ID番号を読み取る
        </button>
      </div>
      <div v-if="status=='reading'">
        <p>読み取り中...</p>
        <button class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 ml-1 border border-blue-500 hover:border-transparent rounded" @click="playVideo">
         戻る
        </button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      status: 'none'
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
      const c_w = this.canvas.width
      const c_h = this.canvas.height
      this.context.fillStyle = "black";
      this.context.fillRect(0, 0, c_w/4, c_h);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(c_w/4*3, 0, c_w, c_h);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(c_w/4, 0, c_w/4*2, c_h/11*5);
      this.context.globalAlpha = 0.8
      this.context.fillStyle = "black";
      this.context.fillRect(c_w/4, c_h/11*6, c_w/4*2, c_h);
      this.context.globalAlpha = 0.8
    },
    async runOcr() { //スナップショットからテキストを抽出
      const Tesseract = require('tesseract.js')
      this.status = 'reading';
      this.pauseVideo()
      const result = await this.pauseVideo();
      const dataUrl = this.canvas.toDataURL();
      Tesseract.recognize(dataUrl, 'eng', {
        logger: log => {
          console.log(log);
        }
      }).then(result => {
        const scan_data = result.data.text
        const num_data = scan_data.replace(/[^0-9]/g, ''); //正規表現によって数字のみ取り出す
        console.log(num_data)
        this.send(num_data);
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
      this.status = 'pause'
      //this.binary();
    },
    takeSnapshot() {
      this.pauseVideo();
      this.binary();
    },
    send(data) {
      this.$emit("get-scan", data);
    },
    binary() {
      const WIDTH = this.canvas.width;
      const HEIGHT = this.canvas.height;
      if (this.video.readyState === this.video.HAVE_ENOUGH_DATA){
        console.log('white');
        this.context.drawImage(this.video, 0, 0, WIDTH, HEIGHT);
        const sourceImageData = this.context.getImageData(0, 0, WIDTH, HEIGHT);
        const sourceData = sourceImageData.data
        console.log(sourceData)
        const THRESHOLD = 200;
        const getColor = (sourceData, i) => {
          const avg = (sourceData[i] + sourceData[i+1], sourceData[i+2]) / 3;
          console.log(avg)
          if (THRESHOLD < avg) { //avg: rgbの平均
            return 255; //white
          } else {
            return 0; //black
          }
        };
        for (let i = 0; i < sourceData.length; i+=4){
          const color = getColor(sourceData, i);
          sourceData[i] = sourceData[i+1] = sourceData[i+2] = color;
        };
        this.context.putImageData(sourceImageData, 0, 0);
      }
    }
  },
  mounted() {
    this.initialize();
  }
}
</script>