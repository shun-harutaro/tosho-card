<template>
  <div class="w-full h-full fixed inset-0">
    <div class="w-full h-full bg-black bg-opacity-50 modal-wrap relative">
      <!-- このボタンを押すとカスタムイベントcloseModalが発生 -->
      <div class="bg-white w-2/5 h-40 absolute m-auto inset-0">
        <button @click="$emit('closeModal')">
          閉じる
        </button>
      </div>
    </div>
  </div>
</template>