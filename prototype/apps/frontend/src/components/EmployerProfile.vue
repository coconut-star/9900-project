<template>
<div class="main_table">
    <!-- Left Panel -->

    <aside id="left-panel" class="left-panel">
        <nav class="navbar navbar-expand-sm navbar-default">
            <div class="navbar-header">
                <a class="navbar-brand" href="/"><img src="../assets/images/theme_logo_text.png" alt="Text"></a>
            </div>

            <div class="profile clearfix">
              <div class="profile_pic">
                <img class="img-circle profile_img" :src="profile_photo" v-if="profile_photo" alt="User Avatar">
                <img class="img-circle profile_img" src="../assets/images/default.png" v-else alt="User Avatar">
              </div>
            </div>

            <div id="main-menu" class="main-menu collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/home/"> <i class="li-icon fa fa-dashboard"></i>Home</a></li>
                    <li><a href="#" @click="edit_profile"><i class="li-icon fa fa-user-circle"></i>Profile</a></li>
                    <li><a href="#" @click="change_password"><i class="li-icon fa fa-key"></i>Change Password</a></li>
                    <li><a href="#" @click="post_jobs_tab"><i class="li-icon fa fa-briefcase "></i>Job Posts</a></li>
                    <li><a href="#" @click="view_job_matches"><i class="li-icon fa fa-bars"></i>Job Matches</a></li>
                    <li><a href="#" @click="view_search_candidates"><i class="li-icon fa fa-search"></i>Search for Candidates</a></li>
                    <li><a href="#" @click="logout"><i class="li-icon fa fa-power-off"></i>Sign Out</a></li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>
    </aside>

    <div id="right-panel" class="right-panel">
        <div id="jobs" class="page-tab" hidden>
            <div class="post-job-form col-md-6 col-sm-6 col-lg-6 col-md-offset-3 col-lg-offset-3">
                <div class="form-group">
                    <h3 class="form-title">Post a Job</h3>
                </div>
                <form @submit.prevent="post_job" role="form">
                    <div class="form-group has-feedback ">
                        <input type="text" class="form-control" placeholder="Job Name" v-model="name" />
                        <i class="form-control-feedback"></i>
                    </div>
                    <div class="form-group has-feedback ">
                        <input type="text" class="form-control" name="description" placeholder="Description" v-model="description" />
                        <i class="form-control-feedback"></i>
                    </div>
                    <div class="form-group">
                        <input class="form-control required" type="text" placeholder="City" v-model="city" />
                    </div>
                    <div class="form-group">
                        <label>Required Education</label>
                        <select v-model="required_education">
                            <option value=0>No Requirement</option>
                            <option value=1>High School</option>
                            <option value=2>Certificate</option>
                            <option value=3>Associate Diploma</option>
                            <option value=4>Diploma</option>
                            <option value=5>Bachelor's Degree</option>
                            <option value=6>Graduate Certificate</option>
                            <option value=7>Graduate Diploma</option>
                            <option value=8>Master's Degree</option>
                            <option value=9>Ph.D</option>
                        </select>
                    </div>
                    <div class="form-group pay-fields">
                        <label>Pay</label>
                        <input class="form-control" type="text" placeholder="Pay" v-model="pay" />
                        <label>per</label>
                        <select title="Pay Type" v-model="pay_type" data-live-search="false" data-size="4" single>
                            <option value="H">Hour</option>
                            <option value="D">Day</option>
                            <option value="M">Month</option>
                            <option value="Y">Year</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary btn-flat m-b-30 m-t-30">Post Job</button>
                </form>
            </div>

            <div class="filter-bar">
                <label>Show</label>
                <select v-model="job_state" @change="filter_job_posts()">
                    <option value="Active">Active Job Posts</option>
                    <option value="All">All Job Posts</option>
                    <option value="Inactive">Inactive Job Posts</option>
                    <option value="W">Withdrawn Job Posts</option>
                    <option value="F">Filled Job Posts</option>
                </select>
                <label>City</label>
                <input type="text" class="form-control" v-model="job_city" @change="filter_job_posts()">
                <label>Name Contains</label>
                <input type="text" class="form-control" v-model="job_name" @change="filter_job_posts()">
                <label>Sort by</label>
                <select v-model="job_sort_field" @change="sort_job_posts()">
                    <option value="Name">Name</option>
                    <option value="City">City</option>
                    <option value="Date">Date Posted</option>
                    <option value="State">State</option>
                </select>
                <select v-model="job_sort_order" @change="sort_job_posts()">
                    <option value="Ascending">Ascending</option>
                    <option value="Descending">Descending</option>
                </select>
            </div>

            <div class="content mt-3" id="jobposts">
                <div class="card" v-for="(job,index) in filtered_job_posts" :key=index>
                    <div class="card-header">
                        <i class="mr-2 fa fa-align-justify"></i>
                        <strong class="card-title">{{job.name}}</strong>
                        <ul>
                            <li>{{job.city}}</li>
                            <li>Posted {{job.date_posted}}</li>
                            <li>{{job_state_name(job)}}</li>
                        </ul>
                        <span @click="remove_job(job)" class="glyphicon glyphicon-remove pull-right"></span>
                        <span @click="update_job(job)" class="glyphicon glyphicon-edit pull-right"></span>
                    </div>
                    <div class="card-body" v-bind:id="'job'+job.id" hidden>
                        <div class="col-md-6 col-sm-6 col-lg-6 col-md-offset-3 col-lg-offset-3">
                            <form @submit.prevent="save_job(job)" role="form">
                                <div class="form-group">
                                    <label class="control-label">Name : </label>
                                    <input :disabled="!can_update_job(job)" type="text" class="form-control" placeholder="Job Name" v-model="job.name" />
                                </div>
                                <div class="form-group">
                                    <label class="control-label ">Description : </label>
                                    <input :disabled="!can_update_job(job)" type="text" class="form-control " placeholder="Job Description" v-model="job.description" />
                                </div>
                                <div class="form-group">
                                    <label class="control-label">City : </label>
                                    <input :disabled="!can_update_job(job)" type="text" class="form-control " placeholder="City" v-model="job.city" />
                                </div>
                                <div class="form-group">
                                    <label>Required Education</label>
                                    <select :disabled="!can_update_job(job)" v-model="job.required_education">
                                        <option value=0>No Requirement</option>
                                        <option value=1>High School</option>
                                        <option value=2>Certificate</option>
                                        <option value=3>Associate Diploma</option>
                                        <option value=4>Diploma</option>
                                        <option value=5>Bachelor's Degree</option>
                                        <option value=6>Graduate Certificate</option>
                                        <option value=7>Graduate Diploma</option>
                                        <option value=8>Master's Degree</option>
                                        <option value=9>Ph.D</option>
                                    </select>
                                </div>
                                <div class="form-group pay-fields">
                                    <label>Pay</label>
                                    <input :disabled="!can_update_job(job)" class="form-control" type="text" placeholder="Pay" v-model="job.pay" />
                                    <label>per</label>
                                    <select :disabled="!can_update_job(job)" title="Pay Type" v-model="job.pay_type" data-live-search="false" data-size="4" single>
                                        <option value="H">Hour</option>
                                        <option value="D">Day</option>
                                        <option value="M">Month</option>
                                        <option value="Y">Year</option>
                                    </select>
                                </div>
                                <!-- Do no allow editing of withdrawn or filled jobs. -->
                                <button v-if="can_update_job(job)" type="submit" class="btn btn-primary btn-flat m-b-30 m-t-30">Save Changes</button>
                            </form>
                        </div>
                    </div>
                    <div v-if="can_update_job(job)" class="card-body">
                        <button @click="create_matches(job)" type="button" class="btn btn-secondary mb-1">
                            Automatically Find Candidates
                        </button>
                        <button @click="withdraw_job(job)" type="button" class="btn btn-secondary mb-1">
                            Withdraw Job
                        </button>
                    </div>
                    <div class="card-body">
                        <div v-if="can_update_job(job)" class="tree-box" v-bind:id="'jobskills'+job.id">
                            <h3>All Skills</h3>
                            <ul class="skill-tree" v-for="(td,index) in treeData" :key="index">
                                <tree-node :model="td"></tree-node>
                            </ul>
                        </div>

                        <div class="skill-panel">
                            <h3>Skill Requirements</h3>
                            <table class="skill-table">
                                <thead>
                                    <tr>
                                        <th>Skill</th>
                                        <th>Priority</th>
                                        <th>Proficiency</th>
                                        <th>Experience</th>
                                    </tr>
                                </thead>
                                <tr v-if="job.skills.length != 0" v-for="(js,index) in job.skills" :key="index">
                                    <td>{{js.skill.name}}</td>
                                    <td>
                                        <select :disabled="!can_update_job(job)" data-placeholder="..." v-model="js.priority" data-width="auto" tabindex="-1"
                                            @change="mark_skill_changed(js)">
                                            <option value=1>1</option>
                                            <option value=2>2</option>
                                            <option value=3>3</option>
                                            <option value=4>4</option>
                                            <option value=5>5</option>
                                        </select>
                                    </td>
                                    <td>
                                        <select :disabled="!can_update_job(job)" data-placeholder="..." v-model="js.proficiency" data-width="auto" tabindex="-1"
                                            @change="mark_skill_changed(js)">
                                            <option value=1>1</option>
                                            <option value=2>2</option>
                                            <option value=3>3</option>
                                            <option value=4>4</option>
                                            <option value=5>5</option>
                                        </select>
                                    </td>
                                    <td class="experience-cell">
                                        <input :disabled="!can_update_job(job)" class="form-control" id="experience" type="number" min="0" v-model="js.experience"
                                            @change="mark_skill_changed(js)"/>
                                        <select :disabled="!can_update_job(job)" v-model="js.experience_unit" @change="mark_skill_changed(js)">
                                            <option value=12>Years</option>
                                            <option value=1>Months</option>
                                        </select>
                                    </td>
                                    <td v-if="can_update_job(job)">
                                        <a v-on:click="remove_skill_from_job(job, js, index)">
                                            <span class="glyphicon glyphicon-remove"></span>
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <div v-if="can_update_job(job)" >
                                <button type="button" class="btn" @click='add_skills_to_job(job)'>Add Selected Skills</button>
                                <button type="button" class="btn" @click="save_job_skill_changes(job)">Save Changes</button>
                                <button type="button" class="btn" @click="revert_job_skills(job)">Revert Unsaved Changes</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="profile_tab" class="profile-card page-tab col-sm-12 col-md-8 col-md-offset-2 col-lg-6 col-lg-offset-3" hidden>
            <div style="padding: 30px;">
                <form @submit.prevent="update_profile" class="form-horizontal">
                    <h3 class="profile-title">Profile</h3>
                    <div class="profile-content">
                        <div class="profile-avatar-col">
                            <profile-avatar v-on:avatar_changed="parent_avatar_changed" :profile_photo="profile_photo"></profile-avatar>
                        </div>
                        <div class="form col-sm-offset-1 col-md-offset-1 col-lg-offset-1 col-sm-10 col-md-10 col-lg-10" v-if="employer">
                            <div class="form-group has-feedback ">
                                <label>First Name</label>
                                <input type="text" v-model="employer.user.first_name" class="form-control" placeholder="First Name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback ">
                                <label>Last Name</label>
                                <input type="text" v-model="employer.user.last_name" class="form-control" placeholder="Last Name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>Email</label>
                                <input class="form-control email" v-model="employer.user.email" type="text" placeholder="Email" />
                                <i class="glyphicon glyphicon-envelope form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>Phone</label>
                                <input class="form-control phone" type="text" placeholder="Phone" v-model="employer.user.phone" />
                                <i class="glyphicon glyphicon-phone form-control-feedback"></i>
                            </div>
                            <div class="form-group">
                                <label>City</label>
                                <input class="form-control required" type="text" v-model="employer.user.city" placeholder="City" />
                            </div>
                            <div class="form-group">
                                <label>Company</label>
                                <input class="form-control" type="text" v-model="employer.company" placeholder="Company" />
                            </div>
                            <div class="form-group">
                                <label>Website</label>
                                <input class="form-control required" type="text" v-model="employer.website" placeholder="Website" />
                            </div>
                            <div class="form-group">
                                <input type="submit" class="btn btn-info" value="Update Profile" />
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <div id="password_tab" style="display: none;" class="col-xs-12 col-sm-10 col-md-10 col-lg-8 col-sm-offset-1 col-md-offset-1 col-lg-offset-2 page-tab shadow-paper" >
            <password-form />
        </div>

        <div id="candidate-matched-list" class="page-tab" hidden>
            <div class="filter-bar">
                <label>Show matches for</label>
                <select v-model="match_job" @change="filter_job_matches()">
                    <option value="">All Jobs</option>
                    <option v-for="(job, index) in all_job_posts" :value="job.id" :key="index">{{job.name}}</option>
                </select>
                <label>State</label>
                <select v-model="match_state" @change="filter_job_matches()">
                    <option value="Active">Active</option>
                    <option value="All">All</option>
                    <option value="Inactive">Inactive</option>
                    <option value="N">No Action Taken</option>
                    <option value="CI">Candidate Interested</option>
                    <option value="EI">Employer Interested</option>
                    <option value="DC">Declined by Candidate</option>
                    <option value="DE">Declined by Employer</option>
                    <option value="P">In Progress</option>
                    <option value="J">Job Offer Made</option>
                    <option value="JD">Job Offer Declined</option>
                    <option value="F">Position Filled</option>
                    <option value="W">Position Withdrawn</option>
                    <option value="H">Hired</option>
                </select>
                <label>Sort by</label>
                <select v-model="match_sort_field" @change="sort_job_matches()">
                    <option value="Score">Suitability Score</option>
                    <option value="C_F_Name">Candidate First Name</option>
                    <option value="C_L_Name">Candidate Last Name</option>
                    <option value="J_Name">Job Name</option>
                    <option value="J_Date">Job Posting Date</option>
                </select>
                <select v-model="match_sort_order" @change="sort_job_matches()">
                    <option value="Ascending">Ascending</option>
                    <option value="Descending">Descending</option>
                </select>
            </div>
            <div class="card-table">
                <CandidateCard :match="match" v-for="match in filtered_job_matches" :key="match.id" v-on:candidate_clicked="change_detail_previous_page('match');view_candidate_details(match.candidate)" />
                <div class="no-matches" v-if="!filtered_job_matches || filtered_job_matches.length===0">
                    <h2>Sorry, we didn't find any job matches.</h2>
                </div>
            </div>
        </div>

        <div id="candidate-details-tab" class="page-tab" hidden>
            <candidate-details v-if="selected_candidate != null" :candidate="selected_candidate" v-on:close_clicked="close_candidate_details" />
        </div>

        <div id="search-candidates-tab" class="page-tab shadow-paper col-md-12 col-lg-12" hidden>
            <div class="paper-up">
                <div id="candidate-skill-tree" class="paper-left">
                    <label>Skills</label>
                    <ul v-for="(td,index) in treeData" :key="index">
                        <tree-node :model="td"></tree-node>
                    </ul>
                </div>
                <div class="paper-right">
                    <div class="form row right-container">
                        <form @submit.prevent="search_candidates" class="form-horizontal">
                            <legend>Choose the best candidate for your job:</legend>
                            <div class="">
                                <!-- City selection. -->
                                <div class="form-group">
                                    <label>Cities</label>
                                    <input type="text" v-model="cities" class="form-control" placeholder="Candidates's location">
                                </div>
                                <!-- First name selection. -->
                                <div class="form-group">
                                    <label>First Name</label>
                                    <input type="text" v-model="first_name" class="form-control" placeholder="Candidate's first name">
                                </div>
                                <!-- Last name selection. -->
                                <div class="form-group">
                                    <label>Last Name</label>
                                    <input type="text" v-model="last_name" class="form-control" placeholder="Candidate's last name">
                                </div>
                                <!-- E-mail selection. -->
                                <div class="form-group">
                                    <label>E-mail</label>
                                    <input type="text" v-model="email" class="form-control" placeholder="Candidate's email">
                                </div>
                                <!-- Gender selection. -->
                                <div class="form-group">
                                    <label>Gender</label>
                                    <select class="select" title="gender" v-model="gender" data-live-search="false" data-size="3" single>
                                        <option value="">Any Gender</option>
                                        <option value="M">Male</option>
                                        <option value="F">Female</option>
                                    </select>
                                </div>
                                <!-- Education selection. -->
                                <div class="form-group" id="education">
                                    <label>Highest Education</label>
                                    <select v-model="highest_education">
                                        <option value=0>Any Level of Education</option>
                                        <option value=1>High School</option>
                                        <option value=2>Certificate</option>
                                        <option value=3>Associate Diploma</option>
                                        <option value=4>Diploma</option>
                                        <option value=5>Bachelor's Degree</option>
                                        <option value=6>Graduate Certificate</option>
                                        <option value=7>Graduate Diploma</option>
                                        <option value=8>Master's Degree</option>
                                        <option value=9>Ph.D</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <input type="submit" class="btn btn-info" value="Search" />
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="paper-down ">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Gender</th>
                            <th>DoB</th>
                            <th>Profile</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(candidate,index) in candidates" :key="index">
                            <td>{{candidate.user.first_name}} {{candidate.user.last_name}}</td>
                            <td>{{candidate.gender}}</td>
                            <td>{{candidate.date_of_birth}}</td>
                            <td>
                                <a href="#">
                                    <span @click="change_detail_previous_page('search');view_candidate_details(candidate)" class="btn btn-info">Profile</span>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- .content -->
    </div>
    <!-- /#right-panel -->
</div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import * as ss from '../assets/js/skillstash.js';
import CandidateCard from '@/components/CandidateCard'
import CandidateDetails from '@/components/CandidateDetails'
import '../../static/assets/js/bootstrap-select.min.js'
import PasswordForm from './PasswordForm'
import ProfileAvatar from './ProfileAvatar'
import TreeNode from './TreeNode'
export default {
    name: 'EmployerProfile',
    components: {
        CandidateCard,
        CandidateDetails,
        PasswordForm,
        ProfileAvatar,
        TreeNode
    },
    data() {
        return {
            loading: false,
            treeData: [],
            root_skills: [],
            cities: null,
            skills: null,
            name: '',
            all_job_posts: [],
            filtered_job_posts: [],
            description: '',
            city: '',
            required_education: 0,
            pay_type: 'Y',
            pay: '',
            company: '',
            employer: null,
            profile_photo: null,
            all_job_matches: [],
            filtered_job_matches: [],
            candidates: [],
            selected_candidate: null,
            highest_education: null,
            cities: '',
            first_name: '',
            last_name: '',
            email: '',
            gender: '',
            highest_education: 0,
            job_city: '',
            job_name: '',
            job_state: 'Active',
            job_sort_field: 'Name',
            job_sort_order: 'Ascending',
            match_job: '',
            match_state: 'Active',
            match_sort_field: 'J_Name',
            match_sort_order: 'Ascending',
            detail_previous_page: 'match',
        }
    },
    methods: {
        logout() {
            axios({
                method: 'post',
                url: API_HOST + '/rest-auth/logout/',
                params: {}
            })
            // Go to the login page unconditionally, since a failure of the
            // logout method probably indicates that the user was no longer
            // logged in.
            sessionStorage.clear();
            this.$router.push({
                path: '/login'
            })
        },
        post_job() {
            if (!this.validate_job_fields(this.name, this.description, this.city, this.pay))
                return;
            axios({
                method: 'post',
                url: API_HOST + '/api/job-posts/',
                data: {
                    "name": this.name,
                    "description": this.description,
                    "city": this.city,
                    "required_education": this.required_education,
                    "pay_type": this.pay_type,
                    "pay": this.pay
                }
            })
            .then((response) => {
                if (response.status === 200 || response.status === 201) {
                    var job = response.data;
                    job.id_to_skill = new Map();
                    this.all_job_posts.push(job);
                    this.filter_job_posts();
                }
            })
            .catch(function (error) {
                console.log(error)
            })
        },
        validate_job_fields(name, description, city, pay) {
            name = name.trim();
            description = description.trim();
            city = city.trim();
            if (name.length == 0) {
                alert("Job name cannot be blank.");
                return false;
            }
            if (description.length == 0) {
                alert("Description cannot be blank.");
                return false;
            }
            if (city.length == 0) {
                alert("City cannot be blank.");
                return false;
            }
            if (pay.length == 0) {
                alert("Pay cannot be blank.");
                return false;
            }
            let payFloat = parseFloat(pay);
            if (payFloat <= 0.0 || isNaN(payFloat)) {
                alert("Pay is invalid.");
                return false;
            }
            return true;
        },
        view_job_matches() {
            this.load_job_posts();
            this.load_job_matches();
            $('.page-tab').hide();
            $('#candidate-matched-list').show();
        },
        change_detail_previous_page(page){
            this.detail_previous_page = page
        },
        view_candidate_details(candidate) {
            this.selected_candidate = candidate
            $('.page-tab').hide()
            $('#candidate-details-tab').show()
        },
        close_candidate_details() {
            $('.page-tab').hide();
            if(this.detail_previous_page === 'match'){
                $('#candidate-matched-list').show()
            }else{
                $('#search-candidates-tab').show()
            }
        },
        view_search_candidates() {
            $('.page-tab').hide()
            $('#search-candidates-tab').show()
        },
        load_job_posts() {
            axios({
                method: 'get',
                url: API_HOST + '/api/job-posts-and-skills/?contact_person=' + sessionStorage.getItem("user_id"),
            }).then(response => {
                this.all_job_posts = response.data
                this.id_to_job = new Map();
                for (var i = 0; i < this.all_job_posts.length; i++) {
                    var job = this.all_job_posts[i];
                    this.id_to_job.set(job.id, job);
                    job.id_to_skill = new Map();
                    for (var j = 0; j < job.skills.length; j++) {
                        var js = job.skills[j];
                        job.id_to_skill.set(js.skill.id, js);
                    }
                }
                this.filter_job_posts();
            })
        },
        filter_job_posts() {
            var filter_jobs = function(j) {
                if (this.job_name != '' && !j.name.includes(this.job_name))
                    return false;
                if (this.job_city != '' && j.city.localeCompare(this.job_city, 'en', {sensitivity: 'base'}) != 0)
                    return false;
                if (this.job_state == 'All')
                    return true;
                if (this.job_state == 'Active')
                    return j.state == 'L' || j.state == 'JO';
                if (this.job_state == 'Inactive')
                    return j.state == 'F' || j.state == 'W';
                return j.state == this.job_state;
            }

            if (this.job_name != '' || this.job_city != '' || this.job_state != 'All') {
                this.filtered_job_posts = this.all_job_posts.filter(filter_jobs, this);
            } else {
                this.filtered_job_posts = this.all_job_posts.slice();
            }
            this.sort_job_posts();
        },
        sort_job_posts() {
            let order = (this.job_sort_order === 'Ascending') ? 1 : -1;
            if (this.job_sort_field === 'Name') {
                this.filtered_job_posts.sort(function(a, b) {
                    return a.name.localeCompare(b.name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.job_sort_field === 'City') {
                this.filtered_job_posts.sort(function(a, b) {
                    return a.city.localeCompare(b.city, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.job_sort_field === 'Date') {
                this.filtered_job_posts.sort(function(a, b) {
                    // This hack relies on the fact that newer jobs will have higher IDs.
                    return (a.id - b.id) * order;
                });
            } else if (this.job_sort_field === 'State') {
                this.filtered_job_posts.sort(function(a, b) {
                    return a.state.localeCompare(b.state, 'en', {sensitivity: 'base'}) * order;
                });
            }
        },
        load_job_matches() {
            // The back end will only return matches for this employer's jobs.
            axios({
                method: "get",
                url: API_HOST + '/api/job-matches-and-candidates/'
            }).then(response => {
                if (response.status === 200) {
                    console.log(response)
                    this.all_job_matches = response.data;
                    this.filter_job_matches();
                }
            })
        },
        filter_job_matches() {
            var filter_job_matches = function(m) {
                if (this.match_job != '' && m.job.id != this.match_job)
                    return false;
                if (this.match_state == 'All')
                    return true;
                if (this.match_state == 'Active')
                    return m.state == 'N' || m.state == 'CI' || m.state == 'EI' || m.state == 'P' || m.state == 'JO';
                if (this.match_state == 'Inactive')
                    return m.state == 'DC' || m.state == 'DE' || m.state == 'H' || m.state == 'JD' || m.state == 'F' || m.state == 'W';
                return m.state == this.match_state;
            }

            if (this.match_job != null || this.match_state != '') {
                this.filtered_job_matches = this.all_job_matches.filter(filter_job_matches, this);
            } else {
                this.filtered_job_matches = this.all_job_matches.slice();
            }
            this.sort_job_matches();
        },
        sort_job_matches() {
            let order = (this.match_sort_order === 'Ascending') ? 1 : -1;
            if (this.match_sort_field === 'Score') {
                this.filtered_job_matches.sort(function(a, b) {
                    return (a.score - b.score) * order;
                });
            } else if (this.match_sort_field === 'C_F_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.candidate.user.first_name.localeCompare(b.candidate.user.first_name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.match_sort_field === 'C_L_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.candidate.user.last_name.localeCompare(b.candidate.user.last_name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.match_sort_field === 'J_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.job.name.localeCompare(b.job.name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.match_sort_field === 'J_Date') {
                this.filtered_job_matches.sort(function(a, b) {
                    // This hack relies on the fact that newer jobs will have higher IDs.
                    return (a.job.id - b.job.id) * order;
                });
            }
        },
        job_state_name(job) {
            return ss.job_state_names[job.state];
        },
        remove_job(job) {
            if (confirm("Are you sure that you want to delete the job " + job.name + "?")) {
                axios({
                    method: 'delete',
                    url: API_HOST + '/api/job-posts/' + job.id + '/',
                }).then(response => {
                    for (let index = 0; index < this.all_job_posts.length; ++index) {
                        if (this.all_job_posts[index].id == job.id) {
                            this.all_job_posts.splice(index, 1);
                            this.filter_job_posts();
                            break;
                        }
                    }
                }).catch(function (error) {
                    alert(error.response.data)
                })
            }
        },
        can_update_job(job) {
            // Do no allow updating of withdrawn or filled jobs.
            return job.state == 'L' || job.state == 'JO';
        },
        update_job(job) {
            if ($("#job" + job.id).is(":hidden")) {
                $("#job" + job.id).show()
            } else {
                $("#job" + job.id).hide()
            }
        },
        save_job(job) {
            if (!this.validate_job_fields(job.name, job.description, job.city, job.pay))
                return;
            axios({
                method: 'PUT',
                url: API_HOST + '/api/job-posts/' + job.id + '/',
                data: {
                    "name": job.name,
                    "description": job.description,
                    "city": job.city,
                    "required_education": job.required_education,
                    "pay_type": job.pay_type,
                    "pay": job.pay
                }
            })
            .then((response) => {
                if (response.status === 200 || response.status === 201) {
                }
            })
            .catch(function (error) {
                console.log(error)
            })
        },
        create_matches(job) {
            axios({
                method: 'post',
                url: API_HOST + '/api/create-matches/',
                data: {
                    job: job.id,
                    max_candidates: 10
                }
            }).then(response => {
                var matches = response.data.length
                if (matches == 0) {
                    alert('No matching candidates found.')
                } else if (matches == 1) {
                    alert('One matching candidate found.')
                } else {
                    alert(matches.toString() + ' matching candidates found.')
                }
            }).catch(function (error) {
                alert(error.response.data)
            })
        },
        withdraw_job(job) {
            if (confirm("Are you sure you want to withdraw the job " + job.name + "? This action cannot be undone.")) {
                axios({
                    method: 'post',
                    url: API_HOST + '/api/job-posts/' + job.id + '/withdraw_job/'
                }).then(response => {
                    job.state = response.data.state;
                }).catch(function (error) {
                    alert(error.response.data)
                })
            }
        },
        add_skills_to_job(job) {
            var checkboxes = $("#jobskills" + job.id + " input[name='skill_checkbox']").toArray();
            for (let index in checkboxes) {
                let checkbox = checkboxes[index];
                if (checkbox.checked) {
                    let skill_id = parseInt(checkbox.attributes['idvalue'].value);
                    // Make sure this skill hasn't already been added to the job.
                    if (!job.id_to_skill.has(skill_id)) {
                        let skill_name = checkbox.attributes['namevalue'].value;
                        var js = {
                            job: job.id,
                            skill: {
                                id: skill_id,
                                name: skill_name
                            },
                            priority: 1,
                            proficiency: 1,
                            months_experience: 0,
                            experience: 0,
                            experience_unit: 12
                        }
                        // Special handling for a skill being removed and then added again.
                        if (job.deleted_skills != undefined) {
                            var deleted_js = job.deleted_skills.get(skill_id);
                            if (deleted_js != undefined) {
                                js.id = deleted_js.id;
                                js.modified = true;
                                job.deleted_skills.delete(skill_id);
                            }
                        }
                        // Insert the new skill into the list in alphabetical order.
                        var i = 0;
                        while (i < job.skills.length && job.skills[i].skill.name < skill_name) {
                            i++;
                        }
                        job.skills.splice(i, 0, js);
                        job.id_to_skill.set(skill_id, js);
                    }
                }
            }
        },
        remove_skill_from_job(job, js, index) {
            if (js.id != undefined) {
                if (job.deleted_skills == undefined) {
                    job.deleted_skills = new Map();
                }
                job.deleted_skills.set(js.skill.id, js);
            }
            job.skills.splice(index, 1);
            job.id_to_skill.delete(js.skill.id);
        },
        mark_skill_changed(js) {
            if (js.id != undefined) {
                js.modified = true;
            }
        },
        save_job_skill_changes(job) {
            for (var i = 0; i < job.skills.length; i++) {
                var js = job.skills[i];
                if (js.id === undefined) {
                    // This is a newly added skill.
                    axios({
                        method: "post",
                        url: API_HOST + "/api/job-skills/",
                        data: {
                            job: js.job,
                            skill: js.skill.id,
                            priority: js.priority,
                            proficiency: js.proficiency,
                            months_experience: js.experience * js.experience_unit
                        }
                    }).then(response => {
                        job.id_to_skill.get(response.data.skill).id = response.data.id
                    });
                } else if (js.modified) {
                    // This is an update to an existing skill.
                    axios({
                        method: "patch",
                        url: API_HOST + "/api/job-skills/" + js.id + "/",
                        data: {
                            priority: js.priority,
                            proficiency: js.proficiency,
                            months_experience: js.experience * js.experience_unit
                        }
                    }).then(response => {
                        delete job.id_to_skill.get(response.data.skill).modified;
                        console.log(response.data);
                    });
                }
            }

            if (job.deleted_skills != undefined) {
                for (let js of job.deleted_skills.values()) {
                    this.delete_job_skill(job, js);
                }
            }
        },
        delete_job_skill(job, js) {
            axios({
                method: "delete",
                url: API_HOST + "/api/job-skills/" + js.id + "/"
            }).then(response => {
                job.deleted_skills.delete(js.skill.id);
            });
        },
        revert_job_skills(job) {
            if (confirm("Are you sure you want to revert all unsaved changes to this job's skill requirements?")) {
                axios({
                    method: 'get',
                    url: API_HOST + '/api/job-skills/',
                    params: {
                        job: job.id
                    }
                }).then(response => {
                    job.skills = response.data;
                    job.id_to_skill.clear();
                    for (var i = 0; i < job.skills.length; i++) {
                        var js = job.skills[i];
                        job.id_to_skill.set(js.skill.id, js);
                    }
                })
            }
        },
        parent_avatar_changed(new_avatar_path) {
            this.profile_photo = new_avatar_path
            console.log(this.profile_photo)
        },
        load_root_skills() {
            axios({
                method: 'get',
                url: API_HOST + '/api/skills/',
                params: {
                    category: "root"
                }
            }).then(response => {
                console.log(response)
                if (this.root_skills.length == 0) {
                    this.root_skills = response.data
                    for (var index in this.root_skills) {
                        var root_skill = this.root_skills[index]
                        this.treeData.push({
                            label: root_skill.name,
                            type: root_skill.type,
                            id: root_skill.id
                        })
                    }
                    this.$forceUpdate()
                }
            })
        },
        search_candidates() {
            // Get the checkboxes from the candidate skill tree.
            var skill_tree = document.getElementById("candidate-skill-tree");
            var checkboxes = skill_tree.querySelectorAll('input[name="skill_checkbox"]');
            var search_skills = "";
            for (var index = 0; index < checkboxes.length; ++index) {
                var checkbox = checkboxes[index]
                if (checkbox.checked) {
                    var idv = parseInt(checkbox.attributes['idvalue'].value)
                    search_skills += idv
                    search_skills += ','
                }
            }
            if (search_skills != '') search_skills = search_skills.substring(0, search_skills.length - 1)

            // filter candidates
            axios({
                method: 'get',
                url: API_HOST + '/api/candidates/',
                params: {
                    cities: this.cities.toString() === '' ? null : this.cities.toString(),
                    skills: search_skills === '' ? null : search_skills,
                    first_name: this.first_name === '' ? null : this.first_name,
                    last_name: this.last_name === '' ? null : this.last_name,
                    email: this.email === '' ? null : this.email.toLowerCase(),
                    gender: this.gender === '' ? null : this.gender,
                    highest_education: this.highest_education == 0 ? null : this.highest_education
                }
            }).then(response => {
                this.candidates = response.data
                console.log(response.data)
                // Sort by last name.
                this.candidates.sort(function(a, b) {
                    return a.user.last_name.localeCompare(b.user.last_name, 'en', {sensitivity: 'base'});
                });
            })
        },
        load_profile() {
            if (this.employer == null) {
                axios({
                    method: 'get',
                    url: API_HOST + '/api/employers/' + sessionStorage.getItem("user_id") + '/'
                }).then(response => {
                    if (response.status === 200) {
                        console.log(response.data)
                        this.employer = response.data
                        if (this.employer.photo && this.employer.photo != null) {
                            this.profile_photo = API_HOST + '/api/download/' + sessionStorage.getItem("user_id") + '/' + this.employer.photo
                        }
                    }
                })
            }
        },
        update_profile() {
            if (!ss.validate_user(this.employer.user))
                return;
            axios({
                method: 'put',
                url: API_HOST + '/api/employers/' + this.employer.user.id + '/',
                data: this.employer
            }).then(response => {
                
            })
        },
        filter_city() {
            this.load_user()
        },
        edit_profile() {
            $('.page-tab').hide()
            $('#profile_tab').show();
        },
        change_password() {
            $(".page-tab").hide();
            $("#password_tab").show();
        },
        post_jobs_tab() {
            $('.page-tab').hide()
            this.load_job_posts()
            $('#jobs').show()
        },
    },
    beforeMount() {
        this.loading = false
        this.load_root_skills()
        this.load_profile()
    },
    mounted() {
        var cbuttons = $('.modal-close').toArray();
        cbuttons.forEach(button => {
            let parentid = button.attributes['parentid'].value
            $(button).click(function () {
                jQuery('#' + parentid).modal('hide')
            })

        });
    },
    updated() {
        $('.selectpicker').selectpicker('refresh');
        $('.selectpicker').selectpicker('render');
    }
}
</script>

<style lang="scss">

.calculate form input {
    width: 220px;
    height: 40px;
    line-height: 40px;
    outline: none;
    border: none;
    vertical-align: middle;
}

.calculate form ul label {
    font-size: 22px;
    vertical-align: middle;
}

.pay-fields input {
    display: inline-block;
    width: 10em;
}

.post-job-form {
    background: #ffffff;
    padding: 30px 30px 20px;
    border-radius: 4px;
    z-index: 2;
    margin-bottom: 10px;
    overflow: hidden;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16), 0px 3px 6px rgba(0, 0, 0, 0.23);
}

#jobposts {
    margin-top: 1.5rem;
}

#experience {
    display: inline-block;
    width: 5em;
}

</style>

<style scoped>
@import 'font-awesome/css/font-awesome.min.css';
@import '../../static/assets/css/build.css';
@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../../static/assets/scss/style.css';
@import '../../static/assets/css/lib/vector-map/jqvmap.min.css';
@import "../assets/css/skillstash.css";
</style>
