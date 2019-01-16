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
                    <li><a href="#" @click="view_jobs"><i class="li-icon fa fa-search"></i>Find Jobs</a></li>
                    <li><a href="#" @click="view_job_matches"><i class="li-icon fa fa-bars"></i>Job Matches</a></li>
                    <li><a href="#" @click="view_search_candidates"><i class="li-icon fa fa-search"></i>Search for Candidates</a></li>
                    <li><a href="#" @click="logout"><i class="li-icon fa fa-power-off"></i>Sign Out</a></li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>
    </aside>

    <div id="right-panel" class="right-panel">
        <div class="mt-3 page-tab" id="jobposts" hidden>
            <div class="shadow-paper col-md-12 col-lg-12">
                <div class="paper-up">
                    <div id="job-skill-tree" class="paper-left">
                        <label>Skills</label>
                        <ul v-for="(td,index) in treeData" :key="index">
                            <tree-node :model="td"></tree-node>
                        </ul>
                    </div>
                    <div class="paper-right">
                        <div class="form row right-container">
                            <form @submit.prevent="search_job" class="form-horizontal">
                                <div class="">
                                    <!-- city selection -->
                                    <div class="form-group">
                                        <label>Cities</label>
                                        <input type="text" v-model="job_cities" class="form-control" placeholder="Cities">
                                    </div>
                                    <!-- name_contains selection -->
                                    <div class="form-group">
                                        <label>Name Contains</label>
                                        <input type="text" v-model="name_contains" class="form-control" placeholder="Name Contains">
                                    </div>
                                    <!-- desc_contains selection -->
                                    <div class="form-group">
                                        <label>Description Contains</label>
                                        <input type="text" v-model="desc_contains" class="form-control" placeholder="Description Contains">
                                    </div>
                                    <!-- education selection -->
                                    <div class="form-group education-fields">
                                        <label>Education Requirement</label>
                                        <select v-model="min_education">
                                            <option value=0>No Minimum</option>
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
                                        <label>to</label>
                                        <select v-model="max_education">
                                            <option value=0>No Maximum</option>
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
                                    <!-- salary selection -->
                                    <div class="form-group">
                                        <label>Salary Range</label>
                                        <div class="salary-fields">
                                            <input type="text" v-model="min_salary" class="form-control" placeholder="-">
                                            <label>to</label>
                                            <input type="text" v-model="max_salary" class="form-control" placeholder="-">
                                        </div>
                                    </div>
                                    <!-- Submit. -->
                                    <div class="form-group">
                                        <input type="submit" class="btn btn-info" value="Search" />
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card-table">
                <div class="job-card" v-for="job in jobposts" :key=job.id>
                    <div class="job-card-header">
                        <i class="mr-2 fa fa-align-justify"></i>
                        <div class="job-card-title"><strong>{{job.name}}</strong></div>
                        <div v-bind:class="[favourite_job_ids.has(job.id) ? 'click pull-right active': 'click pull-right']" @click="toggle_favourite_job(job)" :id="'fav_job' + job.id">
                            <span v-bind:class="[favourite_job_ids.has(job.id) ? 'fa fa-star': 'fa fa-star-o']"></span>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <tr>
                                <td><i class="fa fa-tasks"></i>{{job.description}}</td>
                            </tr>
                            <tr>
                                <td><i class="fa fa-map-marker"></i>{{job.city}}</td>
                            </tr>
                            <tr>
                                <td><i class="fa fa-user"></i>{{job.contact_person.user.first_name}} {{job.contact_person.user.last_name}}</td>
                            </tr>
                            <tr>
                                <td><i class="fa fa-calendar"></i>{{job.date_posted}}</td>
                            </tr>
                            <tr>
                                <td><i class="fa fa-money"></i>{{get_salary_str(job)}}</td>
                            </tr>
                            <tr>
                                <td><i class="fa fa-graduation-cap"></i>{{get_education_name(job)}}</td>
                            </tr>
                        </table>
                    </div>
                    <div class="card-bottom" v-if="job.skills.length != 0">
                        <button type="button" v-if="js.skill" class="btn btn-secondary mb-1 job-skill" v-for="(js,index) in job.skills" :key=index @click="view_job_details(job)">
                            {{js.skill.name}}
                        </button>
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
                        <div class="form col-sm-offset-1 col-md-offset-1 col-lg-offset-1 col-sm-10 col-md-10 col-lg-10" v-if="recruiter">
                            <div class="form-group has-feedback ">
                                <label>First Name</label>
                                <input type="text" v-model="recruiter.user.first_name" class="form-control" placeholder="First Name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback ">
                                <label>Last Name</label>
                                <input type="text" v-model="recruiter.user.last_name" class="form-control" placeholder="Last Name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>Email</label>
                                <input class="form-control email" v-model="recruiter.user.email" type="text" placeholder="Email" />
                                <i class="glyphicon glyphicon-envelope form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>Phone</label>
                                <input class="form-control phone" type="text" placeholder="Phone" v-model="recruiter.user.phone" />
                                <i class="glyphicon glyphicon-phone form-control-feedback"></i>
                            </div>
                            <div class="form-group">
                                <label>City</label>
                                <input class="form-control required" type="text" v-model="recruiter.user.city" placeholder="City" />
                            </div>
                            <div class="form-group">
                                <label>Company</label>
                                <input class="form-control" type="text" v-model="recruiter.company" placeholder="Company" />
                            </div>
                            <div class="form-group">
                                <label>Website</label>
                                <input class="form-control required" type="text" v-model="recruiter.website" placeholder="Website" />
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
                    <option v-for="(job, index) in jobposts" :value="job.id" :key="index">{{job.name}}</option>
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
                <CandidateCard :match="match" no_buttons=true v-for="match in filtered_job_matches" :key="match.id" v-on:candidate_clicked="view_candidate_details(match.candidate)" />
                <div class="no-matches" v-if="!filtered_job_matches || filtered_job_matches.length===0">
                    <h2>Sorry, we didn't find any job matches.</h2>
                </div>
            </div>
        </div>

        <div id="candidate-details-tab" class="page-tab" hidden>
            <candidate-details v-if="selected_candidate != null" :candidate="selected_candidate" v-on:close_clicked="close_candidate_details" />
        </div>

        <div id="job-details-tab" class="page-tab" hidden>
            <job-details v-if="selected_job != null" :job="selected_job" v-on:close_clicked="close_job_details" />
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
                                    <input type="text" v-model="candidate_cities" class="form-control" placeholder="Candidates's location">
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
                                    <label>Education</label>
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
            <div class="paper-down">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Gender</th>
                            <th>DoB</th>
                            <th>Profile</th>
                            <th>Favourite</th>
                            <th>Match to Job</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(candidate,index) in candidates" :key="index">
                            <td>{{candidate.user.first_name}} {{candidate.user.last_name}}</td>
                            <td>{{candidate.gender}}</td>
                            <td>{{candidate.date_of_birth}}</td>
                            <td>
                                <a href="#">
                                    <span @click="view_candidate_details(candidate)" class="btn btn-info">Profile</span>
                                </a>
                            </td>
                            <td>
                                <div v-bind:class="[favourite_candidate_ids.has(candidate.user.id) ? 'click active': 'click']" @click="toggle_favourite_candidate(candidate)" :id="'fav_cand' + candidate.user.id">
                                    <span v-bind:class="[favourite_candidate_ids.has(candidate.user.id) ? 'fa fa-star': 'fa fa-star-o']"></span>
                                </div>
                            </td>
                            <td>
                                <select :id="'job-selector'+candidate.user.id">
                                    <option v-for="(job, index) in favourite_jobs" :value="job.id" :key="index">{{job.name}}</option>
                                </select>
                                <button @click="create_match(candidate)" type="button" class="btn btn-secondary mb-1">Match</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- .content -->
    </div>
    <!-- /#right-panel -->

    <!-- Confimation dialog for creating a job match without the required skills. -->
    <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">Force to Match</h4>
                </div>
                <div class="modal-body">The candidate does not meet the requirements for this job. Do you really want to create a match?</div>
                <div class="modal-footer">
                    <button type="button" parentid="confirmModal" @click="force_create_match" class="btn btn-primary modal-close">Yes</button>
                    <button type="button" parentid="confirmModal" @click="cancel_create_match" class="btn btn-second modal-close">No</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal -->
    </div>
</div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import * as ss from '../assets/js/skillstash.js';
import CandidateCard from '@/components/CandidateCard'
import CandidateDetails from '@/components/CandidateDetails'
import JobDetails from '@/components/JobDetails'
import '../../static/assets/js/bootstrap-select.min.js'
import PasswordForm from './PasswordForm'
import ProfileAvatar from './ProfileAvatar'
import TreeNode from './TreeNode'
export default {
    name: 'RecruiterProfile',
    components: {
        CandidateCard,
        CandidateDetails,
        JobDetails,
        PasswordForm,
        ProfileAvatar,
        TreeNode
    },
    data() {
        return {
            loading: false,
            treeData: [],
            root_skills: [],
            skills: null,
            name: '',
            jobposts: [],
            description: '',
            city: '',
            // Job filtering variables
            job_cities: "",
            name_contains: "",
            desc_contains: "",
            max_education: 0,
            min_education: 0,
            contact_person: [],
            min_salary: "",
            max_salary: "",
            pay_type: 'Y',
            pay: '',
            company: '',
            recruiter: null,
            profile_photo: null,
            all_job_matches: null,
            filtered_job_matches: null,
            filtered_matches: null,
            candidates: [],
            favourite_candidate_ids: new Set(),
            selected_candidate: null,
            selected_job: null,
            highest_education: null,
            candidate_cities: '',
            first_name: '',
            last_name: '',
            email: '',
            gender: '',
            highest_education: 0,
            match_job: '',
            match_state: 'Active',
            match_sort_field: 'J_Name',
            match_sort_order: 'Ascending',
            candidate_to_force_apply: null,
            job_to_force_apply: null,
            favourite_jobs: [],
            favourite_job_ids: new Set(),
            detail_previouse_page: 'search'
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
        toggle_favourite_job(job) {
            if (this.favourite_job_ids.has(job.id)) {
                // Remove this job from favourites.
                axios({
                    method: 'delete',
                    url: API_HOST + '/api/favourites-jobs/',
                    params: {
                        job: job.id,
                        SSUser: sessionStorage.getItem("user_id")
                    }
                }).then(response => {
                    this.favourite_job_ids.delete(job.id);
                    // Remove the job from the favourite_jobs list.
                    for (let i = 0; i < this.favourite_jobs.length; ++i) {
                        if (this.favourite_jobs[i].id == job.id) {
                            this.favourite_jobs.splice(i, 1);
                            break;
                        }
                    }
                    // Update UI.
                    $('#fav_job' + job.id).removeClass('active')
                    $('#fav_job' + job.id + ' span').removeClass('fa-star')
                    $('#fav_job' + job.id + ' span').addClass('fa-star-o')
                })
            } else {
                // Make this job a favourite.
                axios({
                    method: "post",
                    url: API_HOST + "/api/favourites-jobs/",
                    data: {
                        job: job.id,
                        SSUser: sessionStorage.getItem("user_id")
                    }
                }).then(response => {
                    this.favourite_job_ids.add(job.id);
                    // Add the job to the favourite_jobs list in alphabetical order.
                    var i = 0;
                    while (i < this.favourite_jobs.length && this.favourite_jobs[i].name < job.name) {
                        i++;
                    }
                    this.favourite_jobs.splice(i, 0, job);
                    // Update UI.
                    $('#fav_job' + job.id).addClass('active')
                    $('#fav_job' + job.id + ' span').addClass('fa-star')
                    $('#fav_job' + job.id + ' span').removeClass('fa-star-o')
                })
            }
        },
        toggle_favourite_candidate(candidate) {
            var id = candidate.user.id;
            if (this.favourite_candidate_ids.has(id)) {
                // Remove this candidate from favourites.
                axios({
                    method: 'delete',
                    url: API_HOST + '/api/favourites-candidates/',
                    params: {
                        candidate: id,
                        SSUser: sessionStorage.getItem("user_id")
                    }
                }).then(response => {
                    this.favourite_candidate_ids.delete(id);
                    // Update UI.
                    $('#fav_cand' + id).removeClass('active');
                    $('#fav_cand' + id + ' span').removeClass('fa-star');
                    $('#fav_cand' + id + ' span').addClass('fa-star-o');
                })
            } else {
                // Make this candidate a favourite.
                axios({
                    method: "post",
                    url: API_HOST + "/api/favourites-candidates/",
                    data: {
                        candidate: id,
                        SSUser: sessionStorage.getItem("user_id")
                    }
                }).then(response => {
                    this.favourite_candidate_ids.add(id);
                    // Update UI.
                    $('#fav_cand' + id).addClass('active');
                    $('#fav_cand' + id + ' span').addClass('fa-star');
                    $('#fav_cand' + id + ' span').removeClass('fa-star-o');
                })
            }
        },
        get_salary_str(job){
            let pay_type = job.pay_type;
            let pay_period = '';
            if (pay_type === 'D')
                pay_period = 'Day';
            else if (pay_type === 'H')
                pay_period = 'Hour';
            else if (pay_type === 'M')
                pay_period = 'Month';
            else if (pay_type === 'Y')
                pay_period = 'Year';
            return '$' + job.pay + ' / ' + pay_period;
        },
        get_education_name(job) {
            return ss.education_names[job.required_education];
        },
        search_job() {
            // Get the checkboxes from the job skill tree.
            var skill_tree = document.getElementById("job-skill-tree");
            var checkboxes = skill_tree.querySelectorAll('input[name="skill_checkbox"]');
            var search_skills = "";
            for (var index = 0; index < checkboxes.length; ++index) {
                var checkbox = checkboxes[index];
                if (checkbox.checked) {
                    var idv = parseInt(checkbox.attributes["idvalue"].value);
                    search_skills += idv;
                    search_skills += ",";
                }
            }
            if (search_skills != "")
                search_skills = search_skills.substring(0, search_skills.length - 1);
            // Filter jobs.
            this.job_cities = this.job_cities.trim();
            axios({
                method: "get",
                url: API_HOST + "/api/job-posts-and-skills/",
                params: {
                    states: 'L,JO', // Only include active job posts.
                    cities: this.job_cities != "" ? this.job_cities : null,
                    name_contains: this.name_contains != "" ? this.name_contains : null,
                    desc_contains: this.desc_contains != "" ? this.desc_contains : null,
                    min_education: this.min_education > 0 ? this.min_education : null,
                    max_education: this.max_education > 0 ? this.max_education : null,
                    min_salary: this.min_salary != "" ? this.min_salary : null,
                    max_salary: this.max_salary != "" ? this.max_salary : null,
                    skills: search_skills === "" ? null : search_skills
                }
            }).then(response => {
                console.log(response.data);
                this.jobposts = response.data;
                this.jobposts.sort(function(a, b) {
                    return a.name.localeCompare(b.name, 'en', {sensitivity: 'base'});
                });
            });
        },
        view_job_matches() {
            this.load_job_matches();
            $('.page-tab').hide();
            this.detail_previous_page = 'match';
            $('#candidate-matched-list').show();
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
            this.detail_previous_page = 'search';
            $('#search-candidates-tab').show()
        },
        view_jobs() {
            $(".page-tab").hide();
            this.load_job_matches();
            $("#jobposts").show();
        },
        view_job_details(job) {
            this.selected_job = job;
            $('.page-tab').hide();
            $('#job-details-tab').show();
        },
        close_job_details() {
            $('.page-tab').hide();
            $('#jobposts').show();
        },
        load_job_matches() {
            // The back end will only return matches that this recruiter created.
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
        load_favourite_jobs() {
            axios({
                method: 'get',
                url: API_HOST + "/api/favourites-jobs/",
                params: {
                    SSUser: sessionStorage.getItem("user_id")
                }
            }).then(response => {
                let favourites = response.data;
                // Sort by name.
                favourites.sort(function(a, b) {
                    return a.job.name.localeCompare(b.job.name, 'en', {sensitivity: 'base'});
                });
                this.favourite_jobs = [];
                this.favourite_job_ids.clear();
                for (var index in favourites) {
                    this.favourite_jobs.push(favourites[index].job);
                    this.favourite_job_ids.add(favourites[index].job.id);
                }
            })
        },
        load_favourite_candidates() {
            axios({
                method: 'get',
                url: API_HOST + "/api/favourites-candidates/",
                params: {
                    SSUser: sessionStorage.getItem("user_id")
                }
            }).then(response => {
                let favourites = response.data;
                this.favourite_candidate_ids.clear();
                for (var index in favourites) {
                    this.favourite_candidate_ids.add(favourites[index].candidate);
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
        create_match(candidate) {
            // Find the job selector in the correct row in the candidate table.
            var job_selector = document.getElementById('job-selector' + candidate.user.id);
            var job_id = job_selector.value;
            axios({
                method: "post",
                url: API_HOST + "/api/create-manual-match/",
                data: {
                    job: job_id,
                    candidate: candidate.user.id
                }
            }).then(response => {
                if (response.status === 200) {
                    this.all_job_matches.push(response.data);
                }
            }).catch(error => {
                if (error.response.status === 400) {
                    this.candidate_to_force_apply = candidate;
                    this.job_to_force_apply = job_id;
                    jQuery("#confirmModal").modal("show");
                }
            });
        },
        force_create_match() {
            let job_id = this.job_to_force_apply;
            axios({
                method: "post",
                url: API_HOST + "/api/create-manual-match/",
                data: {
                    job: job_id,
                    candidate: this.candidate_to_force_apply.user.id,
                    validate: false
                }
            }).then(response => {
                if (response.status === 200) {
                    this.all_job_matches.push(response.data);
                }
            }).catch(error => {
                alert(error.response.data);
            });
            jQuery("#confirmModal").modal("hide");
        },
        cancel_create_match() {
            jQuery("#confirmModal").modal("hide");
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
            if (search_skills != '')
                search_skills = search_skills.substring(0, search_skills.length - 1)

            // filter candidates
            axios({
                method: 'get',
                url: API_HOST + '/api/candidates/',
                params: {
                    cities: this.candidate_cities.toString() === '' ? null : this.candidate_cities.toString(),
                    skills: search_skills === '' ? null : search_skills,
                    first_name: this.first_name === '' ? null : this.first_name,
                    last_name: this.last_name === '' ? null : this.last_name,
                    email: this.email === '' ? null : this.email,
                    gender: this.gender === '' ? null : this.gender,
                    highest_education: this.highest_education == 0 ? null : this.highest_education
                }
            }).then(response => {
                console.log(response.data)
                this.candidates = response.data
                // Sort by last name.
                this.candidates.sort(function(a, b) {
                    return a.user.last_name.localeCompare(b.user.last_name, 'en', {sensitivity: 'base'});
                });
            })
        },
        load_profile() {
            if (this.recruiter == null) {
                axios({
                    method: 'get',
                    url: API_HOST + '/api/recruiters/' + sessionStorage.getItem("user_id") + '/'
                }).then(response => {
                    if (response.status === 200) {
                        console.log(response.data)
                        this.recruiter = response.data
                        if (this.recruiter.photo && this.recruiter.photo != null) {
                            this.profile_photo = API_HOST + '/api/download/' + sessionStorage.getItem("user_id") + '/' + this.recruiter.photo
                        }
                    }
                })
            }
        },
        update_profile() {
            if (!ss.validate_user(this.recruiter.user))
                return;
            axios({
                method: 'put',
                url: API_HOST + '/api/recruiters/' + this.recruiter.user.id + '/',
                data: this.recruiter
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
        }
    },
    beforeMount() {
        this.loading = false
        this.load_root_skills()
        this.load_profile()
        this.load_favourite_candidates();
        this.load_favourite_jobs();
    },
    mounted() {
        var cbuttons = $('.modal-close').toArray();
        cbuttons.forEach(button => {
            //console.log(button.attributes['parentid'].value)
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
<style scoped>
@import '../../static/assets/css/normalize.css';
@import '../../static/assets/css/themify-icons.css';
@import '../../static/assets/css/cs-skin-elastic.css';
@import '../../static/assets/scss/style.css';
@import '../../static/assets/css/lib/vector-map/jqvmap.min.css';

@import url( //fonts.googleapis.com/css?family=Open+Sans:600,400&subset=latin,cyrillic);

h4 {
    text-align: center;
    font-family: 'Open Sans', sans-serif;
    font-weight: 400;
    opacity: 0.7;
}

.click {
    font-size: 33px;
    color: rgba(0, 0, 0, .5);
    width: 38px;
    height: 38px;
    margin: 0 auto;
    position: relative;
    cursor: pointer;
}

body {
    padding-top: 20px;
}

.click span {
    margin-left: 4px;
    margin-top: 3px;
    z-index: 999;
    position: absolute;
}

span:hover {
    opacity: 0.8;
}

span:active {
    transform: scale(0.93, 0.93) translateY(2px)
}

.ring, .ring2 {
    opacity: 0;
    background: grey;
    width: 1px;
    height: 1px;
    position: absolute;
    top: 19px;
    left: 18px;
    border-radius: 50%;
    cursor: pointer;
}

.active span, .active-2 span {
    color: #F5CC27 !important;
}

.active-2 .ring {
    width: 58px !important;
    height: 58px !important;
    top: -10px !important;
    left: -10px !important;
    position: absolute;
    border-radius: 50%;
    opacity: 1 !important;
}

.active-2 .ring {
    background: #F5CC27 !important;
}

.active-2 .ring2 {
    background: #fff !important;
}

.active-3 .ring2 {
    width: 60px !important;
    height: 60px !important;
    top: -11px !important;
    left: -11px !important;
    position: absolute;
    border-radius: 50%;
    opacity: 1 !important;
}

.info {
    font-family: 'Open Sans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    white-space: nowrap;
    color: grey;
    position: relative;
    top: 30px;
    left: -46px;
    opacity: 0;
    transition: all 0.3s ease;
}

.info-tog {
    color: #F5CC27;
    position: relative;
    top: 45px;
    opacity: 1;
}

* {
    transition: all .32s ease;
}
</style>
