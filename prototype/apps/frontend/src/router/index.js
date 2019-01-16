import Vue from 'vue'
import Router from 'vue-router'
import Registration from '@/components/Registration'
import Login from '@/components/Login'
import CandidateProfile from '@/components/CandidateProfile'
import EmployerProfile from '@/components/EmployerProfile'
import RecruiterProfile from '@/components/RecruiterProfile'
import MainPage from '@/components/MainPage'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/register',
      name: 'register',
      components: {
        main: Registration
      }
    },
    {
      path: '/login',
      name: 'login',
      components: {
        main: Login
      }
    },
    {
      path: '/candidate-profile',
      name: 'cprofile',
      meta:{
        requireAuth: true
      },
      components: {
        main: CandidateProfile
      }
    },
    {
      path: '/employer-profile',
      name: 'eprofile',
      meta:{
        requireAuth: true
      },
      components: {
        main: EmployerProfile
      }
    },
    {
      path: '/recruiter-profile',
      name: 'rprofile',
      components: {
        main: RecruiterProfile
      }
    },
    {
      path: '/',
      alias: '/home',
      name: 'hpage',
      components:{
        main: MainPage
      }
    },
  ]
})
