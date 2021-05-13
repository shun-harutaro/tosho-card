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
  async asyncData(context) {
    const response = await context.$axios.$post
      ('https://us-central1-tosho-card.cloudfunctions.net/handler',{
        "id": "1119490082825296",
        "pin": "3664"
      }).then(res => {
        console.log('成功')
      })
      .catch((err) => {
        console.log(err) //失敗
      });
    return { posts: response };
  } 
}
</script>
