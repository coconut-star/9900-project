<!-- CandidateProfile page -->
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
                    <li><a href="#" @click="edit_skills"><i class="li-icon fa fa-address-card"></i>Manage my skills</a></li>
                    <li><a href="#" @click="edit_docs"><i class="li-icon fa fa-folder-open"></i>Manage my documents</a></li>
                    <li><a href="#" @click="view_jobs"><i class="li-icon fa fa-search"></i>Find Jobs</a></li>
                    <li><a href="#" @click="view_job_matches"><i class="li-icon fa fa-bars"></i>Job Matches</a></li>
                    <li><a href="#" @click="logout"><i class="li-icon fa fa-power-off"></i>Sign Out</a></li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>
    </aside>
    <!-- /#left-panel -->

    <!-- Right Panel -->
    <div id="right-panel" class="right-panel">
        <div id="skill-list" class="page-tab" style="display: none;">
            <div id="candidate-skill-tree" class="tree-box">
                <h3>All Skills</h3>
                <ul class="skill-tree" v-for="(td,index) in treeData" :key="index">
                    <tree-node :model="td"></tree-node>
                </ul>
            </div>

            <div class="skill-panel">
                <h3>My Skills</h3>
                <table class="skill-table">
                    <thead>
                        <tr>
                            <th>Skill</th>
                            <th>Proficiency</th>
                            <th>Experience</th>
                            <th>Evidence</th>
                        </tr>
                    </thead>
                    <tr v-for="(cs,index) in c_skills" :key="index">
                        <td>{{cs.skill.name}}</td>
                        <td>
                            <select v-model="cs.proficiency" @change="mark_skill_changed(cs)">
                                <option value=1>1</option>
                                <option value=2>2</option>
                                <option value=3>3</option>
                                <option value=4>4</option>
                                <option value=5>5</option>
                            </select>
                        </td>
                        <td class="experience-cell">
                            <input class="form-control" type="number" min="0" v-model="cs.experience" @input="mark_skill_changed(cs)" />
                            <select v-model="cs.experience_unit" @change="mark_skill_changed(cs)">
                                <option value=12>Years</option>
                                <option value=1>Months</option>
                            </select>
                        </td>
                        <td class="evidence-cell">
                            <select class="selectpicker" title="Select documents to support skill" v-model="cs.evidence" data-live-search="false" @change="mark_skill_changed(cs)" data-width="100%" multiple>
                                <option v-for="(doc, index) in docs" :key="index" :value="doc.id">{{doc.filename}}</option>
                            </select>
                        </td>
                        <td>
                            <a v-on:click="remove_skill(cs,index)">
                                <span class="glyphicon glyphicon-remove"></span>
                            </a>
                        </td>
                    </tr>
                </table>
                <div>
                    <button type="button" class="btn" @click='add_skills'>Add selected skills</button>
                    <button type="button" class="btn" @click="save_skill_changes">Save Changes</button>
                    <button type="button" class="btn" @click="revert_candidate_skills">Revert Unsaved Changes</button>
                </div>
            </div>
        </div>

        <div id="doc-page" style="display: none;" class="page-tab">
            <div class="shadow-paper">
                <h3>Upload a Document</h3>
                <div class="doc-upload">
                    <span style="white-space:nowrap">
                        <button @click="choose_file" class="btn btn-primary">Choose File</button>
                        <label>{{selected_file.name}}</label>
                        <input id="doc_file" type="file" @change="select_file_changed" hidden />
                    </span>
                    
                    <button type="button" class="btn pull-right" @click='upload_doc'>Upload</button>
                    <span class="pull-right form-inline" style="white-space:nowrap;margin-right:20px">
                        <label class="form-label form-inline">Description</label>
                        <input type="text" class="form-control" size="64" maxlength="64" v-model="upload_doc_desc" />
                    </span>
                    <span class="pull-right" style="white-space:nowrap;margin-right:20px">
                        <label>Type</label>
                        <select id="doc-type" v-model="upload_doc_type" class="selectpicker" data-width="fit">
                            <option v-for="(type, index) in doc_types" :value='type[0]' :key="index">{{type[1]}}</option>
                        </select>
                    </span>
                </div>
            </div>

            <div id="doc-list" class="shadow-paper">
                <h3>My Uploaded Documents</h3>
                <p class="doc-table" v-if="docs.length==0">You have not uploaded any files.</p>
                <table class="doc-table" v-if="docs.length != 0">
                    <tr>
                        <th>File Name</th>
                        <th>Type</th>
                        <th>Description</th>
                        <th>Date Uploaded</th>
                    </tr>
                    <tr v-for="(doc,index) in docs" :key="index">
                        <td><a :href="doc.url">{{doc.filename}}</a></td>
                        <td>
                            <select v-model="doc.type" class="selectpicker" data-width="fit">
                                <option v-for="(type, index) in doc_types" :value='type[0]' :key="index">{{type[1]}}</option>
                            </select>
                        </td>
                        <td><input type="text" class="form-control" style="width:auto" size="64" maxlength="64" v-model="doc.description" /></td>
                        <td>{{doc.date_uploaded}}</td>
                        <td>
                            <a v-on:click="update_doc(doc)">
                                <span class="glyphicon glyphicon-ok"></span>
                            </a>
                        </td>
                        <td>
                            <a v-on:click="remove_doc(doc,index)">
                                <span class="glyphicon glyphicon-remove"></span>
                            </a>
                        </td>
                    </tr>
                </table>
            </div>
        </div>

        <div class="col-md-8 col-md-offset-2 col-lg-8 col-lg-offset-2 col-sm-12 col-xs-12 page-tab shadow-paper" id="cprofile" hidden>
            <div class="form row">
                <form @submit.prevent="update_profile" class="form-horizontal">
                    <h3 class="profile-title">Profile</h3>
                    <div class="profile-content">
                        <div class="profile-avatar-col">
                            <profile-avatar v-on:avatar_changed="parent_avatar_changed" :profile_photo="profile_photo"></profile-avatar>
                        </div>
                        <div class="form row col-md-7 col-md-offset-1" v-if="candidate.user">
                            <div class="form-group has-feedback ">
                                <label>First Name</label>
                                <input type="text" class="form-control" v-model="candidate.user.first_name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback ">
                                <label>Last Name</label>
                                <input type="text" class="form-control" placeholder="Last Name" v-model="candidate.user.last_name" />
                                <i class="glyphicon glyphicon-user form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>email</label>
                                <input class="form-control email" type="text" placeholder="Email" v-model="candidate.user.email" />
                                <i class="glyphicon glyphicon-envelope form-control-feedback"></i>
                            </div>
                            <div class="form-group has-feedback">
                                <label>Phone</label>
                                <input class="form-control phone" type="text" placeholder="Phone" v-model="candidate.user.phone" />
                                <i class="glyphicon glyphicon-phone form-control-feedback"></i>
                            </div>
                            <div class="form-group">
                                <label>City</label>
                                <input class="form-control required" type="text" placeholder="City" v-model="candidate.user.city" />
                            </div>
                            <div class="form-group">
                                <label>Date of Birth</label>
                                <input class="form-control required" type="date" name="bdate" style="text-transform:uppercase" v-model="candidate.date_of_birth" />
                            </div>
                            <div class="form-group" id="gender">
                                <label>Gender</label>
                                <select title="Gender" v-model="candidate.gender">
                                    <option value="N">Not Specified</option>
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                </select>
                            </div>
                            <div class="form-group" id="education">
                                <label>Highest Education</label>
                                <select v-model="candidate.highest_education">
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
                            <div class="checkbox">
                                <input type="checkbox" id="looking-for-work-checkbox" v-model="candidate.looking_for_work">
                                <label for="looking-for-work-checkbox">I am currently looking for work.</label>
                            </div>
                            <div class="form-group">
                                <label>Minimum Annual Salary</label>
                                <input class="form-control" type="number" min="0" placeholder="Minimum Salary" v-model="candidate.minimum_salary" />
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
                                        <input type="text" v-model="cities" class="form-control" placeholder="Cities">
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
                        <button class="button-like pull-right" v-bind:class="{liked : matched_jobs.has(job.id)}" :disabled="matched_jobs.has(job.id)" @click="create_match(job)" :id="'btn_match_'+job.id" :job-id="job.id">
                            <i class="fa fa-heart"></i>
                            <span v-if="!matched_jobs.has(job.id)">Match</span>
                        </button>
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

        <div id="job-matched-list" class="page-tab" hidden>
            <div class="filter-bar">
                <label>Show jobs containing</label>
                <input type="text" class="form-control" v-model="match_job_name" @change="filter_job_matches()">
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
                <select v-model="sort_field" @change="sort_job_matches()">
                    <option value="J_Name">Job Name</option>
                    <option value="Company">Company</option>
                    <option value="C_F_Name">Contact First Name</option>
                    <option value="C_L_Name">Contact Last Name</option>
                    <option value="Salary">Salary</option>
                    <option value="J_Date">Job Posting Date</option>
                </select>
                <select v-model="sort_order" @change="sort_job_matches()">
                    <option value="Ascending">Ascending</option>
                    <option value="Descending">Descending</option>
                </select>
            </div>
            <div class="card-table">
                <JobCard :match="match" v-for="(match,index) in filtered_job_matches" :key="index" v-on:job_clicked="view_job_details(match.job)" />
                <div class="no-matches" v-if="!filtered_job_matches || filtered_job_matches.length===0">
                    <h2>Sorry, we didn't find any job matches.</h2>
                </div>
            </div>
        </div>

        <div id="job-details-tab" class="page-tab" hidden>
            <job-details v-if="selected_job != null" :job="selected_job" v-on:close_clicked="close_job_details" />
        </div>
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
                <div class="modal-body">You do not meet the requirements for this job. Do you really want to apply for it?</div>
                <div class="modal-footer">
                    <button type="button" parentid="myModal" @click="force_create_match" class="btn btn-primary modal-close">Yes</button>
                    <button type="button" parentid="myModal" @click="cancel_create_match" class="btn btn-second modal-close">No</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal -->
    </div>

</div>
</template>

<!-- JavaScript -->
<script>
import "font-awesome/css/font-awesome.min.css";
import "../../static/assets/css/build.css";
import "../../static/assets/js/bootstrap-select.min.js";
import axios from "axios";
import * as ss from '../assets/js/skillstash.js';
import $ from "jquery";
import JobCard from "@/components/JobCard";
import JobDetails from "@/components/JobDetails";
import PasswordForm from "./PasswordForm";
import ProfileAvatar from "./ProfileAvatar";
import TreeNode from "./TreeNode";
export default {
    name: "CandidateProfile",
    components: {
        JobCard,
        JobDetails,
        PasswordForm,
        ProfileAvatar,
        TreeNode
    },
    computed: {
        doc_types() {
            return ss.doc_types;
        }
    },
    data() {
        return {
            loading: false,
            treeData: [],
            c_skills: [],
            root_skills: [],
            candidate: [],
            jobposts: [],
            docs: [],
            selected_file: {name:'No File Chosen'},
            upload_doc_type: "O",
            upload_doc_desc: "",
            profile_photo: null,
            all_job_matches: null,
            matched_jobs: new Map(),
            filtered_job_matches: null,
            selected_job: null,
            detail_previous_page: null,
            cities: "",
            name_contains: "",
            desc_contains: "",
            max_education: 0,
            min_education: 0,
            contact_person: [],
            min_salary: "",
            max_salary: "",
            job_to_force_apply: null,
            password1: "",
            password2: "",
            match_job_name: "",
            match_state: "Active",
            sort_field: "J_Name",
            sort_order: "Ascending"
        };
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
        load_user() {
            var user_id = sessionStorage.getItem("user_id");
            axios({
                method: "get",
                url: API_HOST + "/api/candidates/" + user_id + "/"
            }).then(response => {
                if (response.status === 200) {
                    console.log(response.data);
                    this.candidate = response.data;
                    if (this.candidate.photo != "")
                        this.profile_photo =
                        API_HOST +
                        "/api/download/" +
                        user_id +
                        "/" +
                        this.candidate.photo;
                }
            });
        },
        update_profile() {
            if (!ss.validate_user(this.candidate.user))
                return;
            if (this.candidate.minimum_salary === "") {
                this.candidate.minimum_salary = 0;
            }
            axios({
                method: "put",
                url: API_HOST + "/api/candidates/" + this.candidate.user.id + "/",
                data: this.candidate
            }).then(response => {});
        },
        parent_avatar_changed(new_avatar_path) {
            this.profile_photo = new_avatar_path;
            console.log(this.profile_photo);
        },
        choose_file(){
            $('#doc_file').trigger('click')
        },
        select_file_changed(event){
            console.log(event)
            this.selected_file = event.target.files[0];
        },
        upload_doc() {
            var doc_file = document.getElementById("doc_file");
            if (doc_file.files.length == 0) {
                alert("No file selected for upload.");
                return;
            }
            const form_data = new FormData();
            form_data.append("file", doc_file.files[0]);
            form_data.append("type", this.upload_doc_type);
            form_data.append("description", this.upload_doc_desc);
            axios({
                method: "put",
                url: API_HOST + "/api/upload-doc/" + doc_file.files[0].name,
                data: form_data
            }).then(response => {
                if (response.status === 201) {
                    this.upload_doc_desc = "";
                    doc_file.value = "";
                    // See if this document replaces an existing document.
                    var i = 0;
                    while (i < this.docs.length && this.docs[i].id != response.data.id)
                        i++;
                    var doc = response.data;
                    doc.url =
                        API_HOST +
                        "/api/download/" +
                        sessionStorage.getItem("user_id") +
                        "/" +
                        doc.filename;
                    this.docs.splice(i, 0, doc);
                }
            }).catch(error => {
                alert(error.response.data);
            });
        },
        update_doc(doc) {
            axios({
                method: "put",
                url: API_HOST + "/api/candidate-docs/" + doc.id + "/",
                data: doc
            }).then(response => {
                console.log(response.data);
            }).catch(error => {
                alert(error.response.data);
            });
        },
        remove_doc(doc, index) {
            if (confirm("Are you sure that you want to delete " + doc.filename + "?")) {
                axios({
                    method: "delete",
                    url: API_HOST + "/api/candidate-docs/" + doc.id + "/"
                }).then(response => {
                    console.log(response.data);
                    this.docs.splice(index, 1);
                }).catch(error => {
                    alert(error.response.data);
                });
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
            this.cities = this.cities.trim();
            axios({
                method: "get",
                url: API_HOST + "/api/job-posts-and-skills/",
                params: {
                    states: 'L,JO', // Only include active job posts.
                    cities: this.cities != "" ? this.cities : null,
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
                for (let index in this.jobposts) {
                    let jobpost = this.jobposts[index];
                    $(function () {
                        $(".button-like").bind("click", function (event) {
                            //console.log(event);
                            $(event.currentTarget).toggleClass("liked");
                        });
                    });
                }
            });
        },
        load_root_skills() {
            axios({
                method: "get",
                url: API_HOST + "/api/skills/",
                params: {
                    category: "root"
                }
            }).then(response => {
                this.root_skills = response.data;
                for (var index in this.root_skills) {
                    var root_skill = this.root_skills[index];
                    this.treeData.push({
                        label: root_skill.name,
                        type: root_skill.type,
                        id: root_skill.id
                    });
                }
                this.$forceUpdate();
            });
        },
        edit_skills() {
            $(".page-tab").hide();
            $("#skill-list").show();
        },
        edit_docs() {
            $(".page-tab").hide();
            $("#doc-page").show();
        },
        edit_profile() {
            $(".page-tab").hide();
            $("#cprofile").show();
        },
        change_password() {
            $(".page-tab").hide();
            $("#password_tab").show();
        },
        view_jobs() {
            $(".page-tab").hide();
            this.load_job_matches();
            this.detail_previous_page = "job";
            $("#jobposts").show();
        },
        load_job_matches() {
            // The back end will only return matches for this candidate.
            axios({
                method: "get",
                url: API_HOST + "/api/job-matches-and-posts/"
            }).then(response => {
                if (response.status === 200) {
                    this.all_job_matches = response.data;
                    this.matched_jobs.clear();
                    for (var i = 0; i < this.all_job_matches.length; i++) {
                        var match = this.all_job_matches[i];
                        if (!this.matched_jobs.has(match.job.id)) {
                            this.matched_jobs.set(match.job.id, match);
                            $("#btn_match_" + match.job.id).addClass("liked");
                        }
                    }
                    this.filter_job_matches();
                }
            });
        },
        filter_job_matches() {
            var filter_job_matches = function(m) {
                if (this.match_job_name != '' && !m.job.name.includes(this.match_job_name))
                    return false;
                if (this.match_state == 'All')
                    return true;
                if (this.match_state == 'Active')
                    return m.state == 'N' || m.state == 'CI' || m.state == 'EI' || m.state == 'P' || m.state == 'JO';
                if (this.match_state == 'Inactive')
                    return m.state == 'DC' || m.state == 'DE' || m.state == 'H' || m.state == 'JD' || m.state == 'F' || m.state == 'W';
                return m.state == this.match_state;
            }

            if (this.match_job_name != '' || this.match_state != '') {
                this.filtered_job_matches = this.all_job_matches.filter(filter_job_matches, this);
            } else {
                this.filtered_job_matches = this.all_job_matches.slice();
            }
            this.sort_job_matches();
        },
        sort_job_matches() {
            let order = (this.sort_order === 'Ascending') ? 1 : -1;
            if (this.sort_field === 'J_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.job.name.localeCompare(b.job.name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.sort_field === 'Company') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.job.contact_person.company.localeCompare(b.job.contact_person.company, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.sort_field === 'C_F_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.job.contact_person.user.first_name.localeCompare(b.job.contact_person.user.first_name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.sort_field === 'C_L_Name') {
                this.filtered_job_matches.sort(function(a, b) {
                    return a.job.contact_person.user.last_name.localeCompare(b.job.contact_person.user.last_name, 'en', {sensitivity: 'base'}) * order;
                });
            } else if (this.sort_field === 'Salary') {
                this.filtered_job_matches.sort(function(a, b) {
                    return (a.job.equiv_annual_salary - b.job.equiv_annual_salary) * order;
                });
            } else if (this.sort_field === 'J_Date') {
                this.filtered_job_matches.sort(function(a, b) {
                    // This hack relies on the fact that newer jobs will have higher IDs.
                    return (a.job.id - b.job.id) * order;
                });
            }
        },
        view_job_matches() {
            $(".page-tab").hide();
            this.load_job_matches();
            this.detail_previous_page = "match";
            $("#job-matched-list").show();
        },
        view_job_details(job) {
            this.selected_job = job;
            $('.page-tab').hide();
            $('#job-details-tab').show();
        },
        close_job_details() {
            $('.page-tab').hide();
            if (this.detail_previous_page === 'match') {
                $('#job-matched-list').show();
            } else {
                $('#jobposts').show();
            }
        },
        add_skills() {
            // Get the checkboxes from the candidate skill tree.
            var skill_tree = document.getElementById("candidate-skill-tree");
            var checkboxes = skill_tree.querySelectorAll('input[name="skill_checkbox"]');
            var search_skills = "";
            for (var index = 0; index < checkboxes.length; ++index) {
                var checkbox = checkboxes[index];
                if (checkbox.checked) {
                    var skill_id = parseInt(checkbox.attributes["idvalue"].value);
                    // Make sure this skill hasn't already been added.
                    if (!this.id_to_skill.has(skill_id)) {
                        var skill_name = checkbox.attributes["namevalue"].value;
                        var cs = {
                            skill: {
                                id: skill_id,
                                name: skill_name
                            },
                            proficiency: 1,
                            months_experience: 0,
                            experience: 0,
                            experience_unit: 12,
                            evidence: []
                        }
                        // Special handling for a skill being removed and then added again.
                        var deleted_cs = this.deleted_c_skills.get(skill_id)
                        if (deleted_cs != undefined) {
                            cs.id = deleted_cs.id
                            cs.modified = true
                            this.deleted_c_skills.delete(skill_id)
                        }
                        // Insert the new skill into the list in alphabetical order.
                        var i = 0;
                        while (i < this.c_skills.length && this.c_skills[i].skill.name < skill_name) {
                            i++;
                        }
                        this.c_skills.splice(i, 0, cs)
                        this.id_to_skill.set(skill_id, cs);
                    }
                }
            }
        },
        remove_skill(cs, index) {
            if (cs.id != undefined) {
                this.deleted_c_skills.set(cs.skill.id, cs)
            }
            this.c_skills.splice(index, 1);
            this.id_to_skill.delete(cs.skill.id);
        },
        mark_skill_changed(cs) {
            if (cs.id != undefined) {
                cs.modified = true;
            }
        },
        save_skill_changes() {
            for (var i = 0; i < this.c_skills.length; i++) {
                var cs = this.c_skills[i]
                if (cs.id === undefined) {
                    // This is a newly added skill.
                    axios({
                        method: "post",
                        url: API_HOST + "/api/candidate-skills/",
                        data: {
                            skill: cs.skill.id,
                            proficiency: cs.proficiency,
                            months_experience: cs.experience * cs.experience_unit,
                            evidence: cs.evidence
                        }
                    }).then(response => {
                        this.id_to_skill.get(response.data.skill).id = response.data.id
                    });
                } else if (cs.modified) {
                    axios({
                        method: "patch",
                        url: API_HOST + "/api/candidate-skills/" + cs.id + "/",
                        data: {
                            id: cs.id,
                            skill: cs.skill.id,
                            proficiency: cs.proficiency,
                            months_experience: cs.experience * cs.experience_unit,
                            evidence: cs.evidence
                        }
                    }).then(response => {
                        delete this.id_to_skill.get(response.data.skill).modified
                        console.log(response.data);
                    });
                }
            }

            for (let cs of this.deleted_c_skills.values()) {
                this.delete_candidate_skill(cs)
            }
        },
        delete_candidate_skill(cs) {
            axios({
                method: "delete",
                url: API_HOST + "/api/candidate-skills/" + cs.id + "/"
            }).then(response => {
                this.deleted_c_skills.delete(cs.skill.id)
            });
        },
        revert_candidate_skills() {
            if (confirm("Are you sure you want to revert all unsaved changes to your skills?")) {
                this.load_user_skills()
            }
        },
        create_match(job) {
            let is_matched = false;
            for (let index = 0; index < this.all_job_matches.length; index++) {
                if (job.id === this.all_job_matches[index].job.id) {
                    is_matched = true;
                    break;
                }
            }
            if (!is_matched) {
                axios({
                        method: "post",
                        url: API_HOST + "/api/create-manual-match/",
                        data: {
                            job: job.id,
                            candidate: this.candidate.user.id
                        }
                }).then(response => {
                    if (response.status === 200) {
                        let match = response.data;
                        this.all_job_matches.push(match);
                        this.matched_jobs.set(match.id, match)
                        $("#btn_match_" + job.id).addClass("liked");
                        $("#btn_match_" + job.id).attr('disabled',true)
                    }
                }).catch(error => {
                    if (error.response.status === 400) {
                        this.job_to_force_apply = job;
                        jQuery("#confirmModal").modal("show");
                    }
                });
            }
        },
        force_create_match() {
            let job = this.job_to_force_apply;
            axios({
                method: "post",
                url: API_HOST + "/api/create-manual-match/",
                data: {
                    job: job.id,
                    candidate: this.candidate.user.id,
                    validate: false
                }
            }).then(response => {
                if (response.status === 200) {
                    let match = response.data
                    this.all_job_matches.push(match);
                    this.matched_jobs.set(match.job.id, match)
                    $("#btn_match_" + job.id).addClass("liked")
                    $("#btn_match_" + job.id).attr('disabled',true)
                }
            });
            jQuery("#confirmModal").modal("hide");
        },
        cancel_create_match() {
            jQuery("#confirmModal").modal("hide");
            $("#btn_match_" + this.job_to_force_apply.id).removeClass("liked");
        },
        load_user_skills() {
            this.id_to_skill = new Map();
            this.deleted_c_skills = new Map();
            axios({
                method: "get",
                url: API_HOST + "/api/candidate-skills/",
                params: {
                    candidate: sessionStorage.getItem("user_id")
                }
            }).then(response => {
                this.c_skills = response.data;
                for (var index in this.c_skills) {
                    var cs = this.c_skills[index]
                    this.id_to_skill.set(cs.skill.id, cs);
                }
                console.log(this.c_skills);
            });
        },
        load_user_docs() {
            this.docs = [];
            var user_id = sessionStorage.getItem("user_id");
            axios({
                method: "get",
                url: API_HOST + "/api/candidate-docs/",
                params: {
                    candidate: user_id
                }
            }).then(response => {
                var c_docs = response.data;
                for (var index in c_docs) {
                    var doc = c_docs[index];
                    doc.url = API_HOST + "/api/download/" + user_id + "/" + doc.filename;
                    this.docs.push(doc);
                }
                console.log(this.docs);
            });
        }
    },
    beforeMount() {
        this.loading = false;
        this.load_user();
        this.load_root_skills();
        this.load_user_docs();
        this.load_user_skills();
    },
    updated() {
        $(".selectpicker").selectpicker("refresh");
        $(".selectpicker").selectpicker("render");
    }
};
</script>

<!-- CSS -->
<style lang="scss">
@import '../assets/css/skillstash.css';

/* page properties */
#doc-page {
    margin: 10px;
}

#doc-list {
    margin-top: 10px;
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
    height: 30px;
    width: 30px;
}

/* elements */
#skill-list {
    background: #fff;
    border-radius: 4px;
    overflow: visible;
    display: flex;
    flex-direction: row;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
    padding: 20px 15px 20px 20px;
    margin: 10px;
}

.doc-table {
    margin-top: 2em;
    border-collapse:separate !important;
    border-spacing:0 0.5rem !important;
}

#doc-type {
    display: inline-block;
    width: 20em;
}

#doc-type option {
    width: 20em;
}

.doc-upload {
    margin-top: 2em;
}

.doc-upload span {
    display: inline-block;
}

</style>

<style scoped>
@import "../../static/assets/css/normalize.css";
@import "../../static/assets/css/themify-icons.css";
@import "../../static/assets/css/cs-skin-elastic.css";
@import "../../static/assets/scss/style.css";
@import "../../static/assets/css/lib/vector-map/jqvmap.min.css";
@import "../assets/css/skillstash.css";
</style>
