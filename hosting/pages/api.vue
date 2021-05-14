<template>
  <div>
    <ul>
      <li v-for="post in posts" :key="post.id">
        {{ post }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const response = await $axios.$post
      ('https://us-central1-tosho-card.cloudfunctions.net/main',{
        id: "1119490082825296",
        pin: "3664"
      }).catch(err => {
        console.log(err) //失敗
      });
      console.log(response)
    return { posts: response };
  } 
}
</script>
