<template>
  <div id="container">
    <nuxt/>
    <div id="logo">
      <img src="~/assets/logo.svg" alt="КемГУ">
    </div>

    <div id="registration-wrapper">
      <form action="#" id="registration-form"> 
        <h1>Регистрация</h1>
        <div id="form-inner">
          <div class="input-wrapper">
            <input 
            v-model="username"
            type="text" 
            id="username" 
            placeholder=" " 
            required>
            <label for="username">Ф.И.О.</label>
          </div>
          <div class="input-wrapper">
            <input
            v-model="email"
            type="email" 
            id="email" 
            placeholder=" " 
            required>
            <label for="email">Email</label>
          </div>
          <div class="input-wrapper">
            <input
            v-model="password"
            type="password"
            id="password"
            placeholder=" "
            required>
            <label for="password">Пароль</label>
          </div>
          <div class="buttons-wrapper">
            <button
            class="filled"
            id="register">
              Зарегистрироваться
            </button>
            <button
            id="login">
              Войти
            </button>
          </div>
        </div>
        <p id="registered-under-you">Кто-то зарегистрировался под вашим именем? Обратитесь к <NuxtLink to="#">администрации</NuxtLink></p>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    }
  }
}

</script>

<style lang="less">

@main_blue: #4A72FF;
@main_blue_active: #2C53DA;
@theme-color: #fff;

@input-bg: #FDFDFD;
@input-border: #F3F3F3;

@fz-1: 20px;
@fz-2: 18px;
@fz-3: 16px;
@fw-medium: 500;
@fw-normal: 400;
@fw-light: 300;

.label-focused(@font-size, @font-weight: 400) {
  top: -0.875*@font-size;
  left: 1.5*@font-size;
  font-size: @font-size;
  font-weight: @font-weight;
  line-height: 200%;
}

.flex(
      @justify-content: center, 
      @align-items: normal, 
      @flex-direction: row) {
  display: flex;
  justify-content: @justify-content;
  align-items: @align-items;
  flex-direction: @flex-direction;
}

html {
  font-weight: 300;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

* {
  font-family: "Montserrat", Roboto, "Helvetica Neue", Arial, sans-serif;
}

*, *:before, *:after {
  box-sizing: border-box;
  margin: 0;
}

*:focus {
  outline: none;
}

h1 {
  font-size: 36px;
  line-height: 1em;
  font-weight: @fw-medium;
}

input {
  background: @input-bg;
  border: 1px solid @input-border;
  border-radius: 10px;

  padding-left: 24px;
  width: 100%;
}

input:focus + label,
input:not(:placeholder-shown) + label {
  background: @theme-color;
}

button, label, input {
  font-size: @fz-1;
}

button {
  font-weight: @fw-medium;
  border-radius: 10px;
  border: none;
  background-color: #fff;
}

label {
  color: #AFAFAF;
  padding: 0 8px;
}

p {
  font-size: @fz-2;
  line-height: 160%;
}

a {
  color: @main_blue;
  text-decoration: none;
  position: relative;
}

a::after {
  .absolute();
  bottom: 0;
  left: 0;
  width: 100%;
  border-bottom: 1px solid @main_blue;
}

a:hover, 
a:hover::after {
  color: @main_blue_active;
}

img {
  width: 100%;
  height: 100%;
}

#container {
  position: relative;
}

.label-absolute() {
  position: absolute;
  top: 1.2em;
  left: 1.2em;
}

// Relocate this to global less file -^

#logo {
  height: 85px;
  width: 55px;

  position: absolute;
  top: 25px;
  left: 60px;
}

#registration-wrapper {
  height: 100vh;
  .flex(center, center);
}

#registration-form {
  width: 516px;
}

h1 {
  text-align: center;
}

input {
  height: 70px;

  font-size: @fz-1;
  line-height: 160%;
}

input:focus {
  border-color: @main_blue;
}

input:focus + label,
input:not(:placeholder-shown) + label {
  .label-focused(@fz-3);
}

#form-inner {
  margin-top: 48px;
}

.input-wrapper {
  position: relative;
  margin-top: 18px;
}

.input-wrapper label {
  .label-absolute();
}

.input-wrapper label,
.input-wrapper input {
  transition: .2s ease all;
} 

#form-inner button {
  height: 70px;
  width: 100%;
  margin-top: 4px;

  color: @main_blue;
  border: 1px solid @main_blue;
}

#form-inner button:first-child {
  margin-top: 32px;
}

#form-inner button.filled {
  background-color: @main_blue;
  border: none;
  color: #fff;
}

#registered-under-you {
  margin-top: 18px;
}

.absolute() {
  position: absolute;
  content: '';
}

</style>

