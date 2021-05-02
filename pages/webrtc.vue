<template>
  <section class="section">
    <div class="columns">
      <div class="column"><video id="localvideo" ref="localVideo" autoplay v-bind:srcObject.prop="localstream" width="500" height="500"></video></div>
    </div>
    <div class="columns">
      <div class="column"><canvas id="localPic" ref="localPicCanvas" width="640" height="350"></canvas></div>
    </div>
    <div class="buttons">
      <b-button @click="getUserMedia">映像を取得する</b-button>
      <b-button @click="getUserPic">写真を撮る</b-button>
    </div>
  </section>
</template>

<script>
export default {
  data: function() {
    return {
      localstream: undefined,
      canvas: undefined,
      movie: undefined,
      streamConst: {
        video: {
          width: 1280,
          height: 700
        }
      }
    }
  },
  mounted: function() {
    this.canvas = this.$refs.localPicCanvas;
    this.movie = this.$refs.localVideo;
  },
  methods: {
    getLocalMediaStream: function(mediaStream) {
      this.localstream = mediaStream;
    },
    handleLocalMediaStreamError: function(error) {
      console.error(`navigator.getUserMedia error: ${error}`);
    },
    getUserMedia: function() {
      navigator.mediaDevices
        .getUserMedia(this.streamConst)
        .then(this.getLocalMediaStream)
        .catch(this.handleLocalMediaStreamError);
    },
    getUserPic: function() {
      const ctx = this.canvas.getContext('2d');
      ctx.drawImage(this.movie, 0, 0, 640, 350);
    }
  }
}
</script>
