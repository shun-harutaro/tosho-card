<template>
  <div>
    {{ posts.balance }}
    {{ posts.date }}
  </div>
</template>

<script>
export default {
  async asyncData({$axios}) {
    const posts = await $axios.$post //"$post"にするとresponse.data
      ('https://us-central1-tosho-card.cloudfunctions.net/handler',{
        "id": "1119490082825296",
        "pin": "3664"
      }).catch((err) => {
        console.log(err) //失敗
      });
    console.log(posts)
    return { posts } //{posts : posts}の短縮
  } 
}
</script>