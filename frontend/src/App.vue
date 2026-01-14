<template>
  <div id="app">
    <div class="ui menu">
      <div class="header item">
        <i class="calendar check icon"></i>
        考勤管理系统
      </div>
      <router-link to="/employee" class="item" active-class="active">
        <i class="user icon"></i>
        员工签到
      </router-link>
      <router-link to="/admin" class="item" active-class="active">
        <i class="settings icon"></i>
        管理后台
      </router-link>
    </div>
    
    <div class="ui container" style="margin-top: 2em;">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Lato', 'Helvetica Neue', Arial, Helvetica, sans-serif;
}
</style>
