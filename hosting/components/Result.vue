<template>
  <div class="w-full h-full fixed inset-0">
    <div class="w-full h-full bg-black bg-opacity-50 modal-wrap relative">
      <div class="bg-white w-4/5 h-1/4 absolute m-auto inset-0 text-center flex items-center justify-center">
        <div class="modal-content">
          <p>残額 : {{ card_data.balance }}</p>
          <p>有効期限 : {{ card_data.date }}</p>
          <button
            class="
              bg-blue-500
              hover:bg-blue-700
              text-white
              font-bold
              px-8
              py-3
              rounded
            "
            @click="$emit('closeModal')"
          >
            閉じる
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    card_data: Object,
  },
};
</script>