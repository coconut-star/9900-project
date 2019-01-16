<!-- Login page -->
<template>
<div class="bg-dark">
    <div class="d-flex align-content-center flex-wrap">
        <div class="container">
            <div class="login-content">
                <!-- Logo. -->
                <div class="login-logo">
                    <a href="/">
                        <img class="align-content" src="../assets/images/theme_logo_text.png" alt="">
                    </a>
                </div>

                <!-- Login form. -->
                <div class="login-form">
                    <form @submit.prevent="submit" role="form">
                        <!-- E-mail. -->
                        <div class="form-group">
                            <label>E-mail address</label>
                            <input type="email" v-model="email" class="form-control" placeholder="E-mail">
                        </div>
                        <!-- Password. -->
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" v-model="password" class="form-control" placeholder="Password" name="password">
                        </div>

                        <!-- Submission. -->                        
                        <button type="submit" class="btn btn-primary btn-flat m-b-30 m-t-30">Sign in</button>
                        
                        <label id="error" />

                        <div class="register-link text-center">
                            <p>Don't have an account? <a href="/register">Register here</a>!</p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<!-- JavaScript -->
<script>
import 'font-awesome/css/font-awesome.min.css'
import '../../static/assets/scss/style.css'
import '../../static/assets/css/themify-icons.css'
import axios from 'axios'
export default {
    name: "Login",
    data() {
        return {
            email: '',
            password: '',
            loading: false
        };
    },
    methods: {
        submit() {
            axios({
                    method: 'post',
                    url: API_HOST +'/rest-auth/login/',
                    data: {
                        "email": this.email.toLowerCase(),
                        "password": this.password,
                    }
                })
                .then((response) => {
                    console.log(response)
                    if (response.status === 200 || response.status === 201) {
                        //window.localStorage.getItem('key')
                        this.$store.commit('isLogin', response.data.key)
                        sessionStorage.setItem("key", response.data.key)
                        sessionStorage.setItem("user_id", response.data.user.id)
                        sessionStorage.setItem("user_role", response.data.user.role)
                        if (response.data.user.role === 'E') {
                            this.$router.push({path: '/employer-profile'})
                        } else if (response.data.user.role === 'C') {
                            this.$router.push({path: '/candidate-profile'})
                        } else if (response.data.user.role === 'R') {
                            this.$router.push({path: '/recruiter-profile'})
                        }
                    }
                })
                .catch(function (error) {
                    console.log(error)
                    console.log(error.response)
                    var error_label = document.getElementById("error");
                    error_label.textContent = "Email address or password not recognized."
                    error_label.hidden = false
                })
        },
        getData() {
            this.$http({
                    url: "",
                    method: "get",
                    params: {}
                })
                .then(response => {
                    if (response.data.success === true) {
                        this.loading = false;
                    }
                })
                .catch(function (error) {
                    console.log(error)
                });
        }
    },
    beforeMount() {
        this.loading = false
        sessionStorage.clear();
    }
};
</script>

<!-- CSS -->
<style>
@import '../assets/css/skillstash.css';
</style>

<style scoped>
.bg-dark {
    position: fixed;
    top: 0;
    bottom:100px;
    position:fixed;
    overflow-y:scroll;
    overflow-x:hidden;
    width: 100%;
    height: 100%;
}

a:hover, a:focus {
    text-decoration: none;
    text-decoration-line: none;
    text-decoration-style: initial;
    text-decoration-color: initial;
    color: #000;
}
.login-content {
    max-width: 540px;
    margin: 0 auto;
}
.login-logo {
    text-align: center;
    padding: 55px 0px 30px 0px;
    margin: 0px 25px;
}
.login-form {
    background: #ffffff;
    padding: 30px 30px 20px;
    border-radius: 2px;
}

.btn-primary:not([disabled]):not(.disabled).active, .btn-primary:not([disabled]):not(.disabled):active, .show>.btn-primary.dropdown-toggle {
    color: #fff;
    background-color: #0062cc;
    border-color: #005cbf;
}

.login-form .btn {
    width: 100%;
    text-transform: uppercase;
    font-size: 14px;
    padding: 15px;
    border: 0px;
}

.btn-success {
    color: #fff;
    background-color: #28a745;
    border-color: #007bff;
    background-image: none !important;
    border-radius: 0px !important;
}

.login-form .checkbox {
    color: #878787;
}

.login-form .btn {
    width: 100%;
    text-transform: uppercase;
    font-size: 14px;
    padding: 15px;
    border: 0px;
}

.btn-primary:hover {
    color: #fff;
    background-color: #0069d9;
    border-color: #0062cc;
}

.mb-3, .my-3 {
    margin-bottom: 16px!important;
}

.mt-2, .my-2 {
    margin-top: 8px!important;
}

@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../../static/assets/scss/style.css';
@import '../../static/assets/css/lib/vector-map/jqvmap.min.css';
</style>
