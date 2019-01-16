<!-- Registration page -->
<template>
<div class="page-content bg-dark d-flex align-content-center">
    <div class="register-content">

        <!-- Logo. -->
        <div class="logo-text">
            <a href="/">
                <img class="align-content" src="../assets/images/theme_logo_text.png" alt="SkillStash">
            </a>
        </div>

        <!-- Registration form. -->
        <div class="register-form">

            <!-- Registration type. -->
            <div class="tab">
                <button id="tab-candidate" class="tablinks" @click="selectUserRole('C')">Candidate</button>
                <button id="tab-employer" class="tablinks" @click="selectUserRole('E')">Employer</button>
                <button id="tab-recruiter" class="tablinks" @click="selectUserRole('R')">Recruiter</button>
            </div>

            <!-- User input. -->
            <div class="input-form">
                <form @submit.prevent="submit" role="form">
                    <label class="uppercase-label">Personal Details</label>
                    <!-- First name. -->
                    <div class="form-group has-feedback ">
                        <input title="First name" type="text" class="form-control" name="firstname" placeholder="First name" v-model="first_name" @change="enableSubmitIfReady" />
                        <i class="glyphicon glyphicon-user form-control-feedback"></i>
                    </div>

                    <!-- Last name. -->
                    <div class="form-group has-feedback ">
                        <input title="Last name" type="text" class="form-control" name="lastname" placeholder="Last name" v-model="last_name" @change="enableSubmitIfReady" />
                        <i class="glyphicon glyphicon-user form-control-feedback"></i>
                    </div>

                    <!-- Email. -->
                    <div class="form-group has-feedback">
                        <input title="E-mail" class="form-control eamil" type="text" name="email" placeholder="E-mail" v-model="email" @change="enableSubmitIfReady" />
                        <i class="glyphicon glyphicon-envelope form-control-feedback"></i>
                    </div>

                    <!-- Phone. -->
                    <div class="form-group has-feedback">
                        <input title="Phone" class="form-control phone" type="text" placeholder="Phone" v-model="phone" />
                        <i class="glyphicon glyphicon-phone form-control-feedback"></i>
                    </div>

                    <!-- City. -->
                    <div class="form-group">
                        <input title="City" class="form-control" type="text" name="city" placeholder="City" v-model="city" @change="enableSubmitIfReady" />
                    </div>

                    <!-- Candidate Fields (hidden). -->
                    <div class="form-group" id="candidate-fields" style="display:none">
                        <!-- eductaion -->
                        <div title="Highest education" class="form-group" id="education" >
                            <select class="select-form" v-model="highest_education">
                                <option value="" disabled selected hidden>Highest Education</option>
                                <option value=1>High School</option>
                                <option value=2>Certificate</option>
                                <option value=3>Associate Diploma</option>
                                <option value=4>Diploma</option>
                                <option value=5>Bachelor's Degree</option>
                                <option value=6>Graduate Certificate</option>
                                <option value=7>Graduate Diploma</option>
                                <option value=8>Master's Degree</option>
                                <option value=9>Ph.D</option>
                                <option value=0>None of the above</option>
                            </select>
                        </div>

                        <div class="labelled-personal-input">
                            <!-- date of birth-->
                            <div id="dob-form" >
                                <label class="uppercase-label">Date of Birth</label>
                                <input title="Date of Birth" class="form-control" type="date" name="bdate" style="text-transform:uppercase" v-model="dob" @change="enableSubmitIfReady" />
                            </div>
                            
                            <!-- gender -->
                            <div id="gender-form" >
                                <label class="uppercase-label">Gender</label>
                                <div class='radio-group form-control'>
                                    <label class='radio-label'>
                                        <input type='radio' id="ns" value="N" v-model="gender" checked>
                                        <span class='inner-label'>Not Specified</span>
                                    </label>
                                    
                                    <label class='radio-label'>
                                        <input type='radio' id='male' value="M" v-model="gender">
                                        <span class='inner-label'>Male</span>
                                    </label>
                                    <label class='radio-label'>
                                        <input type='radio' id='female' value="F" v-model="gender">
                                        <span class='inner-label'>Female</span>
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <label class="uppercase-label">Preferences</label>
                        <!-- min salary -->
                        <input title="Minimum annual salary" class="form-control" type="number" min="0" placeholder="Minimum annual salary" v-model="minimum_salary" />
                        
                        <!-- looking for work -->
                        <div class="checkbox">
                            <input type="checkbox" id="looking-for-work-checkbox" v-model="looking_for_work">
                            <label class="lowercase-label" for="looking-for-work-checkbox">I am currently looking for work.</label>
                        </div>
                    </div>

                    <!-- Employer / Recruiter Fields (hidden). -->
                    <div class="form-group" id="employer-fields" style="display:none">
                        <label class="uppercase-label">Corporate Details</label>
                        <div class="form-group has-feedback ">
                            <input title="Company" class="form-control" type="text" placeholder="Company" v-model="company" />
                        </div>
                        <div class="form-group has-feedback ">
                            <input title="Website" class="form-control" type="text" placeholder="Website" v-model="website" />
                        </div>
                    </div>

                    <!-- Password. -->
                    <div class="form-group has-feedback">
                        <label class="uppercase-label">Password</label>
                        <input title="Password" class="form-control" type="password" placeholder="Password" name="password1" v-model="password1" @change="enableSubmitIfReady" />
                        <i class=" glyphicon glyphicon-lock form-control-feedback"></i>
                        </div>

                        <div class="form-group has-feedback">
                        <input title="Verify password" class="form-control" type="password" placeholder="Verify password" name="password2" v-model="password2" @change="enableSubmitIfReady" />
                        <i class=" glyphicon glyphicon-lock form-control-feedback"></i>
                    </div>

                    <!-- Submission. -->
                    <div class="checkbox">
                        <input type="checkbox" id="t-and-c-checkbox" @change="enableSubmitIfReady">
                        <label for="t-and-c-checkbox">I agree to the terms and conditions.</label>
                    </div>

                    <button type="submit" disabled class="btn btn-primary btn-flat m-b-30 m-t-30" id="submit-button">Register</button>
                    
                    <div class="register-link text-center">
                        <p>Already have an account? <a href="/login">Sign in</a>!</p>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</template>

<!-- JavaScript -->
<script>
import 'font-awesome/css/font-awesome.min.css'
import $ from 'jquery'
import '../../static/assets/scss/style.css'
import '../../static/assets/css/themify-icons.css'
//import '../../static/assets/js/main.js'
import axios from 'axios'
export default {
    name: "Registration",
    data() {
        return {
            loading: false,
            role: '',
            first_name: '',
            last_name: '',
            city: '',
            email: '',
            phone: '',
            gender: 'N',  // to be shown selected at load
            highest_education: '',
            looking_for_work: true,
            minimum_salary: '',
            password1: '',
            password2: '',
            dob: '',
            company: '',
            website: ''
        };
    },
    methods: {
        submit() {
            if (this.password1 != this.password2) {
                $('.help-block').remove()
                $("input[name='password2']").parent().append('<small data-bv-validator="notEmpty" data-bv-validator-for="password2" class="help-block">Passwords do not match</small>');
                return;
            }
            axios({
                    method: 'post',
                    url: API_HOST +'/rest-auth/registration/',
                    data: {
                        "role": this.role,
                        "first_name": this.first_name,
                        "last_name": this.last_name,
                        "email": this.email.toLowerCase(),
                        "phone": this.phone,
                        "password1": this.password1,
                        "password2": this.password2,
                        "city": this.city,
                        "date_of_birth": this.dob,
                        "gender": this.gender,
                        "highest_education": this.highest_education,
                        "minimum_salary": this.minimum_salary,
                        "looking_for_work": this.looking_for_work,
                        "company": this.company,
                        "website": this.website
                    }
                })
                .then((response) => {
                    console.log(response)
                    if (response.status === 200 || response.status === 201) {
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
                    var response = error.response
                    var errordata = response.data
                    $('.help-block').remove()
                    for (var key in errordata){
                        console.log(key + ':' + errordata[key])
                        $("input[name='"+key+"']").parent().append('<small data-bv-validator="notEmpty" data-bv-validator-for="'+key+'" class="help-block">' +  errordata[key] + '</small>');
                    }
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
        },
        setVisibleFields() {
            var c_fields = document.getElementById("candidate-fields");
            // We can use employer-fields for recruiters too since they have the same attributes.
            // This dialog is due to vbe reworked anyway.
            var e_fields = document.getElementById("employer-fields");
            if (this.role == 'C') {
                c_fields.style.display = "block";
                e_fields.style.display = "none";
            } else {
                c_fields.style.display = "none";
                e_fields.style.display = "block";
            }
            this.enableSubmitIfReady();
        },
        selectUserRole(user_role) {
            $('.tablinks').removeClass('tab-pressed')
            if (user_role === 'C') {
                $('#tab-candidate').addClass('tab-pressed')
            } else if (user_role === 'E') {
                $('#tab-employer').addClass('tab-pressed')
            } else if (user_role === 'R') {
                $('#tab-recruiter').addClass('tab-pressed')
            }
            this.role = user_role
            this.setVisibleFields()
        },
        enableSubmitIfReady() {
            document.getElementById("submit-button").disabled =
                this.role == '' || this.first_name == '' || this.last_name == '' ||
                this.email == '' || this.password1 == '' || this.password2 == '' ||
                this.city == '' || (this.role == 'C' && this.dob == '') ||
                !document.getElementById("t-and-c-checkbox").checked;
        }
    },
    mounted() {
        this.loading = false
        this.selectUserRole('C')
        sessionStorage.clear();
    }
};
</script>

<!-- CSS -->
<style lang="scss" scoped>
@import '../assets/css/skillstash.css';

/* page content */
.register-content {
    min-width: 510px;
    max-width: 560px;
    margin: 0 auto;
}

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

.register-form {
    border: solid;
    border-color: var(--primary-color);
    border-width: 2px;
    margin-bottom: 20px;
    border-radius: 2px;
}

.logo-text {
    padding: 55px 0px 30px 0px;
    margin: 0px 25px;
}

/* tabs */
.tab {
    overflow: hidden;
    border: none;
    background-color: var(--primary-light);
    display: flex;  
    font-family: var(--theme-font-head);
    font-weight: normal;
    font-size: medium;
}

.tab-pressed {
    background-color: var(--primary-color) !important;
    color: var(--light-gray) !important;
}

.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    width: stretch;
    transition: 0.3s;
    color: var(--dark-bg-color);
    text-transform: uppercase;
}

.tab button:hover {
    background-color: var(--primary-color) !important;
    color: var(--light-gray);
}

/* user input form */
.input-form {
    background: var(--light-bg-color);
    padding: 30px 30px 20px;
}

.labelled-personal-input {
    margin-bottom: 15px;
}

#dob-form {
    display: inline-block;
    width: 37%;
    margin-right: 3%;
    vertical-align: top;
}

#gender-form {
    display: inline-block;
    width: 59%;
    vertical-align: top;
}

.radio-label {
    padding-right: 10px;
    text-transform: initial;
    font-weight: normal;
    display: inline;
}

.radio-group {
    min-width: 59%;
}

.select-form {
    width: stretch;
    height: 34px;
    background-color: var(--light-gray);
}

.input-form .btn {
    width: 100%;
    text-transform: uppercase;
    font-size: 14px;
    padding: 15px;
    border: 0px;
}

.input-form .btn {
    width: 100%;
    text-transform: uppercase;
    font-size: 14px;
    padding: 15px;
    border: 0px;
}

.btn-primary:hover {
    color: #fff;
    background-color: var(--primary-color);
    border-color: var(--primary-dark) !important;
}

@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../../static/assets/scss/style.css';
@import '../../static/assets/css/lib/vector-map/jqvmap.min.css';
</style>
