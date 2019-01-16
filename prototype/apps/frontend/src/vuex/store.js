import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    user: {},
    key: {}
}

const mutations = {
    isLogin(state, key) {
        state.key = key
        window.localStorage.setItem('user_token',key)
    }
}

export default new Vuex.Store({
    state,
    mutations
})