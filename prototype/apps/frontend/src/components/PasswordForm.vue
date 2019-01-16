<template>
<div class="form row">
    <form @submit.prevent="submit" class="form-horizontal">
        <div class="col-xs-10 col-sm-10 col-sm-offset-1 col-md-10 col-lg-10 col-xs-offset-1 col-md-offset-1 col-lg-offset-1">
            <div class="form-group">
                <h3 class="form-title">Change Password</h3>
            </div>
            <div class="form-group has-feedback">
                <input class="form-control required" type="password" placeholder="New Password" name="new_password1" v-model="password1" />
                <i class=" glyphicon glyphicon-lock form-control-feedback"></i>
            </div>
            <div class="form-group has-feedback">
                <input class="form-control required" type="password" placeholder="Verify password" name="new_password2" v-model="password2" />
                <i class=" glyphicon glyphicon-lock form-control-feedback"></i>
            </div>
            <div class="form-group">
                <button type="submit" class="btn btn-primary btn-flat m-b-30 m-t-30" id="change_pw">Change Password</button>
            </div>
        </div>
    </form>
</div>
</template>

<script>
import 'font-awesome/css/font-awesome.min.css'
import $ from 'jquery'
import '../../static/assets/scss/style.css'
import '../../static/assets/css/themify-icons.css'
import "../assets/css/skillstash.css";
import axios from 'axios'
export default {
    name: "registration",
    data() {
        return {
            password1: '',
            password2: ''
        };
    },
    methods: {
        submit() {
            $('.help-block').remove()
            if (this.password1.length == 0) {
                $("input[name='new_password1']").parent().append('<small data-bv-validator="notEmpty" data-bv-validator-for="password1" class="help-block">Password cannot be blank.</small>');
                return;
            }
            if (this.password1 != this.password2) {
                $("input[name='new_password2']").parent().append('<small data-bv-validator="notEmpty" data-bv-validator-for="password2" class="help-block">Passwords do not match.</small>');
                return;
            }
            axios({
                method: 'post',
                url: API_HOST +'/rest-auth/password/change/',
                data: {
                    "new_password1": this.password1,
                    "new_password2": this.password2,
                }
            }).then((response) => {
                console.log(response)
                if (response.status === 200) {
                    alert("Your password has been changed.")
                }
            }).catch(function (error) {
                // There will probably only be a single error message, but support multiple.
                var errordata = error.response.data
                for (var key in errordata){
                    $("input[name='"+key+"']").parent().append('<small data-bv-validator="notEmpty" data-bv-validator-for="'+key+'" class="help-block">' +  errordata[key] + '</small>');
                }
            })
        }
    }
};
</script>
