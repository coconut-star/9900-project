// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './vuex/store'
import axios from 'axios'


Vue.config.productionTip = false

axios.interceptors.request.use(
  config=>{
    var token = sessionStorage.getItem('key')
    try{
      var a = token
    }catch(e){
      token = 'temp token'
    }
    if(token){
      config.headers.Authorization = `token ${token}`
    }
    return config
  },
  error=>{
    return Promise.reject(error)
  }
)


router.beforeEach((to, from, next) =>{
  if(to.meta.requireAuth) {
    var token = sessionStorage.getItem('key')
    try {
      var a = token
    } catch (e) {
      next({
        path: '/login'
        // query: {redirect: to.fullPath}
      })
    }
    if (!isEmptyObject(token)){
      next();
    }else{
      next({
        path: '/login'
        // query: {redirect: to.fullPath}
      })
    }
  }else{
    next();
  }
})

function isEmptyObject(obj) {
  for(var key in obj) {
    return false;
  }
  return true;
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
