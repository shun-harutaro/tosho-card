<template>
  <div class="modal fixed inset-0">
    <div class="modal-wrap relative">
      <!-- このボタンを押すとカスタムイベントcloseModalが発生 -->
      <div class="bg-white w-2/5 h-40 absolute m-auto inset-0">
        <button @click="$emit('closeModal')">
          閉じる
        </button>
      </div>
    </div>
  </div>
</template>

<style>
.modal {
  width: 100%;
  height: 100%;
}
.modal-wrap {
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
}
</style>