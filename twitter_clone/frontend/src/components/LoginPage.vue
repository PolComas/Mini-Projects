<template>
  <div class="container">
    <h1>Inicia Sessió</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Nom d'usuari" required />
      <input type="password" v-model="password" placeholder="Contrasenya" required />
      <button>Inicia Sessió</button>
    </form>
    <p>No tens compte? <router-link to="/register">Registra’t aquí</router-link></p>
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
    async login() {
      try {
        const res = await axios.post('login/', { username: this.username, password: this.password });
        const token = res.data.token;
        localStorage.setItem('token', token);
        this.$router.push('/home');
      } catch (err) {
        this.error = 'Credencials incorrectes';
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
