<template>

<!-- Outer div -->
<div class="main_table">
    <!-- Left Panel -->
    <aside id="left-panel" class="left-panel">
        <nav class="navbar navbar-expand-sm navbar-default">

            <div class="navbar-header">
                <a class="navbar-brand" href="./"><img src="../assets/images/theme_logo_text.png" alt="Logo"></a>
                <a class="navbar-brandy" href="./"><img class="menuToggleLogoImg" src="../assets/images/theme_logo_box.png" alt="Logo"></a>
            </div>

            <div id="main-menu" class="main-menu collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="#" @click="home"><i class="li-icon fa fa-dashboard"></i>Home</a></li>
                    <li>
                        <a v-if="profile_link != undefined" :href="profile_link"><i class="li-icon fa fa-user-circle"></i>My Profile</a>
                        <a v-else href="/login/"><i class="li-icon fa fa-key"></i>Sign In</a>
                    </li>
                    <li><a v-if="profile_link == undefined" href="/register/"><i class="li-icon fa fa-address-card"></i>Register</a></li>
                    <li><a href="#" @click="Contact_us"><i class="li-icon fa fa-phone"></i>Contact Us</a></li>
                    <li><a href="#" @click="about_us"><i class="li-icon fa fa-info-circle"></i>About Us</a></li>
                    <li><a v-if="profile_link != undefined" href="#" @click="logout"><i class="li-icon fa fa-power-off"></i>Sign Out</a></li>
                </ul>
            </div>
        </nav>
    </aside>

    <!-- Right Panel -->
    <div id="right-panel" class="right-panel">
        
        <!-- Home Page -->
        <div id="home" class="col-lg-8 col-md-8 col-sm-8 col-md-offset-2 col-lg-offset-2  page-tab paper-left" >
            <div>&nbsp;</div>
            <div>&nbsp;</div>
            <div><span style="font-family: arial, helvetica, sans-serif; font-size: 24pt; color: #800080;">Welcome to SkillStash!</span></div>

            <a class="navbar-brand0" > <img src="../assets/images/theme_logo_box.png" alt="Logo"></a>
        </div>

        <!-- Contact Us -->
        <div class="content mt-3 page-tab" id="Contactus" hidden>
             <div  class="paper-left" >
<div>
<div style="text-align: center;">
<div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div><span style="font-size: 13pt;">You can always contact us via email:</span></div>
<div><span style="font-size: 13pt;"> <a href="mailto:hello@skillstash.com">hello@skillstash.com</a></span></div>
<div><span style="font-size: 13pt;">Or via phone 02 458 982 278</span></div>
<div>&nbsp;</div>
<div><span style="font-size: 13pt;">We are always eager to hear your feedback and any recommendations regarding our service</span></div>
</div>
</div>
</div>
            </div>
        </div>
        <div class="content mt-3 page-tab" id="Aboutus" hidden>
            <div  class="paper-left" >
    <label>  <div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif; font-size: 14pt;">Nowadays the recruitment process is very sophisticated and complex for all participants: potential employees, hiring companies, and recruiters. We have identified major reasons why this is happening in the industry.</span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><strong><span style="font-family: arial, helvetica, sans-serif;">High variety of skills</span></strong></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Many people have very diverse experience and often their skills vary in many subjects and fields. While many portals allow candidates to choose &lsquo;up to three&rsquo; core skills, some people can count dozens. This issue is very important, as it expands the skillsets to a potentially unlimited number of fields.</span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;"><strong>Unstructured data in CVs</strong></span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Most of CVs are structured in a </span>personalised<span style="font-family: arial, helvetica, sans-serif;"> way, which makes it very difficult to extract any data from them. It is crucial for employers and recruiters to see the previous experience and educational background in order to judge on candidate&rsquo;s skills.</span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;"><strong>Evidence for the skills</strong></span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Unfortunately, many candidates understand that recruiting companies and employers will not be able to verify the skills of potential employees, so they exaggerate or even falsify their skills. This leads to wasted time during </span>recruitment<span style="font-family: arial, helvetica, sans-serif;"> and unfair hiring.</span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;"><strong>Overly specific requirements for candidates</strong></span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Employers tend to demand a lot from their candidates, and very often requirements are overly specific not only in terms of hard </span>skills<span style="font-family: arial, helvetica, sans-serif;"> but also in terms of soft skills. This leads to higher difficulty finding a matching candidate.</span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;"><strong>Recruiters are dependent on their networks</strong></span></div>
<div style="text-align: center;">&nbsp;</div>
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Recruiters have limited professional networks, and have to </span>spend<span style="font-family: arial, helvetica, sans-serif;"> time constantly updating their databases, so they lack time to focus on the quality of candidates and job offers.</span></div>
<br />
<div style="text-align: center;"><span style="font-size: 12pt; font-family: arial, helvetica, sans-serif;">We are aiming to create the system, where all three sides: candidates, employers and recruiters are feeling </span>the ease<span style="font-size: 12pt; font-family: arial, helvetica, sans-serif;"> to work with and all of their priorities are considered. </span>The system<span style="font-size: 12pt; font-family: arial, helvetica, sans-serif;"> must gather skills from candidates, offering the choice from a </span>categorised<span style="font-size: 12pt; font-family: arial, helvetica, sans-serif;"> and structured list of options. Employers can post </span>job<span style="font-size: 12pt; font-family: arial, helvetica, sans-serif;"> requirements, based on the skills they need, proficiency of those skills and the experience, but also in a structured way</span></div>
<br />
<div style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Recruiters should be able to use the system as a great search tool for jobs and candidates, be able to mark their proposed candidate to track their performance and be able to prove a referral.</span></div>
<div>&nbsp;</div>
</div>
</label>
</div>

     </div>
    </div>    
</div>

</template>


<script>
import 'font-awesome/css/font-awesome.min.css'
import '../../static/assets/css/build.css'
import '../../static/assets/js/bootstrap-select.min.js'
//import '../../static/assets/js/main.js'
import axios from 'axios'
import $ from 'jquery'
import TreeNode from './TreeNode'
import ProfileAvatar from './ProfileAvatar'
import JobCard from '@/components/JobCard'
export default {
    name: 'MainPage',
    computed: {
        profile_link() {
            var role = sessionStorage.getItem("user_role");
            if (role == 'C')
                return "/candidate-profile/";
            if (role == 'E')
                return "/employer-profile/";
            if (role == 'R')
                return "/recruiter-profile/";
            return undefined;
        }
    },
    methods: {
        Contact_us() {
            $('.page-tab').hide()
            $('#Contactus').show()
        },
        home() {
            $('.page-tab').hide()
            $('#home').show()
        },
        about_us() {
            $('.page-tab').hide()
            $('#Aboutus').show()
        },
        logout() {
            axios({
                method: 'post',
                url: API_HOST + '/rest-auth/logout/',
                params: {}
            }).then(response => {
                sessionStorage.clear();
                this.$router.push({
                    path: '/login'
                })
            })
        },
    }
}

</script>

<style lang="scss">
.content {
    align-content: center;
}

.navbar-expand-sm .navbar-nav .dropdown-menu {
    position: absolute;
}

.navbar .navbar-nav li.menu-item-has-children .sub-menu {
    background: #272c33;
    border: none;
    box-shadow: none;
    overflow-y: hidden;
    padding: 0 0 0 35px;
}

div a.navbar-brand0  {
    position: absolute;
    left: 320px;  
    top: 150px; 
    width: 200px;
    height: 200px;
}

.paper-left,
.paper-right {
    display: flex;
    flex-direction: column;
    -ms-flex-direction: column;
    width: 50%;
    text-align-last: center;
}

</style>

<style scoped>

@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../../static/assets/scss/style.css';
@import '../../static/assets/css/lib/vector-map/jqvmap.min.css';
@import '../assets/css/skillstash.css';

</style>
