<template>
  <div class="container">
    <h1>MiniTwitter</h1>
    <button @click="logout">Tancar Sessió</button>
    <form @submit.prevent="submitTweet">
      <input v-model="text" placeholder="Què estàs pensant?" required />
      <button>Publicar Tweet</button>
    </form>
    <ul>
      <li v-for="tweet in tweets" :key="tweet.id">
        <b>{{ tweet.author }}</b>: {{ tweet.text }}
      </li>
    </ul>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

export default {
  data() {
    return { token: null, text: '', tweets: [], error: null };
  },
  created() {
    this.token = localStorage.getItem('token');
    if (!this.token) {
      this.$router.push('/');
    } else {
      this.loadTweets();
    }
  },
  methods: {
    async loadTweets() {
      try {
        const res = await axios.get('tweets/', {
          headers: { Authorization: `Token ${this.token}` }
        });
        this.tweets = res.data;
      } catch (err) {
        this.error = 'Error carregant tweets';
      }
    },
    async submitTweet() {
      try {
        await axios.post('tweets/', { text: this.text }, {
          headers: { Authorization: `Token ${this.token}` }
        });
        this.text = '';
        this.loadTweets();
      } catch (err) {
        this.error = 'Error publicant tweet';
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.container {
  width: 400px;
  margin: 50px auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}
input, button {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  background: #1da1f2;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
.error { color: red; }
ul { text-align: left; padding: 0; list-style: none; }
</style>
