<template>
  <div class="container">
    <h1>Registra't</h1>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Nom d'usuari" required />
      <input type="password" v-model="password" placeholder="Contrasenya" required />
      <button>Registrar-se</button>
    </form>
    <p>Ja tens compte? <router-link to="/">Inicia Sessió</router-link></p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

export default {
  data() {
    return { username: '', password: '', error: null };
  },
  methods: {
    async register() {
      try {
        await axios.post('register/', { username: this.username, password: this.password });
        // Auto-login després de registrar
        const res = await axios.post('login/', { username: this.username, password: this.password });
        const token = res.data.token;
        localStorage.setItem('token', token);
        this.$router.push('/home');
      } catch (err) {
        this.error = 'Error al registrar-se';
      }
    }
  }
};
</script>

<style scoped>
.container {
  width: 300px;
  margin: 100px auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  background: #1da1f2;
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  cursor: pointer;
  border-radius: 4px;
}
.error { color: red; }
</style>
